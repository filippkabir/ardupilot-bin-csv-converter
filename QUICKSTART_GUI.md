# Quick Start Guide - GUI Converter

## 30-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the GUI
python gui_converter.py
```

## 5-Minute First Use

1. **Start the application**
   ```bash
   python gui_converter.py
   ```
   A window titled "ArduPilot Bin to CSV Converter" will appear.

2. **Select your .bin file**
   - Click "Browse" next to "Input File (.bin)"
   - Navigate to and select your ArduPilot binary log file
   - The output filename is automatically set to match your input (with .csv extension)

3. **Click "Convert"**
   - Watch the Log Window for progress
   - You'll see a success message when done

4. **Find your CSV file**
   - It's saved in the same location as your .bin file by default
   - Or check the "Output File (.csv)" path shown in the GUI

## Common Tasks

### Check File Before Converting
1. Select your .bin file via "Browse"
2. Click "File Info" to see:
   - File size
   - Number of messages
   - Available message types
   - Flight duration

### Change Output Location
1. Click "Browse" next to "Output File (.csv)"
2. Navigate to desired folder
3. Enter a filename (or keep the suggested name)
4. Click "Convert"

### Separate by Message Type
1. Check the box: "Separate by message type"
2. Click "Convert"
3. You'll get individual CSV files for each message type

### See Detailed Logs
1. Check the box: "Verbose output"
2. Click "Convert"
3. The Log Window shows detailed information

## Keyboard Shortcuts

| Action | Method |
|--------|--------|
| Browse Input | Click "Browse" button next to input field |
| Browse Output | Click "Browse" button next to output field |
| Start Conversion | Click "Convert" or press Enter |
| View File Info | Click "File Info" |
| Clear Log | Click "Clear Log" |

## Troubleshooting

**"Module not found" error?**
```bash
pip install -r requirements.txt
```

**GUI won't open?**
```bash
# Check TKinter is installed
python -m tkinter
```

**Conversion fails?**
- Check the Log Window for details
- Ensure input file exists and you have read permission
- Try with "Verbose output" enabled

**Want more control?**
- Use the CLI version: `python bin2csv.py --help`

## Next Steps

- Read `GUI_README.md` for detailed documentation
- Check `README.md` for the original CLI version
- See `examples/` folder for sample workflows

## Still Need Help?

1. Check the Log Window - it shows detailed error messages
2. Review `GUI_README.md` Troubleshooting section
3. Look at the main `README.md` for background information
