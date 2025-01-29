# GIF Animator

A Python library for applying animated effects to still images and generating GIFs with **alpha transparency**.

## Features
- **Extensible API**: Easily add new animation effects.
- **Preserves Transparency**: Ensures smooth rendering with RGBA images.
- **CLI Support**: Apply effects from the command line.

### Supported Animations

At this time, supported animations are:
- **Jitter**: Adds a random shaking effect to images.

## Installation

### Via PyPi

(Coming soon)

```sh
# pip install gifanimator
```

### Via GitHub (developers)

Clone the repository and install dependencies:

```sh
git clone https://github.com/DJStompZone/gifanimator.git
cd gifanimator
pip install .
```

## Usage

### CLI Usage

Generate a jittery animated GIF:
```
python -m gifanimator input.png output.gif \
    --params '{"effect": "jitter", "params": {"frames": 10, "max_shift": 5}}'
```


### Programmatic Usage
```py
from PIL import Image
from gifanimator.jitter_animation import JitterAnimation
from gifanimator.gif_animator import GIFAnimator

img = Image.open("input.png").convert("RGBA")

effect = JitterAnimation(frames=10, max_shift=5)
animator = GIFAnimator(effect)

animator.generate_gif(img, "output.gif")
print("GIF saved as output.gif")
```

## Contributions

### Adding New Effects

1. Create a new animation class by subclassing BaseAnimation.
2. Implement the apply() method to return a list of frames.
3. Register the effect in ANIMATION_CLASSES in __main__.py.

Example:
```py
class MyCustomAnimation(BaseAnimation):
    def apply(self, image):
        # Custom frame processing logic
        return [image]  # Return modified frames
```

### Running Tests

Ensure everything works as expected with:

```bash
pytest tests
```

## License
[MIT License](LICENSE)

## Author
DJ Stomp
GitHub: [@DJStompZone](https://github.com/djstompzone)
<br>
Discord: https://discord.stomp.zone