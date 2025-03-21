# This file is part of spread_schema.
#
# Copyright 2025 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Pydantic models for a spread.yaml file."""

import pathlib
from typing import Annotated, Literal

import pydantic
from typing_extensions import TypedDict

from ._base import BaseModel, CoercedString, PrepareRestoreEachModel


class System(BaseModel):
    """A customised system."""

    image: str | None = pydantic.Field(
        default=None,
        description="The name of the image to use. Defaults to the system name.",
    )
    username: str | None = None
    password: str | None = None
    workers: int | None = None
    memory: str | None = None
    storage: str | None = pydantic.Field(
        default=None,
        description="Storage to set on the system. Only used by google and linode backends.",
    )
    bios: Literal["uefi", None] = pydantic.Field(
        default=None, description="Bios type to use. Only used by QEMU backend."
    )
    secure_boot: bool = pydantic.Field(
        default=False,
        description="Whether to use secure boot. Only used by the Google backend.",
    )
    environment: dict[str, CoercedString] = pydantic.Field(
        default_factory=dict,
        description="Environment variables to set on this system.",
    )
    manual: bool = pydantic.Field(
        default=False,
        description="Whether to run this system manually. Defaults to false.",
    )


class BaseBackend(PrepareRestoreEachModel):
    """Backend configuration."""

    systems: list[str | dict[str, System]] = pydantic.Field(
        description="Operating systems and versions that this backend will start.",
        examples=[
            "fedora-41-64",
            {"ubuntu-24.04-64": {"workers": 4}},
        ],
    )
    environment: dict[str, CoercedString] = pydantic.Field(
        default_factory=dict,
        description="Environment variables to set on this backend.",
    )


class LxdBackend(BaseBackend):
    type: Literal["lxd"] = "lxd"


class QemuBackend(BaseBackend):
    type: Literal["qemu"] = "qemu"
    memory: str | None = pydantic.Field(
        default=None, description="The amount of memory to provide to each worker."
    )


class GoogleBackend(BaseBackend):
    """A backend running on Google Cloud.

    See the documentation for more info:
    https://github.com/canonical/spread?tab=readme-ov-file#google
    """

    type: Literal["google"] = "google"
    key: str | None = pydantic.Field(
        default=None,
        description="Path to a Google key JSON file. If unset, uses the current user's default credentials.",
        examples=["$(HOST:echo $GOOGLE_JSON_FILENAME)"],
    )
    location: str
    halt_timeout: str | None = pydantic.Field(
        default=None,
        description="Timeout after which the systems will automatically shutdown.",
        examples=["6h"],
    )


class LinodeBackend(BaseBackend):
    type: Literal["linode"] = "linode"
    key: str = pydantic.Field(
        description="Linode API key", examples=["$(HOST:echo $LINODE_API_KEY)"]
    )
    halt_timeout: str | None = pydantic.Field(
        default=None,
        description="Timeout after which the systems will automatically shutdown.",
        examples=["6h"],
    )
    plan: str | None = pydantic.Field(
        default=None,
        description="The plan to use when allocating new machines.",
    )
    location: str | None = pydantic.Field(
        default=None,
        description="The data centre in which to allocate new machines.",
    )


class AdhocBackend(BaseBackend):
    """A backend which allows creating machines using custom scripts.

    https://github.com/canonical/spread?tab=readme-ov-file#adhoc
    """

    type: Literal["adhoc"] = "adhoc"
    allocate: str = pydantic.Field(
        description="Allocation script. Runs on the local machine."
    )
    discard: str = pydantic.Field(
        description="Discard script. Runs on the local machine."
    )


# When adding a new backend, also append it to this union and
# add it to BackendDict.
Backend = Annotated[
    LxdBackend | QemuBackend | GoogleBackend | LinodeBackend | AdhocBackend,
    pydantic.Field(discriminator="type"),
]


class BackendDict(TypedDict, total=False):
    __pydantic_config__ = pydantic.ConfigDict(  # type: ignore[misc]
        extra="allow",
    )
    __extra_items__: Backend
    lxd: LxdBackend
    qemu: QemuBackend
    google: GoogleBackend
    linode: LinodeBackend
    adhoc: AdhocBackend


SuitePath = Annotated[
    str,
    pydantic.Field(
        description="The relative path to a suite.",
        pattern=r"[^/].*/",
    ),
]


class Suite(PrepareRestoreEachModel):
    """Processed spread suite configuration."""

    summary: str = pydantic.Field(description="A summary of the tests in this suite.")
    systems: list[str] | None = pydantic.Field(
        default=None,
        description="A list of systems to test on. Defaults to all available.",
    )
    backends: list[str] | None = pydantic.Field(
        default=None,
        description="Backends to run this suite on. Defaults to all available.",
    )
    environment: dict[str, CoercedString] | None = pydantic.Field(
        default=None, description="Environment variables to set in this test suite."
    )
    warn_timeout: str | None = pydantic.Field(
        default=None,
        description="Default warn timeout for tests in this suite. Defaults to the project warn-timeout. -1 will disable timeout altogether.",
        examples=["30s", "1m30s", "10m", "1.5h"],
    )
    kill_timeout: str | None = pydantic.Field(
        default=None,
        description="Default kill timeout for tests in this suite. Defaults to the project kill-timeout. -1 will disable timeout altogether.",
        examples=["30s", "1m30s", "10m", "1.5h"],
    )
    manual: bool = pydantic.Field(
        default=False, description="Only run this suite when explicitly specified."
    )
    priority: int | None = pydantic.Field(
        default=None, description="Priority for this suite. Higher runs earlier."
    )


class SpreadYaml(PrepareRestoreEachModel):
    """A spread configuration file (spread.yaml)."""

    project: str = pydantic.Field(
        description="The name of the project",
        examples=["hello-world"],
    )
    path: pathlib.Path = pydantic.Field(
        description="The base path to copy to on the remote machine.",
    )
    environment: dict[str, CoercedString] = pydantic.Field(
        default_factory=dict,
        description="Environment variables to set across the entire project.",
    )
    backends: BackendDict = pydantic.Field(description="Backend configuration")
    suites: dict[SuitePath, Suite]
    include: list[str] = pydantic.Field(
        default_factory=lambda: ["*"],
        description="A list of path globs to send to each worker.",
    )
    exclude: list[str] | None = pydantic.Field(
        default=None,
        description="A list of path globs to exclude.",
    )
    rename: list[str] | None = pydantic.Field(
        default=None,
        description="A list of regex replacements for renaming or moving files.",
    )
    warn_timeout: str | None = pydantic.Field(
        default=None,
        description="Default warn timeout for tests. Defaults to 5 minutes. -1 will disable timeout altogether.",
        examples=["30s", "1m30s", "10m", "1.5h"],
    )
    kill_timeout: str | None = pydantic.Field(
        default=None,
        description="Default kill timeout for tests. Defaults to 15 minutes. -1 will disable timeout altogether.",
        examples=["30s", "1m30s", "10m", "1.5h"],
    )
    repack: str | None = pydantic.Field(
        default=None,
        description="Script to run when repacking the data. File descriptors 3 and 4, respectively, are pipes for the specified project content into and out of the script, in tar format.",
    )
