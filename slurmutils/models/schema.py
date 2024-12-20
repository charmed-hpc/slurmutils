# Copyright 2024 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""JSON schemas for validating Slurm data models."""

__all__ = [
    "GRES_NAME_SCHEMA",
    "GRES_NODE_SCHEMA",
    "GRES_NAME_MAPPING_SCHEMA",
    "GRES_NODE_MAPPING_SCHEMA",
]

_GLOBAL_SCHEMA_VERSION = "https://json-schema.org/draft/2020-12/schema"

# `gres.conf` data model schemas.
GRES_NAME_SCHEMA = {
    "$schema": _GLOBAL_SCHEMA_VERSION,
    "type": "object",
    "properties": {
        "AutoDetect": {"type": "string"},
        "Count": {"type": "string"},
        "Cores": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "File": {"type": "string"},
        "Flags": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "Links": {"type": "array", "items": {"type": "string"}},
        "MultipleFiles": {"type": "string"},
        "Name": {"type": "string"},
        "Type": {"type": "string"},
    },
    "additionalProperties": False,
}

GRES_NODE_SCHEMA = {
    "$schema": _GLOBAL_SCHEMA_VERSION,
    "type": "object",
    "properties": {
        "NodeName": {"type": "string"},
        **GRES_NAME_SCHEMA["properties"],
    },
    "additionalProperties": False,
}

GRES_NAME_MAPPING_SCHEMA = {
    "$schema": _GLOBAL_SCHEMA_VERSION,
    "type": "object",
    "patternProperties": {
        "^.+$": {
            "type": "array",
            "items": {
                "$ref": "#/$defs/GRESName",
            },
            "uniqueItems": True,
        },
    },
    "$defs": {"GRESName": GRES_NAME_SCHEMA},
}

GRES_NODE_MAPPING_SCHEMA = {
    "$schema": _GLOBAL_SCHEMA_VERSION,
    "type": "object",
    "patternProperties": {
        "^.+$": {
            "type": "array",
            "items": {"$ref": "#/$defs/GRESNode"},
            "uniqueItems": True,
        }
    },
    "$defs": {
        "GRESNode": GRES_NODE_SCHEMA,
    },
}

GRES_CONFIG_SCHEMA = {
    "$schema": _GLOBAL_SCHEMA_VERSION,
    "type": "object",
    "properties": {
        "AutoDetect": {"type": "string"},
        "Names": {"$ref", "#/$defs/GRESNameMapping"},
        "Nodes": {"$ref", "#/$defs/GRESNodeMapping"},
    },
    "additionalProperties": False,
    "$defs": {
        "GRESNameMapping": GRES_NAME_MAPPING_SCHEMA,
        "GRESNodeMapping": GRES_NODE_MAPPING_SCHEMA,
    },
}
