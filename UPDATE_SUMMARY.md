# GUI Update Summary - Output Directory Support

**Date:** October 19, 2025  
**Version:** 2.0  
**Status:** Complete ✅

---

## What Changed

The GUI has been updated to use **output directories** instead of output files, with smart naming based on the "Separate by message type" option.

### Changes Made

1. **Output Field**
   - Changed from: "Output File (.csv)"
   - Changed to: "Output Directory"

2. **Browse Button Behavior**
   - Changed from: File save dialog (`asksaveasfilename`)
   - Changed to: Directory selection dialog (`askdirectory`)

3. **Auto-Generated Path**
   - Changed from: `{same_dir}/{filename}.csv`
   - Changed to: `{same_dir}/{filename_stem}_csv_output/`

4. **Output File Naming**
   - **When "Separate by message type" is UNCHECKED:**
     - Creates: `{filename_stem}.csv` in the output directory
     - Example: `flight.csv` contains all messages
   
   - **When "Separate by message type" is CHECKED:**
     - Creates: `{MESSAGE_TYPE}.csv` for each message type
     - Example: `GPS.csv`, `IMU.csv`, `BARO.csv`, etc.

---

## Key Features

✅ **Smart Default Paths**
- Input: `/path/to/flight.bin`
- Output: `/path/to/flight_csv_output/`
- Naming follows the input file stem

✅ **Flexible File Organization**
- All output files in one directory
- Easy to manage and organize conversions

✅ **Dual Output Modes**
- **Combined Mode** (default): Single CSV with all messages
- **Separated Mode**: Individual CSVs for each message type

✅ **User Control**
- Auto-generated default path
- Browse button to choose custom location
- Option to change output directory before converting

---

## Usage Examples

### Example 1: Basic Conversion (Default)
```
Input:     C:\Logs\flight.bin
Output:    C:\Logs\flight_csv_output\
Separate:  ☐ (unchecked)
Result:    C:\Logs\flight_csv_output\flight.csv
```

### Example 2: Separate by Message Type
```
Input:     C:\Logs\flight.bin
Output:    C:\Logs\flight_csv_output\
Separate:  ☑ (checked)
Result:    C:\Logs\flight_csv_output\
           ├── GPS.csv
           ├── IMU.csv
           ├── BARO.csv
           └── (other message types)
```

### Example 3: Custom Output Directory
```
Input:     C:\Logs\flight.bin
Output:    D:\MyOutputs\  (custom location)
Separate:  ☑ (checked)
Result:    D:\MyOutputs\
           ├── GPS.csv
           ├── IMU.csv
           └── (other message types)
```

---

## Technical Details

### Modified Methods

**`browse_input()`**
```python
# Auto-generates output directory based on input file
base_name = os.path.splitext(os.path.basename(file_path))[0]
output_dir = os.path.join(parent_dir, f'{base_name}_csv_output')
```

**`browse_output()`**
```python
# Changed to directory selection instead of file save
dir_path = filedialog.askdirectory(
    title='Select output directory for CSV files'
)
```

**`convert()`**
```python
# Passes directory to converter
success = self.converter.convert(input_file, output_dir, 
                               message_types, separate_by_type)
```

### Converter Integration

The `BinToCsvConverter` receives:
- `input_file`: Path to .bin file
- `output_directory`: Path to directory (not a file)
- `message_types`: None (all types)
- `separate_by_type`: Boolean flag

The converter handles:
- Creating the output directory if it doesn't exist
- Naming files appropriately based on `separate_by_type`
- Organizing output files logically

---

## Log Messages

The log window now shows directory-related information:

```
INFO: Selected input file: C:\Logs\flight.bin
INFO: Output directory set to: C:\Logs\flight_csv_output
INFO: Starting conversion...
INFO: Input: C:\Logs\flight.bin
INFO: Output Directory: C:\Logs\flight_csv_output
INFO: Successfully converted C:\Logs\flight.bin to C:\Logs\flight_csv_output
```

---

## GUI Layout (Updated)

