from enum import Enum


class PotentialEnum(Enum):
    HO = "harmonic_oscillator"
    MORSE = "morse"
    BARRIER = "rectangular_barrier"
    HIGH_BARRIER = "high_barrier"
    STEP = "step"
    OPEN = "open"
