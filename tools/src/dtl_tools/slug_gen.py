"""Generate URL-friendly slugs for device type YAML files."""

import re
from pathlib import Path

import yaml


def generate_slug(manufacturer: str, model: str) -> str:
    """Generate a URL-friendly slug from manufacturer and model."""
    slug = f"{manufacturer}-{model}".lower()
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def add_slugs_to_dir(device_dir: Path) -> int:
    """Add slug to all YAML files missing it. Returns count of modified files."""
    count = 0
    for f in sorted(device_dir.glob("*.yaml")):
        content = f.read_text()
        if "slug:" in content:
            continue
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if not data:
            continue
        manufacturer = data.get("manufacturer", "")
        model = data.get("model", "")
        if not manufacturer or not model:
            continue
        slug = generate_slug(manufacturer, model)
        content = content.replace(
            f"model: {model}\n",
            f"model: {model}\nslug: {slug}\n",
        )
        f.write_text(content)
        count += 1
    return count
