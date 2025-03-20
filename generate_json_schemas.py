#!/usr/bin/env python3
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
"""Generate JSON schema file for spread.yaml."""

import json
import pathlib

import spread_schema

PROJECT_DIR = pathlib.Path(__file__).parent
SCHEMA_DIR = PROJECT_DIR / "schema"

with (SCHEMA_DIR / "spread.json").open("w") as f:
    json.dump(
        spread_schema.SpreadYaml.model_json_schema(),
        f,
        indent=2,
    )
    f.write("\n")
