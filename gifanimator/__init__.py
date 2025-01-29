from typing import Optional
from abc import ABC, abstractmethod
from PIL import Image

class BaseAnimation(ABC):
    """Abstract base class for animated image effects."""

    def __init__(self, duration: int|float = 2, params: Optional[dict[str, str | int | bool | list[str] | list[int]]] = None):
        """
        :param duration: Frame duration in milliseconds.
        :param params: Optional dictionary of animation parameters.
        """
        self.duration = duration
        self.params = params or {}

    @abstractmethod
    def apply(self, images: Image.Image | list[Image.Image]) -> list[Image.Image]:
        """Apply the animation effect and return a list of frames."""
