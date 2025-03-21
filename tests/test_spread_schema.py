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
"""Tests for the spread.yaml schema."""

import pathlib

import jsonschema
import pytest
import yaml
from spread_schema import SpreadYaml

TESTS_DIR = pathlib.Path(__file__).parent
VALID_SPREAD_DIR = TESTS_DIR / "valid_spread_files"


@pytest.fixture(scope="session")
def spread_schema():
    return SpreadYaml.model_json_schema()


@pytest.mark.parametrize(
    "path",
    [pytest.param(path, id=path.name) for path in VALID_SPREAD_DIR.glob("*.yaml")],
)
def test_validate_valid_files(path: pathlib.Path, spread_schema):
    with path.open("r") as f:
        spread_yaml = yaml.safe_load(f)

    jsonschema.validate(spread_yaml, spread_schema)
