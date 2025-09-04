#!/usr/bin/env python3
"""
Prana Log September Files Merger Script
Merges all September prana log files and attachments into a comprehensive document
"""

import os
import glob
from datetime import datetime

def merge_september_files():
    """Merge all September prana log files and attachments"""
    
    # Define the source directory for September prana logs
    prana_sept_dir = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/prana_log/Sept"
    
    # Output file path
    output_file = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/tools/merged_september_pranalogs.md"
    
    # Find all relevant files
    txt_files = glob.glob(os.path.join(prana_sept_dir, "*.txt"))
    md_files = glob.glob(os.path.join(prana_sept_dir, "*.md"))
    py_files = glob.glob(os.path.join(prana_sept_dir, "*.py"))
    rtf_files = glob.glob(os.path.join(prana_sept_dir, "*.rtf"))
    
    all_files = txt_files + md_files + py_files + rtf_files
    
    print(f"Found {len(all_files)} files in September prana logs:")
    for file in sorted(all_files):
        filename = os.path.basename(file)
        file_size = os.path.getsize(file)
        if file_size > 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size} bytes"
        print(f"  - {filename} ({size_str})")
    
    # Create merged content
    merged_content = []
    
    # Header
    merged_content.append("# Comprehensive September Prana Log Merger")
    merged_content.append(f"# Merged on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    merged_content.append("")
    merged_content.append("This document contains all September prana log files and related documents.")
    merged_content.append("These files contain dialogues, observations, and processing logs from September 2025.")
    merged_content.append("")
    merged_content.append("=" * 80)
    merged_content.append("")
    
    # Process each file
    for i, file_path in enumerate(sorted(all_files), 1):
        filename = os.path.basename(file_path)
        file_extension = os.path.splitext(filename)[1].lower()
        print(f"Processing {filename}...")
        
        # Add file header
        merged_content.append(f"## Source File {i}: {filename}")
        merged_content.append(f"**File Path**: `{file_path}`")
        merged_content.append(f"**File Type**: {file_extension}")
        merged_content.append("")
        
        try:
            # Handle different file types
            if file_extension == '.rtf':
                # RTF files need special handling
                merged_content.append("**Note**: RTF file content (Rich Text Format)")
                merged_content.append("```rtf")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()[:5000]  # Limit RTF content to avoid overflow
                    merged_content.append(content)
                merged_content.append("```")
            elif file_extension in ['.txt', '.md', '.py']:
                # Regular text files
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if file_extension == '.py':
                    merged_content.append("```python")
                    merged_content.append(content)
                    merged_content.append("```")
                elif file_extension == '.md':
                    merged_content.append("### Markdown Content:")
                    merged_content.append(content)
                else:
                    merged_content.append("### Text Content:")
                    merged_content.append("```")
                    merged_content.append(content)
                    merged_content.append("```")
            
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
        
        print(f"\nSuccessfully merged {len(all_files)} files!")
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
        
        return output_file
        
    except Exception as e:
        print(f"Error writing merged file: {e}")
        return None

if __name__ == "__main__":
    output_path = merge_september_files()
    if output_path:
        print(f"\n✅ Merge completed successfully!")
        print(f"📁 File location: {output_path}")
    else:
        print("❌ Merge failed!")
