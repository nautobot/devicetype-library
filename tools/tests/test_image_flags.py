from dtl_tools.image_flags import should_have_front_image, should_have_rear_image


def test_front_image_detected(tmp_path):
    img_dir = tmp_path / "elevation-images" / "Arista"
    img_dir.mkdir(parents=True)
    (img_dir / "arista-dcs-7050cx3-32s-f.front.png").write_bytes(b"PNG")
    assert should_have_front_image("DCS-7050CX3-32S-F", "Arista", tmp_path) is True


def test_no_image(tmp_path):
    img_dir = tmp_path / "elevation-images" / "Arista"
    img_dir.mkdir(parents=True)
    assert should_have_front_image("DCS-FAKE-MODEL", "Arista", tmp_path) is False


def test_rear_image(tmp_path):
    img_dir = tmp_path / "elevation-images" / "Arista"
    img_dir.mkdir(parents=True)
    (img_dir / "arista-dcs-7050cx3-32s-f.rear.png").write_bytes(b"PNG")
    assert should_have_rear_image("DCS-7050CX3-32S-F", "Arista", tmp_path) is True
