# Copyright Senne vanden Berghe, 2024

from __future__ import annotations
from typing import Optional, Union

from ._element import _Element


class Source(_Element):
    """Source base class"""

    def __init__(self) -> None:
        super().__init__()


class VoltageSource(Source):
    """Voltage source

    Args:
        V (Optional[Union[float, int]], optional): Voltage. Defaults to None.
    """

    def __init__(self, V: Optional[Union[float, int]] = None) -> None:
        self._V: float = 0
        self.V = V  # use setter for santization
        super().__init__()

    @property
    def V(self):
        return self._V

    @V.setter
    def V(self, v_val):
        if not (isinstance(v_val, int) or isinstance(v_val, float)):
            raise TypeError("Voltage must be a float!")
        self._V = v_val

    def _properties(self) -> list:
        return [self.name, f"vdc={self._V:.3f}"]


class CurrentSource(Source):
    """Current source

    Args:
        I (Optional[Union[float, int]], optional): Current. Defaults to None.
    """

    def __init__(self, I: Optional[Union[float, int]] = None) -> None:
        self._I: float = 0
        self.I = I  # use setter for santization
        super().__init__()

    @property
    def I(self):
        return self._I

    @I.setter
    def I(self, i_val):
        if not isinstance(i_val, (int, float)):
            raise TypeError("Current must be a float!")
        self._I = i_val

    def _properties(self) -> list:
        return [self.name, f"idc={self._I*1e6:.3f}u"]
