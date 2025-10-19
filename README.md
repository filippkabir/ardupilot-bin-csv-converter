# ArduPilot Bin to CSV Converter

A Python utility for converting ArduPilot binary log files (.bin) to CSV format for analysis and visualization.

## Overview

ArduPilot flight controllers generate binary log files (.bin) that contain telemetry data from flights. This tool provides a simple way to convert these binary files into human-readable CSV format, making it easy to analyze flight data in spreadsheet applications or data analysis tools.

## Features

- Convert ArduPilot .bin files to CSV format
- Preserve all message types and parameters
- Command-line interface for batch processing
- Python API for programmatic usage
- Support for all standard ArduPilot log message types

## Installation

### Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Convert a single bin file:
```bash
python bin2csv.py input.bin output.csv
```

Convert multiple files:
```bash
python bin2csv.py *.bin --output-dir ./csv_files/
```

### Python API

```python
from src.converter import BinToCsvConverter

converter = BinToCsvConverter()
converter.convert('flight_log.bin', 'flight_log.csv')
```

## File Structure

```
ardupilot-bin-csv-converter/
├── src/
│   ├── __init__.py
│   ├── converter.py          # Main conversion logic
│   └── parser.py             # Binary file parser
├── tests/
│   └── test_converter.py     # Unit tests
├── examples/
│   └── basic_usage.py        # Example usage script
├── docs/
│   └── api.md                # API documentation
├── bin2csv.py                # CLI script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## ArduPilot Log Format

ArduPilot binary logs contain various message types including:
- IMU data (accelerometer, gyroscope)
- GPS coordinates and status
- Attitude information (roll, pitch, yaw)
- Motor outputs and control inputs
- System status and error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- ArduPilot project for the flight controller software
- pymavlink library for MAVLink protocol support