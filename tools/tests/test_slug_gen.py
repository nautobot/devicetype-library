from dtl_tools.slug_gen import generate_slug


def test_slug_basic():
    assert generate_slug("Arista", "DCS-7050CX3-32S-F") == "arista-dcs-7050cx3-32s-f"


def test_slug_palo_alto():
    assert generate_slug("Palo Alto", "PA-5540") == "palo-alto-pa-5540"


def test_slug_special_chars():
    assert generate_slug("F5", "BIG-IP i2600") == "f5-big-ip-i2600"
