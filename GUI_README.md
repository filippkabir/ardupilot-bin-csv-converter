# ArduPilot Bin to CSV Converter - GUI Version

A graphical user interface for converting ArduPilot binary log files (.bin) to CSV format using TKinter.

## Features

- **Easy File Selection**: Browse and select input `.bin` files with automatic output filename generation
- **Auto Path Generation**: Automatically generates output CSV filename when you select an input file
- **Log Window**: Real-time logging of all conversion operations
- **File Information**: Display detailed information about binary log files before conversion
- **Conversion Options**:
  - Separate output by message type
  - Verbose logging for debugging
- **Status Bar**: Real-time status updates during operations
- **Error Handling**: Clear error messages with automatic validation

## Requirements

- Python 3.6 or higher
- TKinter (usually included with Python)
- All dependencies from `requirements.txt`

## Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the GUI

```bash
python gui_converter.py
```

### Basic Workflow

1. **Select Input File**:
   - Click the "Browse" button next to "Input File (.bin)"
   - Choose your ArduPilot binary log file
   - Output filename is automatically generated (same name with `.csv` extension)

2. **Modify Output Path (Optional)**:
   - Click the "Browse" button next to "Output File (.csv)"
   - Choose a custom output location or filename

3. **Configure Options (Optional)**:
   - **Separate by message type**: Creates separate CSV files for each message type
   - **Verbose output**: Shows detailed logging information

4. **View File Information (Optional)**:
   - Click "File Info" to see details about the selected binary file:
     - File size
     - Total message count
     - Message types available
     - Flight duration

5. **Convert File**:
   - Click "Convert" to start the conversion
   - Monitor progress in the Log Window
   - A success message will appear when complete

6. **Clear Log (Optional)**:
   - Click "Clear Log" to clear the log window

## GUI Components

### Input Fields

- **Input File (.bin)**: Path to the ArduPilot binary log file
- **Output File (.csv)**: Path where the CSV file will be saved

### Options

- **Separate by message type**: Creates individual CSV files for each message type found in the log
- **Verbose output**: Enables detailed logging output

### Buttons

- **Convert**: Starts the file conversion process
- **File Info**: Displays information about the selected binary file
- **Clear Log**: Clears the log window text

### Log Window

A scrollable text area showing:
- Conversion progress
- File information
- Error messages
- Status updates

### Status Bar

Shows the current operation status:
- "Ready" - Application idle
- "Converting..." - Conversion in progress
- "Conversion complete" - Successfully finished
- "Error reading file" - Error occurred

## Example Workflow

```
1. Launch application: python gui_converter.py
2. Click Browse (Input File) → select "flight.bin"
3. Output automatically set to "flight.csv"
4. (Optional) Click "File Info" to inspect the file
5. Click "Convert"
6. Wait for "Conversion complete" message
7. Find "flight.csv" in the same directory as "flight.bin"
```

## Troubleshooting

### Application Won't Start
- Ensure Python 3.6+ is installed
- Verify TKinter is available: `python -m tkinter`
- Check that all dependencies are installed: `pip install -r requirements.txt`

### Conversion Fails
- Check the Log Window for error details
- Verify the input file exists and is readable
- Ensure the output directory has write permissions
- Try with verbose logging enabled for more details

### No Log Output
- Logs appear in real-time in the Log Window
- Use "Clear Log" to remove old messages
- Enable "Verbose output" for more detailed logging

## Differences from CLI Version

| Feature | CLI | GUI |
|---------|-----|-----|
| File Selection | Command line arguments | File browser dialog |
| Batch Processing | Supported via glob patterns | Single file at a time |
| Output Control | Multiple options (-o, -d) | Single output path |
| Real-time Feedback | Console output | Log window with scrolling |
| Message Type Filtering | Supported (-m flag) | Not available in GUI version |
| List Types | Supported (--list-types) | Available via "File Info" |

## License

Same as the main project.

## Support

For issues or questions, refer to the main README.md or open an issue in the repository.
