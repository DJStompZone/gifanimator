import math
import random
from PIL import Image
from gifanimator import BaseAnimation

class JitterAnimation(BaseAnimation):
    """Applies a jittery effect by shifting the image in a random direction from the origin."""
    
    def __init__(self, *args, frames: int = 10, max_shift: int = 5, **kwargs):
        """
        :param frames: Number of frames in the animation.
        :param max_shift: Maximum pixel shift for jittering in any direction.
        """
        super().__init__(*args, **kwargs)
        self.frames = frames
        self.max_shift = max_shift

    def apply(self, images: Image.Image | list[Image.Image]) -> list[Image.Image]:
        """
        Apply jitter effect to a single image or a list of images.
        Parameters:
        images (Image.Image | list[Image.Image]): A single PIL Image object or a list of PIL Image objects to which the jitter effect will be applied.
        Returns:
        list[Image.Image]: A list of PIL Image objects with the jitter effect applied.
        The jitter effect randomly shifts the image by a small amount in a random direction for a specified number of frames.
        """
        frames = []

        if isinstance(images, list):
            for img in images:
                width, height = img.size
                for _ in range(self.frames):
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(0, self.max_shift)
                    
                    dx = int(distance * math.cos(angle))
                    dy = int(distance * math.sin(angle))

                    jittered = Image.new("RGBA", (width, height), (0, 0, 0, 0))
                    jittered.paste(img, (dx, dy), img)
                    frames.append(jittered)
        else:
            width, height = images.size
            for _ in range(self.frames):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, self.max_shift)
                
                dx = int(distance * math.cos(angle))
                dy = int(distance * math.sin(angle))

                jittered = Image.new("RGBA", (width, height), (0, 0, 0, 0))
                jittered.paste(images, (dx, dy), images)
                frames.append(jittered)

        return frames
