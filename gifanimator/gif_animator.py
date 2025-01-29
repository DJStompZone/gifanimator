import os
from PIL import Image
from gifanimator import BaseAnimation

class GIFAnimator:
    """Manages applying animations and generating an animated GIF."""

    def __init__(self, animations: list[BaseAnimation]):
        self.animations = animations

    def generate_gif(self, image: Image.Image, output_path: str):
        """
        Applies the animations in sequence to the entire frame array.

        :param image: The input image (RGBA mode recommended for transparency).
        :param output_path: File path to save the generated animation.
        """
        frames = [image]
        print(f"[DEBUG] Initial frames: {len(frames)}")  # 🔍 Debugging

        for animation in self.animations:
            frames = animation.apply(frames)  # Ensure it returns a valid list
            print(f"[DEBUG] After {animation.__class__.__name__}, frames: {len(frames)}")  # 🔍 Debugging

            if not frames or not all(isinstance(f, Image.Image) for f in frames):
                raise ValueError(f"[ERROR] Invalid frames after {animation.__class__.__name__}")

        if not frames:
            raise ValueError("[ERROR] No valid frames were generated.")

        output_ext = os.path.splitext(output_path)[-1].lower()

        # Use the last applied animation's duration
        last_duration = self.animations[-1].duration if self.animations else 50
        duration_list = [last_duration] * len(frames)

        if output_ext == ".gif":
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                loop=0,
                duration=duration_list,
                transparency=0,  # Only applies to GIFs
                disposal=2  # Preserve transparency correctly
            )
        else:
            base_name, ext = os.path.splitext(output_path)
            for i, frame in enumerate(frames):
                frame.save(f"{base_name}_{i}{ext}")  # Save each frame separately for non-GIF formats
