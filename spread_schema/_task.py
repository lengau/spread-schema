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
"""Pydantic models for a task.yaml file."""

import pydantic

from ._base import BaseModel, CoercedString


class TaskYaml(BaseModel):
    """task.yaml, a single task for spread."""

    summary: str = pydantic.Field(description="A brief summary of this task")
    artifacts: list[str] | None = pydantic.Field(
        default=None, description="Artifact paths to fetch after the test completes."
    )
    environment: dict[str, CoercedString] | None = pydantic.Field(
        default_factory=dict,  # type: ignore[arg-type]
        description="Environment variables for this test.",
    )
    prepare: str | None = pydantic.Field(
        default=None, description="Preparation to do for this task."
    )
    execute: str = pydantic.Field(
        description="The script where the actual testing is run."
    )
    restore: str | None = pydantic.Field(
        default=None,
        description="Restore script. Runs after the task regardless of success.",
    )
    debug: str | None = pydantic.Field(
        default=None, description="Debug script to run if the test fails."
    )
    manual: bool = pydantic.Field(
        default=False, description="Set to true to run this test only manually."
    )
