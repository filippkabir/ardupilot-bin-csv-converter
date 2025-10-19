# GUI Updates - Output Directory Mode

## Summary of Changes

The GUI has been updated to work with **output directories** instead of individual output files. This provides more flexible batch processing and cleaner organization of output files.

---

## What Changed

### 1. Output Field Label
**Before:** "Output File (.csv)"  
**After:** "Output Directory"

### 2. Browse Button Behavior
**Before:** `filedialog.asksaveasfilename()` (file save dialog)  
**After:** `filedialog.askdirectory()` (directory selection dialog)

### 3. Auto-Generated Output Path
**Before:** Same directory as input file with `.csv` extension
```
Input:  /path/to/flight.bin
Output: /path/to/flight.csv
```

**After:** Creates a subdirectory in the input file's parent directory
```
Input:  /path/to/flight.bin
Output: /path/to/flight_csv_output/
```

### 4. File Naming in Output Directory

The naming of CSV files depends on the **"Separate by message type"** option:

#### Option A: Separate by Message Type = UNCHECKED (Default)
All messages combined into a single file with the input file's stem:
```
Input:  /path/to/flight.bin
Output Directory: /path/to/flight_csv_output/
Files Created:  /path/to/flight_csv_output/flight.csv
```

#### Option B: Separate by Message Type = CHECKED
Individual files created for each message type:
```
Input:  /path/to/flight.bin
Output Directory: /path/to/flight_csv_output/
Files Created:
  - /path/to/flight_csv_output/GPS.csv
  - /path/to/flight_csv_output/IMU.csv
  - /path/to/flight_csv_output/BARO.csv
  - /path/to/flight_csv_output/COMPASS.csv
  - /path/to/flight_csv_output/ARSPD.csv
  (... one file per message type found in the binary log)
```

---

## Workflow Examples

### Example 1: Basic Conversion (Combine All Messages)
```
1. Input File:    C:\Logs\flight.bin
2. Auto Output:   C:\Logs\flight_csv_output\
3. Separate:      ☐ (unchecked)
4. Click Convert
5. Result:        C:\Logs\flight_csv_output\flight.csv
                  (single file with all messages)
```

### Example 2: Separate by Message Type
```
1. Input File:    C:\Logs\flight.bin
2. Auto Output:   C:\Logs\flight_csv_output\
3. Separate:      ☑ (checked)
4. Click Convert
5. Result:        C:\Logs\flight_csv_output\
                  ├── GPS.csv
                  ├── IMU.csv
                  ├── BARO.csv
                  └── (more message types...)
                  (multiple files, one per message type)
```

### Example 3: Custom Output Directory
```
1. Input File:    C:\Logs\flight.bin
2. Auto Output:   C:\Logs\flight_csv_output\
3. Click Browse (Output Directory)
4. Select:        D:\ConvertedLogs\
5. Separate:      ☑ (checked)
6. Click Convert
7. Result:        D:\ConvertedLogs\
                  ├── GPS.csv
                  ├── IMU.csv
                  └── (more message types...)
```

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

## Success Notification

After conversion completes, you'll see:

```
✓ File converted successfully!
  Output files are in:
  C:\Logs\flight_csv_output
```

---

## Key Features

✅ **Automatic Output Subdirectory**
- Input file determines subdirectory name
- No manual path creation needed

✅ **Smart File Naming**
- Without "Separate by type": Uses input file stem (flight.csv)
- With "Separate by type": Uses message type names (GPS.csv, IMU.csv, etc.)

✅ **Flexible Path Selection**
- Auto-generated default path (recommended)
- Browse button to choose custom location

✅ **Clean Organization**
- All output files in one directory
- Easy to find and manage converted files

✅ **Proper Directory Creation**
- Creates output directory automatically if it doesn't exist
- No manual directory setup required

---

## Technical Implementation

### Method Changes

**`browse_input()`**
```python
# Now generates a subdirectory path:
# /path/to/{input_file_stem}_csv_output
output_dir = os.path.join(parent_dir, f'{base_name}_csv_output')
```

**`browse_output()`**
```python
# Changed from file save dialog to directory selection:
dir_path = filedialog.askdirectory(
    title='Select output directory for CSV files'
)
```

**`convert()`**
```python
# Passes directory path to converter instead of file path
success = self.converter.convert(input_file, output_dir, 
                               message_types, separate_by_type)
```

---

## Integration with Backend

The `BinToCsvConverter` class now receives:
- **input_file**: Path to .bin file
- **output_directory**: Path to output directory (not a file)
- **message_types**: None (for all types)
- **separate_by_type**: Boolean

The backend handles:
- Creating individual message type CSV files (if `separate_by_type=True`)
- Creating single combined CSV file (if `separate_by_type=False`)
- Naming files appropriately based on the mode

---

## Benefits

### For Users
- Cleaner, more organized output
- Less manual setup required
- Better for batch processing workflows

### For Data Organization
- Multiple related files in one directory
- Clear naming convention
- Easy to back up or archive output

### For Scripting
- Deterministic output location
- Predictable file naming patterns
- Easy to automate downstream processing

---

## Backwards Compatibility

**Note:** This change is **not backwards compatible** with the old file-based output system. The GUI now exclusively uses directories.

The CLI version (`bin2csv.py`) can still output to files if needed:
```bash
python bin2csv.py flight.bin -o flight.csv  # File output
python bin2csv.py flight.bin -d ./output/   # Directory output
```

---

## Common Questions

**Q: Can I still output to a single file?**  
A: No, the GUI now uses directories. For single file output, use the CLI version or place all files in a directory and work with them there.

**Q: What if the output directory already exists?**  
A: The converter creates it if needed and adds files to it. Existing files are not deleted.

**Q: How are file names determined?**  
A: Based on the "Separate by message type" checkbox:
- Unchecked: Uses input file name (e.g., "flight.csv")
- Checked: Uses message type name (e.g., "GPS.csv")

**Q: Can I specify a different subdirectory name?**  
A: Yes! Use the Browse button for the output directory to select any path you want.

**Q: What's the default subdirectory naming?**  
A: `{input_file_stem}_csv_output`

Example: If input is "flight.bin", default output is "flight_csv_output/"

---

## Testing the Changes

Try these workflows to verify:

1. **Basic conversion**: Click Browse input → select .bin → click Convert
2. **Custom output**: Click Browse input → select .bin → Click Browse output → select different directory → click Convert
3. **Separate by type**: Check the "Separate by message type" box before converting
4. **View results**: Navigate to the output directory to see the generated CSV files

---

*Last Updated: October 19, 2025*
