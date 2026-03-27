"""Validate YAML device types against JSON schema."""

import json
from pathlib import Path

import yaml
from jsonschema import Draft4Validator, RefResolver


def validate_device_type(yaml_path: Path, schema_dir: Path) -> list[str]:
    """Validate a single YAML file. Returns list of error messages."""
    schema_file = schema_dir / "devicetype.json"
    with open(schema_file) as f:
        schema = json.load(f)
    resolver = RefResolver(f"file://{schema_dir.resolve()}/", schema)
    validator = Draft4Validator(schema, resolver=resolver)
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return [e.message for e in validator.iter_errors(data)]


def validate_all(device_dir: Path, schema_dir: Path) -> dict[str, list[str]]:
    """Validate all YAML files. Returns {filename: [errors]}."""
    results = {}
    for f in sorted(device_dir.glob("*.yaml")):
        errors = validate_device_type(f, schema_dir)
        if errors:
            results[f.name] = errors
    return results
