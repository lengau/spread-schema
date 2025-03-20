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
from typing import Annotated, Literal, TypedDict

import pydantic

from ._base import BaseModel, CoercedString, PrepareRestoreEachModel


class System(BaseModel):
    """A customised system."""

    username: str | None = None
    password: str | None = None
    workers: int | None = None
    memory: str | None = None
    storage: str | None = None


class BaseBackend(PrepareRestoreEachModel):
    """Backend configuration."""

    model_config = PrepareRestoreEachModel.model_config | pydantic.ConfigDict(
        extra="forbid",
    )

    systems: list[str | dict[str, System]] = pydantic.Field(
        description="Operating systems and versions that this backend will start.",
        examples=[
            "fedora-41-64",
            {"ubuntu-24.04-64": {"workers": 4}},
        ],
    )


class LxdBackend(BaseBackend):
    type: Literal["lxd"] = "lxd"


class QemuBackend(BaseBackend):
    type: Literal["qemu"] = "qemu"


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
    # With Python 3.14 (https://peps.python.org/pep-0728/),
    # set extra_items=Backend
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
    environment: dict[str, str] | None = pydantic.Field(
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
        coerce_numbers_to_str=True,
    )
    backends: dict[str, Backend] = pydantic.Field(description="Backend configuration")
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
