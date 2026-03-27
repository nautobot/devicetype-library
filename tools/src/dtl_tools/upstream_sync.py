"""Fetch and adapt YAML device types from upstream netbox-community repo."""

from pathlib import Path

import requests

UPSTREAM_API = "https://api.github.com/repos/netbox-community/devicetype-library/contents/device-types/{manufacturer}"
UPSTREAM_RAW = "https://raw.githubusercontent.com/netbox-community/devicetype-library/master/device-types/{manufacturer}/{filename}"


def adapt_yaml_content(content: str) -> str:
    """Remove slug, mgmt_only: false; ensure trailing newline."""
    lines = content.splitlines()
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("slug:"):
            continue
        if stripped == "mgmt_only: false":
            continue
        result.append(line)
    out = "\n".join(result)
    if not out.endswith("\n"):
        out += "\n"
    return out


def list_upstream_models(manufacturer: str) -> list[str]:
    """List all YAML filenames from upstream for a manufacturer."""
    url = UPSTREAM_API.format(manufacturer=manufacturer)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return [f["name"] for f in resp.json() if f["name"].endswith((".yaml", ".yml"))]


def fetch_upstream_yaml(manufacturer: str, filename: str) -> str:
    """Fetch raw YAML content from upstream."""
    url = UPSTREAM_RAW.format(manufacturer=manufacturer, filename=filename)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def sync_missing(manufacturer: str, local_dir: Path) -> list[str]:
    """Download and adapt all missing models. Returns list of created files."""
    local_models = {f.stem for f in local_dir.glob("*.yaml")} | {f.stem for f in local_dir.glob("*.yml")}
    upstream_files = list_upstream_models(manufacturer)

    created = []
    for filename in upstream_files:
        stem = filename.rsplit(".", 1)[0]
        if stem not in local_models:
            content = fetch_upstream_yaml(manufacturer, filename)
            adapted = adapt_yaml_content(content)
            target = local_dir / filename.replace(".yml", ".yaml")
            target.write_text(adapted)
            created.append(target.name)
    return created
