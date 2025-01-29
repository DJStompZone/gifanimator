import argparse
import os
from typing import Optional, Any

from PIL import Image

from gifanimator.jitter_animation import JitterAnimation
from gifanimator.gif_animator import GIFAnimator

# Supported animations
ANIMATION_CLASSES = {
    "jitter": JitterAnimation,
}

def parse_animation_params(effect: str, options: dict[str, Any]):
    """Parses animation parameters and returns an instance of the animation class."""
    if effect not in ANIMATION_CLASSES:
        raise ValueError(f"Unknown animation effect: {effect}")

    animation_class = ANIMATION_CLASSES[effect]
    return animation_class(**options)


def main(input_img: str, output_img: str, params: Optional[list[dict[str, Any]]]):
    """Applies animations to an image and saves as GIF."""
    
    if not os.path.exists(input_img):
        raise OSError(f"Input image not found: {input_img}")

    img = Image.open(input_img).convert("RGBA")

    # Instantiate effects
    effects = [parse_animation_params(effect["effect"], effect["params"]) for effect in params]

    animator = GIFAnimator(*effects)
    animator.generate_gif(img, output_img)
    print(f"GIF saved to {output_img}")


def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Apply animated effects to an image and save as a GIF.")
    
    parser.add_argument("input_img", type=str, help="Path to the input image (PNG recommended).")
    parser.add_argument("output_img", type=str, help="Path to save the output GIF.")
    parser.add_argument(
        "--params",
        type=str,
        nargs="+",
        help="JSON strings defining animation parameters, e.g., '{\"effect\": \"jitter\", \"params\": {\"frames\": 10, \"max_shift\": 5}}'",
    )

    args = parser.parse_args()

    # Convert JSON strings to Python dicts
    try:
        effect_params = [json.loads(param) for param in args.params] if args.params else []
    except Exception as e:
        print(f"{e.__class__.__name__} encountered while parsing args:", e)
        raise ValueError from e

    main(input_img=args.input_img, output_img=args.output_img, params=effect_params)


if __name__ == "__main__":
    parse_args()