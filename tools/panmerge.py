#!/usr/bin/env python3
"""
Chat Files Merger Script
Merges all extracted ChatGPT conversation files in the current directory
"""

import os
import glob
from datetime import datetime

def merge_extracted_chat_files():
    """Merge all extracted chat files into a comprehensive document"""
    
    # Define the source directory as current working directory
    source_dir = os.getcwd()
    
    # Output file path in current directory
    output_file = os.path.join(source_dir, "merged_extracted_conversations.md")
    
    # Find all extracted markdown files
    pattern = os.path.join(source_dir, "*_extracted.md")
    extracted_files = glob.glob(pattern)
    
    print(f"Found {len(extracted_files)} extracted chat files:")
    for file in extracted_files:
        print(f"  - {os.path.basename(file)}")
    
    # Create merged content
    merged_content = []
    
    # Header
    merged_content.append("# Comprehensive Merged ChatGPT Conversations")
    merged_content.append(f"# Merged on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    merged_content.append("")
    merged_content.append("This document contains all extracted ChatGPT conversations in the current directory.")
    merged_content.append("")
    merged_content.append("=" * 80)
    merged_content.append("")
    
    # Process each file
    for i, file_path in enumerate(sorted(extracted_files), 1):
        filename = os.path.basename(file_path)
        print(f"Processing {filename}...")
        
        # Add file header
        merged_content.append(f"## Source File {i}: {filename}")
        merged_content.append(f"**File Path**: `{file_path}`")
        merged_content.append("")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Add the content
            merged_content.append(content)
            merged_content.append("")
            merged_content.append("=" * 80)
            merged_content.append("")
            
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            merged_content.append(f"**ERROR**: Could not read file - {e}")
            merged_content.append("")
            merged_content.append("=" * 80)
            merged_content.append("")
    
    # Write merged file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(merged_content))
        
        print(f"\nSuccessfully merged {len(extracted_files)} files!")
        print(f"Output saved to: {output_file}")
        
        # Get file size
        file_size = os.path.getsize(output_file)
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        elif file_size > 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{file_size} bytes"
        
        print(f"Merged file size: {size_str}")
        
    except Exception as e:
        print(f"Error writing merged file: {e}")

if __name__ == "__main__":
    merge_extracted_chat_files()