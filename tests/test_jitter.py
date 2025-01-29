import pytest
import os
from PIL import Image

from gifanimator.jitter_animation import JitterAnimation
from gifanimator.gif_animator import GIFAnimator


@pytest.fixture
def test_img():
    """Fixture for creating a test image."""
    return Image.new("RGBA", (100, 100), (255, 0, 0, 255))


@pytest.fixture
def test_output():
    """Fixture for output file path."""
    output_path = "test_output.gif"
    yield output_path
    if os.path.exists(output_path):
        os.remove(output_path)


def test_jitter_animation_does_not_crash(test_img):
    """Ensures JitterAnimation applies without crashing."""
    effect = JitterAnimation(frames=10, max_shift=5)
    frames = effect.apply(test_img)

    assert isinstance(frames, list)
    assert len(frames) > 0
    assert isinstance(frames[0], Image.Image)


def test_gifanimator_generates_gif(test_img, test_output):
    """Ensures GIFAnimator successfully generates a GIF."""
    effect = JitterAnimation(frames=10, max_shift=5)
    animator = GIFAnimator(effect)
    animator.generate_gif(test_img, test_output)

    assert os.path.exists(test_output)