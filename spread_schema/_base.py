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
"""Base model for spread-schema models."""

from typing import Annotated, Any

import pydantic


def alias_generator(s: str) -> str:
    """Generate an alias YAML key."""
    return s.replace("_", "-")


class BaseModel(pydantic.BaseModel):
    """Base model for spread models."""

    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        extra="forbid",
        populate_by_name=True,
        alias_generator=alias_generator,
        coerce_numbers_to_str=True,
    )


class PrepareRestoreEachModel(BaseModel):
    """A model that has prepare, restore, prepare-each and restore-each keys."""

    prepare: str | None = pydantic.Field(
        default=None, description="prepare script. Runs once per worker."
    )
    restore: str | None = pydantic.Field(
        default=None, description="restore script. Runs once per worker."
    )
    prepare_each: str | None = pydantic.Field(
        default=None, description="prepare-each script. Runs once per task."
    )
    restore_each: str | None = pydantic.Field(
        default=None, description="restore-each script. Runs once per task."
    )
    debug: str | None = pydantic.Field(
        default=None, description="Script to run when other scripts fail."
    )
    debug_each: str | None = pydantic.Field(
        default=None, description="Debug script to run when each script fails"
    )


CoercedString = Annotated[
    str,
    pydantic.BeforeValidator(str, json_schema_input_type=Any),
    pydantic.Field(
        coerce_numbers_to_str=True,
    ),
]
