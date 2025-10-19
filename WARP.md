# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

ArduPilot Bin to CSV Converter is a Python utility for converting ArduPilot binary log files (.bin) to CSV format for analysis and visualization. The project uses pymavlink for parsing MAVLink protocol data from flight controller logs.

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install in development mode (if needed)
pip install -e .
```

### Running the Tool
```bash
# Convert single file
python bin2csv.py input.bin output.csv

# Convert multiple files
python bin2csv.py *.bin --output-dir ./csv_files/

# List available message types
python bin2csv.py flight.bin --list-types

# Get file information
python bin2csv.py flight.bin --info

# Convert specific message types
python bin2csv.py flight.bin -o output.csv -m GPS -m IMU

# Create separate files by message type
python bin2csv.py flight.bin -d ./output/ --separate-by-type
```

### Testing
```bash
# Run tests (pytest is included in requirements.txt)
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_converter.py
```

### Code Quality
```bash
# Check code formatting (if using black)
black src/ bin2csv.py

# Type checking (if using mypy)
mypy src/

# Linting (if using flake8)
flake8 src/ bin2csv.py
```

## Architecture

### Core Components

**BinFileParser (`src/parser.py`)**
- Handles low-level binary file parsing using pymavlink
- Validates ArduPilot .bin files
- Extracts messages and metadata from binary logs
- Provides generator-based parsing for memory efficiency

**BinToCsvConverter (`src/converter.py`)**
- High-level conversion logic and orchestration
- Handles single file and batch conversions
- Supports message type filtering and separation
- Manages output file generation and directory creation

**CLI Interface (`bin2csv.py`)**
- Command-line interface using Click framework
- Supports glob patterns for batch processing
- Provides verbose logging and error handling
- Offers multiple output formats (single/separate files)

### Data Flow

1. **Validation**: BinFileParser validates input .bin files using pymavlink
2. **Parsing**: Messages are extracted as dictionaries with timestamps and message types
3. **Filtering**: Optional filtering by message types (GPS, IMU, ATT, etc.)
4. **Conversion**: pandas DataFrames are created from message dictionaries
5. **Output**: CSV files are generated either combined or separated by message type

### Key Dependencies

- **pymavlink**: MAVLink protocol library for ArduPilot log parsing
- **pandas**: Data manipulation and CSV generation
- **click**: Command-line interface framework
- **numpy**: Numerical computing (pandas dependency)

### Message Types

ArduPilot logs contain various message types including:
- IMU data (accelerometer, gyroscope)
- GPS coordinates and status  
- Attitude information (roll, pitch, yaw)
- Motor outputs and control inputs
- System status and error messages

### Memory Considerations

The parser uses generator-based parsing to handle large .bin files efficiently. For very large files, consider:
- Processing specific message types only (`-m` option)
- Using separate file output to reduce memory usage
- Batch processing with smaller chunks if needed

## Development Notes

### Testing Strategy
- Unit tests should be placed in `tests/` directory
- Test files should follow `test_*.py` naming convention
- Use pytest fixtures for common test data (sample .bin files)
- Mock pymavlink connections for unit tests to avoid dependency on actual .bin files

### Error Handling
- File validation occurs before processing
- Graceful handling of corrupted or invalid .bin files
- Detailed logging for debugging conversion issues
- CLI provides user-friendly error messages

### Performance
- Generator-based parsing minimizes memory usage
- Batch processing supports multiple files efficiently
- pandas operations are optimized for CSV output
- Large file processing should be monitored for memory consumption