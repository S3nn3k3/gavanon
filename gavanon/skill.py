# Copyright Senne Vanden Berghe, 2024

from __future__ import annotations
from typing import List, Union
from os import PathLike

import warnings

from .transistor import Transistor, DoubleTransistor
from .sources import CurrentSource, VoltageSource


class CadenceCell:
    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Library name must be a string!")
        else:
            self._name: str = name

        self._transistors: List[Transistor] = []
        self._double_transistors: List[DoubleTransistor] = []
        self._current_sources: List[CurrentSource] = []
        self._voltage_sources: List[VoltageSource] = []
        self._free_entries: List[str] = []

    def add(self, element: Union[Transistor, DoubleTransistor, CurrentSource, VoltageSource], *args):
        """Add an element to the CadanceCell class"""
        for e in [element] + list(args):
            if isinstance(e, Transistor):
                self._transistors.append(e)
            elif isinstance(e, DoubleTransistor):
                self._double_transistors.append(e)
            elif isinstance(e, CurrentSource):
                self._current_sources.append(e)
            elif isinstance(e, VoltageSource):
                self._voltage_sources.append(e)
            else:
                warnings.warn(
                    f"Cannot add instance which is not Transistor OR DoubleTransistor OR CurrentSource OR VoltageSource. ({repr(e)})")  # noqa E501
        return self

    def __iadd__(self, element: Union[Transistor, DoubleTransistor, CurrentSource, VoltageSource]):
        return self.add(element)

    def add_free_entry(self, text_entry: str):
        """Adds string to SetProperties in skill script.

        Args:
            text_entry (str): Entry you would like to add in skill script
        """
        if not isinstance(text_entry, str):
            raise TypeError("Text entry must be a string instance!")
        self._free_entries.append(text_entry)
        return self

    def _get_set_properties_text(self, lib_name: str) -> str:
        # Returns string for cell that needs to be pasted
        def helper(elements):
            # helper function for formatting the text files
            t = ""
            maximum = [0, 0, 0, 0]
            for element in elements:
                el = element._properties()
                maximum = [max(e, len(el[i]) if i < len(el) else 0)
                           for i, e in enumerate(maximum)]
            # when maximum is found make text based on maximum values
            for element in elements:
                el = element._properties()
                # t += f"\t\"{el[0]:^{maximum[0]}} : {el[1]:^{maximum[1]}}; {el[2]:^{maximum[2]}}; {el[3]:^{maximum[3]}}\"\n"  # noqa E501
                t += f"\t\"{el[0]:^{maximum[0]}} : "
                t += "; ".join([f"{el[i]:^{maximum[i]}}" for i in range(1, len(el))])
                t += "\"\n"
            return t

        text = f"SetProperties(\"{lib_name}.{self._name}.schematic\"\n"
        text += helper(self._transistors + self._double_transistors +
                       self._current_sources + self._voltage_sources)
        text += '\n'.join(self._free_entries)  # add free text to properties
        text += ");\n"
        return text

    def export_sizing(self, skill_name: str, lib_name: str):
        # Is not really needed since most of the time you just use a CadenceLib instance
        with open(skill_name, 'w') as file:
            file.write("load(\"autoschematic.il\")\n")
            file.write(self._get_set_properties_text(lib_name))


class CadenceLib:
    """Cadance Libray class
    """

    def __init__(self, name: str) -> None:
        """Cadence Libray class is used to define the Cadence library.

        Args:
            name (str): Name of the Cadence library

        Raises:
            TypeError: When name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Library name must be a string!")

        self._name: str = name

        self._cells: List[CadenceCell] = []

    def add(self, *args: CadenceCell):
        """Add (multiple) CadanceCell objects to the CadenceLib class object. \n
        """
        for c in list(args):
            if isinstance(c, CadenceCell):
                self._cells.append(c)
            else:
                warnings.warn("Cannot add instance which is not a CadenceCell")
        return self

    def __iadd__(self, cell: CadenceCell):
        return self.add(cell)

    def __str__(self) -> str:
        return self._name

    def export_sizing(self, skill_name: Union[str, bytes, PathLike]):
        """Makes skill script file in __main__ directory or specified path.

        Args:
            skill_name (Union[str, bytes, PathLike]): name or path of the skill script.

        Returns:
            self
        """
        with open(skill_name, 'w', encoding='utf-8') as file:
            file.write("load(\"autoschematic.il\")\n")
            for cell in self._cells:
                file.write(cell._get_set_properties_text(self._name))
        return self
