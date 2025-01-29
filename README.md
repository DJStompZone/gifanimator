# GIF Animator

A Python library for applying animated effects to still images and generating GIFs with **alpha transparency**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
pip install gifanimator
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

```bash
gifanimator input.png output.gif --params '{"effect": "jitter", "duration": 2, "params": {"frames": 10, "max_shift": 5}}'
```

Generate a **really** jittery animated GIF:

```bash
gifanimator input.png output.gif --params '{"effect": "jitter", "duration": 2, "params": {"frames": 10, "max_shift": 5}}'  --params '{"effect": "jitter", "duration": 4, "params": {"frames": 30, "max_shift": 15}}'
```

**Note:** As seen above, multiple effects can be applied by appending more than one `--params` argument

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
3. Register the effect in ANIMATION_CLASSES in **main**.py.

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

MIT License. See the [LICENSE](LICENSE) file for details.

<hr>

<div align="center"><br><img src="https://i.imgur.com/L31eOwn.png"/>
<h1><a href="https://github.com/djstompzone"><img src="https://img.shields.io/github/stars/DJStompZone?label=DJStompZone%20%7C%20Stars"/></a><br><a href="https://discord.stomp.zone"><img src="https://img.shields.io/discord/599808270655291403?logo=discord&label=StompZone%20Discord"/></a><br><a href="https://youtube.com/@djstompzone"><img src="https://img.shields.io/youtube/channel/views/UCVmIXrlXjpzJTGkANYlTxaQ"/></a></h1></div>
