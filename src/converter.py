"""
Main converter module for ArduPilot bin to CSV conversion.

This module provides the BinToCsvConverter class for converting ArduPilot binary
log files to CSV format.
"""

import os
import logging
import pandas as pd
from typing import Dict, List, Optional, Any
from .parser import BinFileParser


class BinToCsvConverter:
    """Main converter class for ArduPilot bin to CSV conversion."""
    
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize the converter.
        
        Args:
            log_level: Logging level for converter operations
        """
        self.parser = BinFileParser(log_level)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        # Create console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def convert(self, input_path: str, output_path: str, 
                message_types: Optional[List[str]] = None,
                separate_by_type: bool = False) -> bool:
        """
        Convert a binary log file to CSV format.
        
        Args:
            input_path: Path to input .bin file
            output_path: Path to output .csv file
            message_types: List of message types to include (None for all)
            separate_by_type: If True, create separate CSV files for each message type
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            self.logger.info(f"Converting {input_path} to {output_path}")
            
            if separate_by_type:
                return self._convert_separate_files(input_path, output_path, message_types)
            else:
                return self._convert_single_file(input_path, output_path, message_types)
                
        except Exception as e:
            self.logger.error(f"Error during conversion: {e}")
            return False
    
    def _convert_single_file(self, input_path: str, output_path: str, 
                           message_types: Optional[List[str]] = None) -> bool:
        """
        Convert binary log to a single CSV file.
        
        Args:
            input_path: Path to input .bin file or output directory
            output_path: Path to output .csv file or directory
            message_types: List of message types to include
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Determine if output_path is a directory or file
            if os.path.isdir(output_path) or (not os.path.exists(output_path) and output_path.endswith(os.sep)):
                # It's a directory - derive filename from input
                output_dir = output_path
                input_stem = os.path.splitext(os.path.basename(input_path))[0]
                output_file = os.path.join(output_dir, f"{input_stem}.csv")
            else:
                # It's a file path
                output_dir = os.path.dirname(output_path)
                output_file = output_path
            
            # Collect all messages
            messages = []
            for message in self.parser.parse_messages(input_path, message_types):
                messages.append(message)
            
            if not messages:
                self.logger.warning(f"No messages found in {input_path}")
                return False
            
            # Create DataFrame and save to CSV
            df = pd.DataFrame(messages)
            
            # Ensure output directory exists
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            df.to_csv(output_file, index=False)
            self.logger.info(f"Successfully saved {len(messages)} messages to {output_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in single file conversion: {e}")
            return False
    
    def _convert_separate_files(self, input_path: str, output_base: str, 
                              message_types: Optional[List[str]] = None) -> bool:
        """
        Convert binary log to separate CSV files by message type.
        
        Args:
            input_path: Path to input .bin file
            output_base: Output directory path for separate files
            message_types: List of message types to include
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure output_base is treated as a directory
            output_dir = output_base
            
            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Group messages by type
            messages_by_type = {}
            
            for message in self.parser.parse_messages(input_path, message_types):
                msg_type = message['message_type']
                if msg_type not in messages_by_type:
                    messages_by_type[msg_type] = []
                messages_by_type[msg_type].append(message)
            
            if not messages_by_type:
                self.logger.warning(f"No messages found in {input_path}")
                return False
            
            # Save each message type to separate file in the output directory
            for msg_type, messages in messages_by_type.items():
                df = pd.DataFrame(messages)
                output_file = os.path.join(output_dir, f"{msg_type}.csv")
                df.to_csv(output_file, index=False)
                self.logger.info(f"Saved {len(messages)} {msg_type} messages to {output_file}")
            
            self.logger.info(f"Successfully converted {input_path} to {len(messages_by_type)} separate CSV files in {output_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in separate files conversion: {e}")
            return False
    
    def get_available_message_types(self, input_path: str) -> List[str]:
        """
        Get list of available message types in the binary log file.
        
        Args:
            input_path: Path to input .bin file
            
        Returns:
            List of available message types
        """
        try:
            message_types = self.parser.get_message_types(input_path)
            return sorted(list(message_types))
        except Exception as e:
            self.logger.error(f"Error getting message types: {e}")
            return []
    
    def get_file_summary(self, input_path: str) -> Dict[str, Any]:
        """
        Get summary information about the binary log file.
        
        Args:
            input_path: Path to input .bin file
            
        Returns:
            Dictionary with file summary
        """
        try:
            info = self.parser.get_file_info(input_path)
            
            # Convert set to list for JSON serialization
            info['message_types'] = sorted(list(info['message_types']))
            
            # Add human-readable file size
            size_bytes = info['file_size']
            if size_bytes >= 1024*1024:
                info['file_size_mb'] = round(size_bytes / (1024*1024), 2)
            elif size_bytes >= 1024:
                info['file_size_kb'] = round(size_bytes / 1024, 2)
            
            # Add duration in human-readable format
            if info['duration'] > 0:
                duration_sec = info['duration']
                if duration_sec >= 3600:
                    info['duration_hours'] = round(duration_sec / 3600, 2)
                elif duration_sec >= 60:
                    info['duration_minutes'] = round(duration_sec / 60, 2)
                else:
                    info['duration_seconds'] = round(duration_sec, 2)
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting file summary: {e}")
            return {}
    
    def batch_convert(self, input_files: List[str], output_dir: str, 
                     message_types: Optional[List[str]] = None,
                     separate_by_type: bool = False) -> Dict[str, bool]:
        """
        Convert multiple binary log files to CSV format.
        
        Args:
            input_files: List of input .bin file paths
            output_dir: Directory for output CSV files
            message_types: List of message types to include
            separate_by_type: If True, create separate CSV files for each message type
            
        Returns:
            Dictionary mapping input file to conversion success status
        """
        results = {}
        
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for input_file in input_files:
            try:
                # Generate output filename
                base_name = os.path.splitext(os.path.basename(input_file))[0]
                output_path = os.path.join(output_dir, f"{base_name}.csv")
                
                # Convert file
                success = self.convert(input_file, output_path, message_types, separate_by_type)
                results[input_file] = success
                
            except Exception as e:
                self.logger.error(f"Error processing {input_file}: {e}")
                results[input_file] = False
        
        successful = sum(1 for success in results.values() if success)
        self.logger.info(f"Batch conversion complete: {successful}/{len(input_files)} files successful")
        
        return results
