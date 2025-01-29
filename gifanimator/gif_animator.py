import os
from typing import Optional
from PIL import Image
from gifanimator import BaseAnimation

class GIFAnimator:
    """Manages applying animations and generating an animated GIF."""

    def __init__(self, animation: BaseAnimation):
        self.animation = animation

    def generate_gif(self, image: Image.Image, output_path: str):
        """
        Applies the animation and saves the output.

        :param image: The input image (RGBA mode recommended for transparency).
        :param output_path: File path to save the generated animation.
        """
        frames = self.animation.apply(image)

        if not frames:
            raise ValueError("No frames were generated.")

        output_ext = os.path.splitext(output_path)[-1].lower()

        if output_ext == ".gif":
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                loop=0,
                duration=self.animation.duration,
                transparency=0,  # Only applies to GIFs
                disposal=2  # Preserve transparency correctly
            )
        else:
            frames[0].save(output_path)  # Standard save for non-GIF formats