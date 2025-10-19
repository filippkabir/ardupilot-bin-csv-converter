#!/usr/bin/env python3
"""
Command-line interface for ArduPilot bin to CSV converter.

This script provides a command-line interface for converting ArduPilot binary 
log files (.bin) to CSV format.
"""

import os
import sys
import glob
import logging
import click
from typing import List, Optional
from src.converter import BinToCsvConverter


@click.command()
@click.argument('input_files', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('--output', '-o', 
              help='Output CSV file path (for single input) or directory (for multiple inputs)')
@click.option('--output-dir', '-d', 
              help='Output directory for CSV files (alternative to --output)')
@click.option('--message-types', '-m', multiple=True,
              help='Message types to include (can be specified multiple times)')
@click.option('--separate-by-type', '-s', is_flag=True,
              help='Create separate CSV files for each message type')
@click.option('--list-types', '-l', is_flag=True,
              help='List available message types and exit')
@click.option('--info', '-i', is_flag=True,
              help='Show file information and exit')
@click.option('--verbose', '-v', is_flag=True,
              help='Enable verbose logging')
@click.option('--quiet', '-q', is_flag=True,
              help='Suppress all output except errors')
def main(input_files: tuple, output: Optional[str], output_dir: Optional[str],
         message_types: tuple, separate_by_type: bool, list_types: bool,
         info: bool, verbose: bool, quiet: bool):
    """
    Convert ArduPilot binary log files (.bin) to CSV format.
    
    INPUT_FILES: One or more .bin files to convert. Supports glob patterns.
    
    Examples:
    \\b
        # Convert single file
        python bin2csv.py flight.bin -o flight.csv
        
        # Convert multiple files to directory
        python bin2csv.py *.bin -d ./csv_output/
        
        # Convert with specific message types
        python bin2csv.py flight.bin -o flight.csv -m GPS -m IMU
        
        # Create separate files for each message type
        python bin2csv.py flight.bin -d ./output/ --separate-by-type
        
        # List available message types
        python bin2csv.py flight.bin --list-types
    """
    # Set up logging
    if quiet:
        log_level = logging.ERROR
    elif verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s'
    )
    
    # Expand glob patterns in input files
    expanded_files = []
    for pattern in input_files:
        if '*' in pattern or '?' in pattern:
            matches = glob.glob(pattern)
            if matches:
                expanded_files.extend(matches)
            else:
                click.echo(f"Warning: No files match pattern '{pattern}'", err=True)
        else:
            expanded_files.append(pattern)
    
    if not expanded_files:
        click.echo("Error: No input files found", err=True)
        sys.exit(1)
    
    # Initialize converter
    converter = BinToCsvConverter(log_level)
    
    # Handle list-types option
    if list_types:
        for input_file in expanded_files:
            click.echo(f"\nMessage types in {input_file}:")
            try:
                msg_types = converter.get_available_message_types(input_file)
                if msg_types:
                    for msg_type in msg_types:
                        click.echo(f"  - {msg_type}")
                else:
                    click.echo("  No message types found")
            except Exception as e:
                click.echo(f"Error reading {input_file}: {e}", err=True)
        return
    
    # Handle info option
    if info:
        for input_file in expanded_files:
            click.echo(f"\nFile information for {input_file}:")
            try:
                summary = converter.get_file_summary(input_file)
                if summary:
                    click.echo(f"  Size: {summary.get('file_size', 0)} bytes")
                    if 'file_size_mb' in summary:
                        click.echo(f"        {summary['file_size_mb']} MB")
                    elif 'file_size_kb' in summary:
                        click.echo(f"        {summary['file_size_kb']} KB")
                    
                    click.echo(f"  Total messages: {summary.get('total_messages', 0)}")
                    click.echo(f"  Message types: {len(summary.get('message_types', []))}")
                    
                    if summary.get('duration', 0) > 0:
                        click.echo(f"  Duration: {summary['duration']:.1f} seconds")
                    
                    msg_types = summary.get('message_types', [])
                    if msg_types:
                        click.echo("  Available message types:")
                        for msg_type in msg_types:
                            click.echo(f"    - {msg_type}")
                else:
                    click.echo("  Unable to read file information")
            except Exception as e:
                click.echo(f"Error reading {input_file}: {e}", err=True)
        return
    
    # Determine output configuration
    if not output and not output_dir:
        if len(expanded_files) == 1:
            # Single file: generate output filename
            input_file = expanded_files[0]
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output = f"{base_name}.csv"
        else:
            # Multiple files: use current directory
            output_dir = "./csv_output"
    
    # Convert message_types tuple to list
    msg_types_list = list(message_types) if message_types else None
    
    try:
        if len(expanded_files) == 1 and output and not output_dir:
            # Single file conversion
            input_file = expanded_files[0]
            success = converter.convert(input_file, output, msg_types_list, separate_by_type)
            
            if success:
                if not quiet:
                    click.echo(f"Successfully converted {input_file} to {output}")
            else:
                click.echo(f"Failed to convert {input_file}", err=True)
                sys.exit(1)
        
        else:
            # Batch conversion
            target_dir = output_dir or output or "./csv_output"
            
            if not quiet:
                click.echo(f"Converting {len(expanded_files)} files to {target_dir}...")
            
            results = converter.batch_convert(expanded_files, target_dir, 
                                            msg_types_list, separate_by_type)
            
            successful = sum(1 for success in results.values() if success)
            failed = len(results) - successful
            
            if not quiet:
                click.echo(f"Conversion complete: {successful} successful, {failed} failed")
            
            if failed > 0:
                if verbose:
                    click.echo("Failed files:")
                    for file_path, success in results.items():
                        if not success:
                            click.echo(f"  - {file_path}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        click.echo("\nConversion cancelled by user", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error during conversion: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()