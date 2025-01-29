import math
import random
from PIL import Image, ImageSequence
from gifanimator import BaseAnimation

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
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, self.max_shift)
            
            dx = int(distance * math.cos(angle))
            dy = int(distance * math.sin(angle))

            jittered = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            jittered.paste(image, (dx, dy), image)
            frames.append(jittered)

        return frames
