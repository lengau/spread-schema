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
"""spread_schema base package."""

try:
    from ._version import __version__
except ImportError:  # pragma: no cover
    from importlib.metadata import version, PackageNotFoundError

    try:
        __version__ = version("spread_schema")
    except PackageNotFoundError:
        __version__ = "dev"


from ._base import alias_generator, BaseModel, PrepareRestoreEachModel
from ._spread import System, Backend, BackendDict, SuitePath, Suite, SpreadYaml
from ._task import TaskYaml


__all__ = [
    "__version__",
    "alias_generator",
    "BaseModel",
    "PrepareRestoreEachModel",
    "System",
    "Backend",
    "BackendDict",
    "SuitePath",
    "Suite",
    "SpreadYaml",
    "TaskYaml",
]
