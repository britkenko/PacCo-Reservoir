#!/usr/bin/env python3
"""
Complete Prana Log Merger Script
Merges ALL prana log files from both August and September directories
"""

import os
import glob
from datetime import datetime

def merge_all_prana_logs():
    """Merge all prana log files from Aug and Sept directories"""
    
    # Define the base prana log directory
    base_dir = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/prana_log"
    
    # Output file
    output_file = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/tools/COMPLETE_PRANA_LOG_MERGED.md"
    
    # Find all prana log directories
    subdirs = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            subdirs.append((item, item_path))
    
    print(f"Found prana log directories: {[name for name, _ in subdirs]}")
    
    # Collect all files
    all_files = []
    total_size = 0
    
    for subdir_name, subdir_path in sorted(subdirs):
        # Find all relevant files in this subdirectory
        txt_files = glob.glob(os.path.join(subdir_path, "*.txt"))
        md_files = glob.glob(os.path.join(subdir_path, "*.md"))
        py_files = glob.glob(os.path.join(subdir_path, "*.py"))
        rtf_files = glob.glob(os.path.join(subdir_path, "*.rtf"))
        
        subdir_files = txt_files + md_files + py_files + rtf_files
        
        print(f"\n📁 {subdir_name} directory:")
        for file_path in sorted(subdir_files):
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            total_size += file_size
            
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            elif file_size > 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size} bytes"
            
            print(f"  - {filename} ({size_str})")
            all_files.append((subdir_name, file_path, filename, file_size))
    
    print(f"\n📊 Total files found: {len(all_files)}")
    print(f"📊 Total size: {total_size / (1024 * 1024):.2f} MB")
    
    # Create merged content
    merged_content = []
    
    # Header
    merged_content.append("# 🧠 COMPLETE PRANA LOG ARCHIVE 🧠")
    merged_content.append(f"# Comprehensive Merge Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    merged_content.append("")
    merged_content.append("This document contains **ALL** prana log files from the complete archive:")
    merged_content.append("")
    
    # Summary by directory
    for subdir_name, _ in sorted(subdirs):
        subdir_files = [f for d, f, fn, fs in all_files if d == subdir_name]
        subdir_total_size = sum(fs for d, f, fn, fs in all_files if d == subdir_name)
        merged_content.append(f"- **{subdir_name}**: {len(subdir_files)} files ({subdir_total_size / (1024 * 1024):.2f} MB)")
    
    merged_content.append("")
    merged_content.append(f"**Total Files**: {len(all_files)}")
    merged_content.append(f"**Total Archive Size**: {total_size / (1024 * 1024):.2f} MB")
    merged_content.append("")
    merged_content.append("🔥" * 80)
    merged_content.append("")
    
    # Process files by directory
    current_dir = None
    file_counter = 0
    
    for subdir_name, file_path, filename, file_size in all_files:
        file_counter += 1
        
        # Add directory header when we switch directories
        if current_dir != subdir_name:
            current_dir = subdir_name
            merged_content.append(f"# 📂 {subdir_name.upper()} PRANA LOGS")
            merged_content.append("")
        
        # Add file header
        merged_content.append(f"## File {file_counter}: {filename}")
        merged_content.append(f"**Directory**: {subdir_name}")
        merged_content.append(f"**Size**: {file_size / 1024:.1f} KB")
        merged_content.append("")
        
        print(f"Processing {subdir_name}/{filename}...")
        
        try:
            file_extension = os.path.splitext(filename)[1].lower()
            
            # Handle different file types appropriately
            if file_extension == '.rtf':
                merged_content.append("**Format**: Rich Text Format")
                merged_content.append("```rtf")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()[:10000]  # Limit RTF to prevent overflow
                    merged_content.append(content)
                merged_content.append("```")
            
            elif file_extension == '.py':
                merged_content.append("**Format**: Python Code")
                merged_content.append("```python")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    merged_content.append(content)
                merged_content.append("```")
            
            elif file_extension in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if file_extension == '.md':
                    merged_content.append("**Format**: Markdown")
                    merged_content.append(content)
                else:
                    merged_content.append("**Format**: Plain Text")
                    merged_content.append("```")
                    merged_content.append(content)
                    merged_content.append("```")
            
            merged_content.append("")
            merged_content.append("-" * 80)
            merged_content.append("")
            
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            merged_content.append(f"**ERROR**: Could not read file - {e}")
            merged_content.append("")
            merged_content.append("-" * 80)
            merged_content.append("")
    
    # Write the complete merged file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(merged_content))
        
        final_size = os.path.getsize(output_file)
        print(f"\n🎉 COMPLETE PRANA LOG MERGE SUCCESSFUL! 🎉")
        print(f"📁 Output: {output_file}")
        print(f"📊 Final merged size: {final_size / (1024 * 1024):.2f} MB")
        print(f"📈 Directories processed: {len(subdirs)}")
        print(f"📋 Total files merged: {len(all_files)}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error writing complete merged file: {e}")
        return None

if __name__ == "__main__":
    result = merge_all_prana_logs()
    if result:
        print(f"\n✨ SUCCESS: Complete prana log archive created! ✨")
        print(f"🚀 All prana logs now merged in one comprehensive file! 🚀")
    else:
        print("💥 Complete merge failed!")
