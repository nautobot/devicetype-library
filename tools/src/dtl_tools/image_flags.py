"""Add front_image/rear_image flags to YAML based on actual elevation image files."""

from pathlib import Path

import yaml


def _image_exists(model: str, manufacturer: str, repo_root: Path, side: str) -> bool:
    prefix = manufacturer.lower().replace(" ", "-")
    img_name = f"{prefix}-{model.lower()}.{side}.png"
    img_dir = repo_root / "elevation-images" / manufacturer
    return (img_dir / img_name).exists()


def should_have_front_image(model: str, manufacturer: str, repo_root: Path) -> bool:
    return _image_exists(model, manufacturer, repo_root, "front")


def should_have_rear_image(model: str, manufacturer: str, repo_root: Path) -> bool:
    return _image_exists(model, manufacturer, repo_root, "rear")


def update_image_flags(device_dir: Path, manufacturer: str, repo_root: Path) -> int:
    """Update front_image/rear_image in all YAML files. Returns modified count."""
    count = 0
    for f in sorted(device_dir.glob("*.yaml")):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if not data:
            continue
        model = data.get("model", "")
        content = f.read_text()
        changed = False

        has_front = should_have_front_image(model, manufacturer, repo_root)
        has_rear = should_have_rear_image(model, manufacturer, repo_root)

        if has_front and "front_image:" not in content:
            content = content.replace("is_full_depth:", "front_image: true\nis_full_depth:")
            if "front_image:" not in content:
                content = content.replace("u_height:", "front_image: true\nu_height:")
            changed = True
        if has_rear and "rear_image:" not in content:
            content = content.replace("front_image: true\n", "front_image: true\nrear_image: true\n")
            changed = True

        if changed:
            f.write_text(content)
            count += 1
    return count