```
┌──────────────────────────────────────────────────┐
│  ArduPilot Bin to CSV Converter                  │
├──────────────────────────────────────────────────┤
│ Input File (.bin):   [path] [Browse]             │
│ Output Directory:    [path] [Browse]   ← Changed │
│ ┌─ Options ──────────────────────────────────┐   │
│ │ ☐ Separate by type   ☐ Verbose output   │   │
│ └────────────────────────────────────────────┘   │
│ Log Window:                                      │
│ [Log messages appear here...]                    │
│ [Convert] [File Info] [Clear Log]                │
│ Status: Ready                                    │
└──────────────────────────────────────────────────┘
```

---

## File Structure After Conversion

### Single File Mode (No Separate)
```
Before:
  D:\Logs\flight.bin

After:
  D:\Logs\flight.bin
  D:\Logs\flight_csv_output\
  └── flight.csv
```

### Separate Mode
```
Before:
  D:\Logs\flight.bin

After:
  D:\Logs\flight.bin
  D:\Logs\flight_csv_output\
  ├── GPS.csv
  ├── IMU.csv
  ├── BARO.csv
  ├── COMPASS.csv
  └── ARSPD.csv
```

---

## Quick Start

1. **Run the GUI:**
   ```bash
   python gui_converter.py
   ```

2. **Select Input File:**
   - Click "Browse" next to "Input File (.bin)"
   - Select your .bin file
   - Output directory auto-fills

3. **Choose Output Mode:**
   - Leave "Separate by type" unchecked for single combined file
   - Check "Separate by type" for individual files per message type

4. **Convert:**
   - Click "Convert"
   - Wait for success message
   - Check the output directory for files

---

## Benefits

### For Users
- ✅ Cleaner file organization
- ✅ Less manual path management
- ✅ Clear visual directory selection
- ✅ Smart default naming

### For Data Management
- ✅ Multiple related files in one location
- ✅ Consistent naming patterns
- ✅ Easy to archive or backup

### For Processing
- ✅ Organized output ready for downstream tools
- ✅ Predictable file locations
- ✅ Scalable for batch operations

---

## Documentation Files

- **`GUI_CHANGES.md`** - Detailed explanation of all changes
- **`GUI_CHANGES_VISUAL.txt`** - Visual comparison and examples
- **`UPDATE_SUMMARY.md`** - This file (quick overview)

---

## Testing Checklist

- [x] Output field renamed to "Output Directory"
- [x] Browse button opens directory selector
- [x] Auto-generated path uses `{stem}_csv_output` format
- [x] File naming works correctly in both modes
- [x] Log messages show directory info
- [x] Success dialog shows output directory
- [x] Directory created automatically if needed
- [x] No linting errors
- [x] Production ready

---

## Files Modified

- `gui_converter.py` - Updated GUI application (320 lines)

## Files Created

- `GUI_CHANGES.md` - Detailed change documentation
- `GUI_CHANGES_VISUAL.txt` - Visual guides and examples
- `UPDATE_SUMMARY.md` - This summary

---

## Backward Compatibility

⚠️ **Note:** This is a **breaking change** from the previous file-based system.

- **GUI:** Now exclusively uses directories
- **CLI:** Still supports both file and directory modes (unchanged)
  ```bash
  python bin2csv.py flight.bin -o flight.csv      # File output
  python bin2csv.py flight.bin -d ./output/        # Directory output
  ```

---

## Status

✅ **Complete and Ready to Use**

- All changes implemented
- Tested and verified
- No linting errors
- Documentation complete
- Ready for production use

---

## Next Steps

1. **Try it out:**
   ```bash
   python gui_converter.py
   ```

2. **Read detailed documentation:**
   - `GUI_CHANGES.md` for full details
   - `GUI_CHANGES_VISUAL.txt` for examples

3. **Use the features:**
   - Explore both output modes
   - Try custom directories
   - Check the log window for details

---

**Created:** October 19, 2025  
**Version:** 2.0  
**Status:** Production Ready ✨
