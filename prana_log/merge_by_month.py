#!/usr/bin/env python3
"""
Prana Log Monthly Merger
Merges all prana log files by month and cleans up individual files
"""

import os
import glob
from datetime import datetime
import shutil

def merge_files_by_month():
    base_path = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco copy/prana_log"
    
    months = ['Aug', 'Sept']
    
    for month in months:
        month_path = os.path.join(base_path, month)
        if not os.path.exists(month_path):
            continue
            
        # Output file name
        output_file = os.path.join(month_path, f"PRANA_LOG_{month.upper()}_COMPLETE.md")
        
        # Skip if already exists and is recent
        if os.path.exists(output_file):
            print(f"Output file already exists: {output_file}")
            continue
            
        print(f"\n🔄 Processing {month} directory...")
        
        # Find all files to merge (excluding already merged files)
        patterns = ['*.txt', '*.md']
        files_to_merge = []
        
        for pattern in patterns:
            files = glob.glob(os.path.join(month_path, pattern))
            for file in files:
                # Skip already merged files and certain system files
                filename = os.path.basename(file)
                if (filename.startswith('PRANA_LOG_') or 
                    filename.startswith('COMPLETE_PRANA_LOG_') or
                    filename == 'merge_files.py' or
                    filename == '.DS_Store'):
                    continue
                files_to_merge.append(file)
        
        if not files_to_merge:
            print(f"   No files to merge in {month}")
            continue
            
        # Sort files by name for consistent ordering
        files_to_merge.sort()
        
        print(f"   Found {len(files_to_merge)} files to merge:")
        for file in files_to_merge:
            print(f"     - {os.path.basename(file)}")
        
        # Create merged file
        total_lines = 0
        total_size = 0
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Write header
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            outfile.write(f"# 🧠 PRANA LOG {month.upper()} COMPLETE ARCHIVE 🧠\n")
            outfile.write(f"# Merged: {timestamp}\n\n")
            outfile.write(f"This document contains ALL prana log files from {month}:\n\n")
            
            for i, file_path in enumerate(files_to_merge, 1):
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                total_size += file_size
                
                outfile.write(f"**File {i}/{len(files_to_merge)}**: {filename} ({file_size:,} bytes)\n")
            
            outfile.write(f"\n**Total Files**: {len(files_to_merge)}\n")
            outfile.write(f"**Total Size**: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)\n\n")
            outfile.write("---\n\n")
            
            # Merge file contents
            for i, file_path in enumerate(files_to_merge, 1):
                filename = os.path.basename(file_path)
                
                outfile.write(f"\n## 📄 FILE {i}: {filename}\n")
                outfile.write(f"**Source**: {file_path}\n")
                outfile.write(f"**Modified**: {datetime.fromtimestamp(os.path.getmtime(file_path))}\n\n")
                outfile.write("```\n")
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as infile:
                        content = infile.read()
                        outfile.write(content)
                        total_lines += content.count('\n')
                        
                        # Add newline if file doesn't end with one
                        if content and not content.endswith('\n'):
                            outfile.write('\n')
                            
                except Exception as e:
                    outfile.write(f"ERROR READING FILE: {e}\n")
                
                outfile.write("```\n\n")
                outfile.write("---\n\n")
        
        print(f"   ✅ Created: {output_file}")
        print(f"   📊 Stats: {total_lines:,} lines, {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
        
        # Ask before deleting individual files
        print(f"   \n🗑️  Ready to delete {len(files_to_merge)} individual files...")
        response = input(f"   Delete individual files from {month}? (y/N): ").strip().lower()
        
        if response == 'y':
            deleted_count = 0
            for file_path in files_to_merge:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    print(f"     ✅ Deleted: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"     ❌ Error deleting {os.path.basename(file_path)}: {e}")
            
            print(f"   🎯 Deleted {deleted_count}/{len(files_to_merge)} files")
        else:
            print(f"   ⏭️  Skipped deletion for {month}")

if __name__ == "__main__":
    print("🚀 Prana Log Monthly Merger Starting...")
    merge_files_by_month()
    print("\n✨ Merge process complete!")
