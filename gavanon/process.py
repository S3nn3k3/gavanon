# Copyright Senne Vanden Berghe, 2024
# This data is copied from prof. dr. ir. Pieter Rombouts Matlab script from the Gavanon course.

from dataclasses import dataclass


@dataclass(frozen=True)
class NMOS:
    """Contains all needed values of the NMOS transistor in the 0.35µm technology"""
    KP_n = 170e-6
    n = 1.3
    VT = 0.7
    VEarly = 18e6
    vsat = 8e4
    Cox = 6e-3
    Kf = 1.6e-26
    CDB0 = 0.5e-9
    CSB0 = 0.5e-9
    CGS0 = 0.1e-9
    CGD0 = 0.1e-9


@dataclass(frozen=True)
class PMOS:
    """Contains all needed values of the PMOS transistor in the 0.35µm technology"""
    KP_n = 50e-6
    n = 1.3
    VT = 0.7
    VEarly = 8e6
    vsat = 8e4
    Cox = 6e-3
    Kf = 4e-28
    CDB0 = 0.5e-9
    CSB0 = 0.5e-9
    CGD0 = 0.09e-9
    CGS0 = 0.1e-9
