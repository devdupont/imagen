import unittest

from imagen.config import cfg
from imagen.service.conversion_service import copy_image_to_images_folder


class TestDBModel(unittest.TestCase):
    def test_image_copy(self):
        images_2 = cfg.image_path.parent / "images_2"
        assert images_2.exists()
        images_to_copy = list(images_2.glob("*"))
        assert len(images_to_copy) > 0
        image_to_copy = images_to_copy[0]
        assert image_to_copy.exists()
        copied = copy_image_to_images_folder(image_to_copy)
        assert copied.exists()
        copied.unlink()
        assert not copied.exists()

    def test_image_copy_2(self):
        images_2 = cfg.image_path.parent / "images_2"
        image_to_copy = (
            images_2
            / "DALL·E 2024-03-17 19.36.03 - An abstract representation of the concept of economy of time, featuring a large, vintage clock in the center, its hands moving rapidly. Surrounding th.webp"
        )
        assert image_to_copy.exists()
        copied = copy_image_to_images_folder(image_to_copy)
        assert copied.exists()
        copied.unlink()
        assert not copied.exists()


if __name__ == "__main__":
    unittest.main()
