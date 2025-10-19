"""
Binary file parser for ArduPilot log files.

This module handles the parsing of ArduPilot binary log files (.bin) using pymavlink.
"""

import os
import logging
from typing import Generator, Dict, Any, Optional
from pymavlink import mavutil


class BinFileParser:
    """Parser for ArduPilot binary log files."""
    
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize the parser.
        
        Args:
            log_level: Logging level for parser operations
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        # Create console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def validate_bin_file(self, file_path: str) -> bool:
        """
        Validate if the file is a valid ArduPilot binary log file.
        
        Args:
            file_path: Path to the .bin file
            
        Returns:
            True if valid, False otherwise
        """
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return False
            
        if not file_path.lower().endswith('.bin'):
            self.logger.warning(f"File does not have .bin extension: {file_path}")
            
        try:
            # Try to open the file with mavutil
            mlog = mavutil.mavlink_connection(file_path)
            # Try to read first message to validate format
            msg = mlog.recv_match()
            if msg is None:
                self.logger.error(f"No valid messages found in file: {file_path}")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error validating file {file_path}: {e}")
            return False
    
    def parse_messages(self, file_path: str, message_types: Optional[list] = None) -> Generator[Dict[str, Any], None, None]:
        """
        Parse messages from a binary log file.
        
        Args:
            file_path: Path to the .bin file
            message_types: List of message types to filter (None for all types)
            
        Yields:
            Dictionary containing message data
        """
        if not self.validate_bin_file(file_path):
            raise ValueError(f"Invalid binary log file: {file_path}")
        
        self.logger.info(f"Starting to parse file: {file_path}")
        
        try:
            mlog = mavutil.mavlink_connection(file_path)
            message_count = 0
            
            while True:
                msg = mlog.recv_match(type=message_types)
                if msg is None:
                    break
                
                message_count += 1
                
                # Convert message to dictionary
                msg_dict = {
                    'timestamp': getattr(msg, '_timestamp', 0),
                    'message_type': msg.get_type(),
                }
                
                # Add all message fields
                for field in msg.get_fieldnames():
                    try:
                        msg_dict[field] = getattr(msg, field)
                    except AttributeError:
                        msg_dict[field] = None
                
                yield msg_dict
            
            self.logger.info(f"Parsed {message_count} messages from {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error parsing file {file_path}: {e}")
            raise
    
    def get_message_types(self, file_path: str) -> set:
        """
        Get all unique message types in the binary log file.
        
        Args:
            file_path: Path to the .bin file
            
        Returns:
            Set of unique message types
        """
        message_types = set()
        
        try:
            for message in self.parse_messages(file_path):
                message_types.add(message['message_type'])
        except Exception as e:
            self.logger.error(f"Error getting message types from {file_path}: {e}")
            raise
        
        return message_types
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get information about the binary log file.
        
        Args:
            file_path: Path to the .bin file
            
        Returns:
            Dictionary with file information
        """
        info = {
            'file_path': file_path,
            'file_size': 0,
            'message_types': set(),
            'total_messages': 0,
            'duration': 0,
            'start_time': None,
            'end_time': None
        }
        
        if not os.path.exists(file_path):
            return info
        
        info['file_size'] = os.path.getsize(file_path)
        
        try:
            first_timestamp = None
            last_timestamp = None
            
            for message in self.parse_messages(file_path):
                info['message_types'].add(message['message_type'])
                info['total_messages'] += 1
                
                timestamp = message.get('timestamp', 0)
                if timestamp > 0:
                    if first_timestamp is None:
                        first_timestamp = timestamp
                    last_timestamp = timestamp
            
            if first_timestamp and last_timestamp:
                info['start_time'] = first_timestamp
                info['end_time'] = last_timestamp
                info['duration'] = last_timestamp - first_timestamp
                
        except Exception as e:
            self.logger.error(f"Error getting file info for {file_path}: {e}")
        
        return info