from typing import Optional
from PIL import Image
from gifanimator import BaseAnimation

class GIFAnimator:
    """Manages applying animations and generating an animated GIF."""

    def __init__(self, animation: BaseAnimation):
        self.animation = animation

    def generate_gif(self, image: Image.Image, output_path: str):
        """
        Applies the animation and saves an animated GIF.

        :param image: The input image (RGBA mode recommended for transparency).
        :param output_path: File path to save the generated GIF.
        """
        frames = self.animation.apply(image)

        if frames:
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                loop=0,
                duration=self.animation.duration,
                transparency=0,
                disposal=2
            )