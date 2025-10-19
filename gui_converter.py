#!/usr/bin/env python3
"""
GUI interface for ArduPilot bin to CSV converter using TKinter.

This script provides a graphical user interface for converting ArduPilot binary 
log files (.bin) to CSV format.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import scrolledtext
import logging
import os
import sys
from pathlib import Path
from src.converter import BinToCsvConverter


class LogHandler(logging.Handler):
    """Custom logging handler to redirect logs to TKinter text widget."""
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
    
    def emit(self, record):
        """Emit a log record to the text widget."""
        log_message = self.format(record)
        self.text_widget.config(state='normal')
        self.text_widget.insert('end', log_message + '\n')
        self.text_widget.see('end')
        self.text_widget.config(state='disabled')
        self.text_widget.update()


class BinToCsvGUI:
    """GUI application for converting ArduPilot bin files to CSV."""
    
    def __init__(self, root):
        self.root = root
        self.root.title('ArduPilot Bin to CSV Converter')
        self.root.geometry('800x600')
        
        # Initialize converter
        self.converter = BinToCsvConverter(logging.INFO)
        
        # Setup logging
        self.setup_logging()
        
        # Create GUI elements
        self.create_widgets()
    
    def setup_logging(self):
        """Configure logging to display in the log window."""
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Format for logging
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        
        # Handler for log window (will be set after creating text widget)
        self.log_handler = None
        self.log_formatter = formatter
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding='10')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text='ArduPilot Bin to CSV Converter', 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Input file selection
        ttk.Label(main_frame, text='Input File (.bin):', font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        input_frame.columnconfigure(0, weight=1)
        
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.input_var)
        input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        input_btn = ttk.Button(input_frame, text='Browse', command=self.browse_input)
        input_btn.grid(row=0, column=1, padx=(5, 0))
        
        # Output directory selection
        ttk.Label(main_frame, text='Output Directory:', font=('Arial', 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var)
        output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        output_btn = ttk.Button(output_frame, text='Browse', command=self.browse_output)
        output_btn.grid(row=0, column=1, padx=(5, 0))
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text='Options', padding='10')
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        
        self.separate_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text='Separate by message type', 
                       variable=self.separate_var).grid(row=0, column=0, sticky=tk.W)
        
        self.verbose_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text='Verbose output', 
                       variable=self.verbose_var).grid(row=0, column=1, sticky=tk.W)
        
        # Log window label
        ttk.Label(main_frame, text='Log Window:', font=('Arial', 10)).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        # Log window (scrolled text widget)
        self.log_text = scrolledtext.ScrolledText(
            main_frame, height=15, width=80, state='disabled', font=('Courier', 9)
        )
        self.log_text.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Setup logging handler for the text widget
        self.log_handler = LogHandler(self.log_text)
        self.log_handler.setFormatter(self.log_formatter)
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.INFO)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        # Convert button
        self.convert_btn = ttk.Button(button_frame, text='Convert', command=self.convert)
        self.convert_btn.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))
        
        # Info button
        self.info_btn = ttk.Button(button_frame, text='File Info', command=self.show_info)
        self.info_btn.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        # Clear log button
        self.clear_btn = ttk.Button(button_frame, text='Clear Log', command=self.clear_log)
        self.clear_btn.grid(row=0, column=2, padx=5, sticky=(tk.W, tk.E))
        
        # Status bar
        self.status_var = tk.StringVar(value='Ready')
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief='sunken', anchor=tk.W)
        status_bar.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def browse_input(self):
        """Browse for input .bin file."""
        file_path = filedialog.askopenfilename(
            title='Select input .bin file',
            filetypes=[('Binary files', '*.bin'), ('All files', '*.*')]
        )
        if file_path:
            self.input_var.set(file_path)
            # Auto-generate output directory based on input file location
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            parent_dir = os.path.dirname(file_path)
            output_dir = os.path.join(parent_dir, f'{base_name}_csv_output')
            self.output_var.set(output_dir)
            logging.info(f'Selected input file: {file_path}')
            logging.info(f'Output directory set to: {output_dir}')
    
    def browse_output(self):
        """Browse for output directory."""
        dir_path = filedialog.askdirectory(
            title='Select output directory for CSV files'
        )
        if dir_path:
            self.output_var.set(dir_path)
            logging.info(f'Selected output directory: {dir_path}')
    
    def convert(self):
        """Perform the conversion."""
        input_file = self.input_var.get()
        output_dir = self.output_var.get()
        
        # Validate inputs
        if not input_file:
            messagebox.showerror('Error', 'Please select an input file')
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror('Error', f'Input file does not exist: {input_file}')
            return
        
        if not output_dir:
            messagebox.showerror('Error', 'Please specify an output directory')
            return
        
        # Update status
        self.status_var.set('Converting...')
        self.convert_btn.config(state='disabled')
        logging.info(f'Starting conversion...')
        logging.info(f'Input: {input_file}')
        logging.info(f'Output Directory: {output_dir}')
        
        try:
            # Create output directory if needed
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Perform conversion
            message_types = None
            separate_by_type = self.separate_var.get()
            
            success = self.converter.convert(input_file, output_dir, 
                                           message_types, separate_by_type)
            
            if success:
                logging.info(f'Successfully converted {input_file} to {output_dir}')
                self.status_var.set('Conversion complete')
                messagebox.showinfo('Success', f'File converted successfully!\nOutput files are in:\n{output_dir}')
            else:
                logging.error(f'Failed to convert {input_file}')
                self.status_var.set('Conversion failed')
                messagebox.showerror('Error', 'Conversion failed. Check the log for details.')
        
        except Exception as e:
            logging.error(f'Error during conversion: {e}')
            self.status_var.set('Error occurred')
            messagebox.showerror('Error', f'An error occurred:\n{str(e)}')
        
        finally:
            self.convert_btn.config(state='normal')
    
    def show_info(self):
        """Show file information."""
        input_file = self.input_var.get()
        
        if not input_file:
            messagebox.showerror('Error', 'Please select an input file')
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror('Error', f'Input file does not exist: {input_file}')
            return
        
        self.status_var.set('Reading file information...')
        self.info_btn.config(state='disabled')
        
        try:
            logging.info(f'Reading information from {input_file}...')
            summary = self.converter.get_file_summary(input_file)
            
            if summary:
                logging.info(f'File information:')
                logging.info(f'  Size: {summary.get("file_size", 0)} bytes')
                if 'file_size_mb' in summary:
                    logging.info(f'        {summary["file_size_mb"]} MB')
                elif 'file_size_kb' in summary:
                    logging.info(f'        {summary["file_size_kb"]} KB')
                
                logging.info(f'  Total messages: {summary.get("total_messages", 0)}')
                logging.info(f'  Message types: {len(summary.get("message_types", []))}')
                
                if summary.get('duration', 0) > 0:
                    logging.info(f'  Duration: {summary["duration"]:.1f} seconds')
                
                msg_types = summary.get('message_types', [])
                if msg_types:
                    logging.info('  Available message types:')
                    for msg_type in msg_types:
                        logging.info(f'    - {msg_type}')
                
                self.status_var.set('File information displayed')
            else:
                logging.error('Unable to read file information')
                self.status_var.set('Error reading file')
        
        except Exception as e:
            logging.error(f'Error reading file information: {e}')
            self.status_var.set('Error occurred')
        
        finally:
            self.info_btn.config(state='normal')
    
    def clear_log(self):
        """Clear the log window."""
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state='disabled')
        logging.info('Log cleared')


def main():
    """Main function to start the GUI application."""
    root = tk.Tk()
    app = BinToCsvGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
