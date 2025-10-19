#!/usr/bin/env python3
"""
Example usage of the ArduPilot Bin to CSV Converter.

This script demonstrates how to use the converter programmatically.
"""

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the path so we can import the src module
sys.path.append(str(Path(__file__).parent.parent))

from src.converter import BinToCsvConverter


def main():
    """
    Demonstrate basic usage of the BinToCsvConverter class.
    """
    # Configure logging to see what's happening
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    print("ArduPilot Bin to CSV Converter - Example Usage")
    print("=" * 50)
    
    # Replace this with the path to your actual .bin file
    sample_bin_file = "sample_flight.bin"  # You need to provide this file
    
    # Check if sample file exists
    if not os.path.exists(sample_bin_file):
        print(f"Sample file '{sample_bin_file}' not found.")
        print("Please place a .bin file in this directory or update the file path.")
        print("\\nTo test this example:")
        print("1. Copy an ArduPilot .bin file to this directory")
        print("2. Rename it to 'sample_flight.bin' or update the path in this script")
        return
    
    # Initialize the converter
    converter = BinToCsvConverter()
    
    try:
        print(f"\\n1. Getting file information...")
        summary = converter.get_file_summary(sample_bin_file)
        
        if summary:
            print(f"   File size: {summary.get('file_size', 0)} bytes")
            if 'file_size_mb' in summary:
                print(f"   File size: {summary['file_size_mb']} MB")
            
            print(f"   Total messages: {summary.get('total_messages', 0)}")
            print(f"   Message types: {len(summary.get('message_types', []))}")
            
            if summary.get('duration', 0) > 0:
                print(f"   Duration: {summary['duration']:.1f} seconds")
        
        print(f"\\n2. Getting available message types...")
        message_types = converter.get_available_message_types(sample_bin_file)
        
        if message_types:
            print(f"   Found {len(message_types)} message types:")
            for i, msg_type in enumerate(message_types[:10]):  # Show first 10
                print(f"      - {msg_type}")
            if len(message_types) > 10:
                print(f"      ... and {len(message_types) - 10} more")
        else:
            print("   No message types found")
        
        print(f"\\n3. Converting entire file to CSV...")
        output_file = "sample_flight_all.csv"
        success = converter.convert(sample_bin_file, output_file)
        
        if success:
            print(f"   ✓ Successfully converted to {output_file}")
            
            # Check the output file
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"   Output file size: {file_size} bytes")
        else:
            print(f"   ✗ Conversion failed")
        
        print(f"\\n4. Converting specific message types...")
        # Convert only GPS and IMU data (common message types)
        specific_types = []
        for msg_type in message_types:
            if 'GPS' in msg_type or 'IMU' in msg_type or 'ATT' in msg_type:
                specific_types.append(msg_type)
                if len(specific_types) >= 3:  # Limit to first 3 matches
                    break
        
        if specific_types:
            output_file_specific = "sample_flight_specific.csv"
            success = converter.convert(
                sample_bin_file, 
                output_file_specific,
                message_types=specific_types
            )
            
            if success:
                print(f"   ✓ Successfully converted {len(specific_types)} message types to {output_file_specific}")
                print(f"     Message types: {', '.join(specific_types)}")
            else:
                print(f"   ✗ Specific types conversion failed")
        else:
            print("   No GPS/IMU message types found for specific conversion")
        
        print(f"\\n5. Converting to separate files by message type...")
        output_base = "sample_flight_separated"
        success = converter.convert(
            sample_bin_file,
            output_base,
            separate_by_type=True
        )
        
        if success:
            print(f"   ✓ Successfully created separate CSV files")
            # List the created files
            for file in os.listdir('.'):
                if file.startswith('sample_flight_separated_') and file.endswith('.csv'):
                    file_size = os.path.getsize(file)
                    print(f"     - {file} ({file_size} bytes)")
        else:
            print(f"   ✗ Separate files conversion failed")
        
        print(f"\\n6. Batch conversion example...")
        # This would work if you had multiple .bin files
        bin_files = [f for f in os.listdir('.') if f.endswith('.bin')]
        
        if len(bin_files) > 1:
            results = converter.batch_convert(bin_files, './batch_output/')
            successful = sum(1 for success in results.values() if success)
            print(f"   ✓ Batch conversion: {successful}/{len(bin_files)} files successful")
        else:
            print(f"   Only one .bin file found, skipping batch conversion demo")
        
        print(f"\\n✓ Example completed successfully!")
        print(f"\\nCheck the current directory for output files:")
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        for csv_file in csv_files:
            print(f"   - {csv_file}")
            
    except Exception as e:
        print(f"\\n✗ Error during example execution: {e}")
        logging.exception("Detailed error information:")


if __name__ == '__main__':
    main()