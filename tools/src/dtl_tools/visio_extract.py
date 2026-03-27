"""Extract elevation images and model mappings from Visio VSSX stencil files."""

import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

import defusedxml.ElementTree as DefusedET

NS_VISIO = {"v": "http://schemas.microsoft.com/office/visio/2012/main"}
NS_REL = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
NS_OREL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


@dataclass
class VssMaster:
    name: str
    master_id: str
    image_file: str
    is_rear: bool = False


def parse_vssx_masters(vssx_path: Path) -> list[VssMaster]:
    """Parse VSSX and return list of masters with their image files."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(vssx_path) as zf:
            zf.extractall(tmp_path)

        rels_path = tmp_path / "visio/masters/_rels/masters.xml.rels"
        rid_to_file = {}
        if rels_path.exists():
            tree = DefusedET.parse(rels_path)
            for rel in tree.getroot().findall(".//r:Relationship", NS_REL):
                rid_to_file[rel.get("Id")] = rel.get("Target", "")

        masters_xml = tmp_path / "visio/masters/masters.xml"
        tree = DefusedET.parse(masters_xml)
        root = tree.getroot()

        results = []
        for master in root.findall(".//v:Master", NS_VISIO):
            mid = master.get("ID")
            name = master.get("Name", "")
            if not name or "connector" in name.lower():
                continue

            rel_elem = master.find(".//v:Rel", NS_VISIO)
            if rel_elem is None:
                continue
            rid = rel_elem.get(f"{{{NS_OREL}}}id")
            master_file = rid_to_file.get(rid, "")
            master_num = master_file.replace("master", "").replace(".xml", "")

            master_rels = tmp_path / f"visio/masters/_rels/master{master_num}.xml.rels"
            if not master_rels.exists():
                continue

            r2 = DefusedET.parse(master_rels)
            for r in r2.getroot().findall(".//r:Relationship", NS_REL):
                if "image" in r.get("Type", ""):
                    img = r.get("Target", "").replace("../media/", "")
                    is_rear = "(rear" in name.lower()
                    results.append(VssMaster(
                        name=name,
                        master_id=mid,
                        image_file=img,
                        is_rear=is_rear,
                    ))
        return results


def extract_images(vssx_path: Path, output_dir: Path, manufacturer_prefix: str = "arista") -> dict[str, Path]:
    """Extract images from VSSX and rename to nautobot convention."""
    masters = parse_vssx_masters(vssx_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(vssx_path) as zf:
            zf.extractall(tmp_path)

        media_dir = tmp_path / "visio/media"
        mapping = {}

        for m in masters:
            src = media_dir / m.image_file
            if not src.exists():
                continue

            clean_name = m.name.split(" (")[0].strip()
            while clean_name and clean_name[-1].isdigit() and "." in clean_name:
                parts = clean_name.rsplit(".", 1)
                if parts[-1].isdigit():
                    clean_name = parts[0]
                else:
                    break

            side = "rear" if m.is_rear else "front"
            ext = src.suffix
            target_name = f"{manufacturer_prefix}-{clean_name.lower()}.{side}{ext}"
            target = output_dir / target_name

            shutil.copy2(src, target)
            mapping[f"{clean_name}:{side}"] = target

        return mapping
