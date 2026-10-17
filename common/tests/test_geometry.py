import numpy as np
import pytest

from ecv_common.geometry import Homography

H = np.array([[0.02, 0.001, -3.0], [0.0005, 0.03, -5.0], [1e-5, 2e-4, 1.0]])


def test_roundtrip_pixel_ground_pixel():
    h = Homography(H)
    px = np.array([[100.0, 200.0], [640.0, 360.0], [1000.0, 700.0]])
    back = h.ground_to_pixel(h.pixel_to_ground(px))
    assert np.allclose(back, px, atol=1e-6)


def test_yaml_roundtrip(tmp_path):
    p = tmp_path / "h.yaml"
    Homography(H).save(p)
    assert np.allclose(Homography.load(p).H, H)
    assert p.read_text().startswith("%YAML:1.0")


def test_bad_shape():
    with pytest.raises(ValueError):
        Homography(np.eye(2))
