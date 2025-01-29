import argparse
import os
import re
import json
from typing import Optional, Any

from PIL import Image

from gifanimator.jitter_animation import JitterAnimation
from gifanimator.gif_animator import GIFAnimator

# Supported animations
ANIMATION_CLASSES = {
    "jitter": JitterAnimation,
}


def repair_json_string(broken_str: str) -> str:
    """Fixes a malformed JSON-like string by handling escape sequences and adding missing quotes."""
    if broken_str.startswith("[") and broken_str.endswith("]"):
        broken_str = broken_str[1:-1]
    broken_str = broken_str.replace("\\'", "'")
    if broken_str.startswith("'") and broken_str.endswith("'"):
        broken_str = broken_str[1:-1]
    repaired_str = re.sub(r'(?<!["\'])\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?=\s*:)', r'"\1"', broken_str)
    repaired_str = re.sub(r'(:\s*)([a-zA-Z_][a-zA-Z0-9_]*)\b(?!\s*["\'}])', r'\1"\2"', repaired_str)
    repaired_str = repaired_str.replace("'", '"')
    try:
        parsed = json.loads(repaired_str) # Never hurts to double-check
        return json.dumps(parsed)
    except json.JSONDecodeError as err:
        raise ValueError("The input string could not be transformed into valid JSON") from err


def parse_params(params: list[str]) -> list[dict[str, Any]]:
    """Parses JSON strings into dictionaries."""
    _params = []
    for param in params:
        try:
            _params.append(json.loads(param))
        except json.JSONDecodeError:
            print(f"Attempting to repair malformed JSON string: {param}")
            try:
                _params.append(repair_json_string(param))
            except ValueError as e:
                print(f"Error: {e}")
    try:
        return [json.loads(param) for param in _params]
    except json.decoder.JSONDecodeError:
        print("Attempting alternate JSON parsing method")
        print(f"[Debug info] (Before) {_params=} {repr(_params)=}")
        _params = [ea.replace("\\'", '"').replace("'", '"') for ea in _params]
        print(f"[Debug info] (After) {_params=} {repr(_params)=}")
        return [json.loads(param) for param in _params]
    except Exception as e:
        print(f"{e.__class__.__name__} encountered while parsing params:", e)
        print(f"Debug info: {_params=} {repr(_params)=}")
        return []


def parse_animation_params(effect: str, duration: int|float, options: dict[str, Any]):
    """Parses animation parameters and returns an instance of the animation class."""
    if effect not in ANIMATION_CLASSES:
        raise ValueError(f"Unknown animation effect: {effect}")

    animation_class = ANIMATION_CLASSES[effect]
    return animation_class(duration=duration, **options)


def main(input_img: str, output_img: str, params: Optional[list[dict[str, Any]]]):
    """Applies animations to an image and saves as GIF."""

    if not os.path.exists(input_img):
        raise OSError(f"Input image not found: {input_img}")

    img = Image.open(input_img).convert("RGBA")

    effects = [parse_animation_params(
        effect=effect["effect"],
        duration=effect["duration"],
        options=effect["params"]
    ) for effect in params]
    print(f"[DEBUG] {effects=}")
    animator = GIFAnimator(effects)
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
        help="JSON strings defining animation parameters, e.g., '{\"effect\": \"jitter\", \"duration\": 3, \"params\": {\"frames\": 10, \"max_shift\": 5}}'",
    )

    args = parser.parse_args()

    effect_params = parse_params(args.params)

    main(input_img=args.input_img, output_img=args.output_img, params=effect_params)


if __name__ == "__main__":
    parse_args()
