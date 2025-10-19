"""
ArduPilot Bin to CSV Converter Package

A Python utility for converting ArduPilot binary log files (.bin) to CSV format.
"""

__version__ = "1.0.0"
__author__ = "ArduPilot Bin Converter Team"

from .converter import BinToCsvConverter
from .parser import BinFileParser

__all__ = ["BinToCsvConverter", "BinFileParser"]