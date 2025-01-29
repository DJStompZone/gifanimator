import math
import random
import os
from abc import ABC, abstractmethod
from typing import Optional
from PIL import Image, ImageSequence

class BaseAnimation(ABC):
    """Abstract base class for animated image effects."""

    def __init__(self, duration: int = 50, params: Optional[dict[str, str | int | bool | list[str] | list[int]]] = None):
        """
        :param duration: Frame duration in milliseconds.
        :param params: Optional dictionary of animation parameters.
        """
        self.duration = duration
        self.params = params or {}

    @abstractmethod
    def apply(self, image: Image.Image) -> list[Image.Image]:
        """Apply the animation effect and return a list of frames."""
        pass

class JitterAnimation(BaseAnimation):
    """Applies a jittery effect by shifting the image in a random direction from the origin."""
    
    def __init__(self, frames: int = 10, max_shift: int = 5, **kwargs):
        """
        :param frames: Number of frames in the animation.
        :param max_shift: Maximum pixel shift for jittering in any direction.
        """
        super().__init__(**kwargs)
        self.frames = frames
        self.max_shift = max_shift

    def apply(self, image: Image.Image) -> list[Image.Image]:
        frames = []
        width, height = image.size

        for _ in range(self.frames):
            # Choose a random angle and distance within the max_shift radius
            angle = random.uniform(0, 2 * math.pi)  # Random direction
            distance = random.uniform(0, self.max_shift)  # Random displacement magnitude
            
            dx = int(distance * math.cos(angle))
            dy = int(distance * math.sin(angle))

            jittered = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            jittered.paste(image, (dx, dy), image)
            frames.append(jittered)

        return frames

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
                disposal=2  # Preserve transparency correctly
            )