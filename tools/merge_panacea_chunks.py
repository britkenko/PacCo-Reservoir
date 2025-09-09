#!/usr/bin/env python3
"""
Panacea Files Merger (Excluding Panacea_Bravery)
Merges all panacea files except Panacea_Bravery.md and divides into 10MB chunks
"""

import os
import glob
from datetime import datetime
import math

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def merge_panacea_files():
    base_path = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco copy/panacea"
    
    # Find all markdown files except Panacea_Bravery.md
    patterns = ['*.md']
    files_to_merge = []
    
    for pattern in patterns:
        files = glob.glob(os.path.join(base_path, pattern))
        for file in files:
            filename = os.path.basename(file)
            # Skip Panacea_Bravery.md and any previously merged files
            if (filename == 'Panacea_Bravery.md' or 
                filename.startswith('PANACEA_COMPLETE_') or
                filename.startswith('PANACEA_CHUNK_')):
                continue
            files_to_merge.append(file)
    
    if not files_to_merge:
        print("No Panacea files found to merge!")
        return
        
    # Sort files by name for consistent ordering
    files_to_merge.sort()
    
    print(f"🔄 Processing Panacea directory...")
    print(f"   Found {len(files_to_merge)} files to merge:")
    
    total_size_mb = 0
    for file in files_to_merge:
        size_mb = get_file_size_mb(file)
        total_size_mb += size_mb
        print(f"     - {os.path.basename(file)} ({size_mb:.2f} MB)")
    
    print(f"   📊 Total size: {total_size_mb:.2f} MB")
    
    # Calculate number of 10MB chunks needed
    chunk_size_mb = 10
    num_chunks = math.ceil(total_size_mb / chunk_size_mb)
    print(f"   📦 Will create {num_chunks} chunks of ~{chunk_size_mb}MB each")
    
    # Create temporary complete file first
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    temp_file = os.path.join(base_path, f"TEMP_PANACEA_COMPLETE_{timestamp}.md")
    
    total_lines = 0
    total_bytes = 0
    
    print(f"\n🔨 Creating temporary complete file...")
    
    with open(temp_file, 'w', encoding='utf-8') as outfile:
        # Write header
        outfile.write(f"# 🧠 PANACEA COMPLETE ARCHIVE (Excluding Bravery) 🧠\n")
        outfile.write(f"# Merged: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        outfile.write(f"This document contains ALL panacea files except Panacea_Bravery.md:\n\n")
        
        for i, file_path in enumerate(files_to_merge, 1):
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            total_bytes += file_size
            
            outfile.write(f"**File {i}/{len(files_to_merge)}**: {filename} ({file_size:,} bytes, {file_size/1024/1024:.2f} MB)\n")
        
        outfile.write(f"\n**Total Files**: {len(files_to_merge)}\n")
        outfile.write(f"**Total Size**: {total_bytes:,} bytes ({total_bytes/1024/1024:.2f} MB)\n")
        outfile.write(f"**Excluded**: Panacea_Bravery.md\n\n")
        outfile.write("---\n\n")
        
        # Merge file contents
        for i, file_path in enumerate(files_to_merge, 1):
            filename = os.path.basename(file_path)
            
            outfile.write(f"\n## 📄 FILE {i}: {filename}\n")
            outfile.write(f"**Source**: {file_path}\n")
            outfile.write(f"**Modified**: {datetime.fromtimestamp(os.path.getmtime(file_path))}\n\n")
            outfile.write("```markdown\n")
            
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
    
    print(f"   ✅ Temporary file created: {total_lines:,} lines, {total_bytes:,} bytes")
    
    # Now split into 10MB chunks
    print(f"\n📦 Splitting into {chunk_size_mb}MB chunks...")
    
    chunk_size_bytes = chunk_size_mb * 1024 * 1024  # 10MB in bytes
    chunk_num = 1
    current_chunk_size = 0
    
    chunk_files = []
    
    with open(temp_file, 'r', encoding='utf-8') as infile:
        current_chunk_file = os.path.join(base_path, f"PANACEA_CHUNK_{chunk_num:02d}_of_{num_chunks:02d}.md")
        chunk_files.append(current_chunk_file)
        
        with open(current_chunk_file, 'w', encoding='utf-8') as outfile:
            # Write chunk header
            outfile.write(f"# 🧠 PANACEA COMPLETE ARCHIVE - CHUNK {chunk_num}/{num_chunks} 🧠\n")
            outfile.write(f"# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            outfile.write(f"# Chunk Size: ~{chunk_size_mb}MB | Total Archive: {total_bytes/1024/1024:.2f}MB\n\n")
            
            current_chunk_size = len(outfile.tell().to_bytes(8, 'big'))  # Header size estimate
            
            for line in infile:
                line_bytes = len(line.encode('utf-8'))
                
                # Check if adding this line would exceed chunk size
                if current_chunk_size + line_bytes > chunk_size_bytes and chunk_num < num_chunks:
                    # Close current chunk and start new one
                    outfile.write(f"\n\n---\n**END OF CHUNK {chunk_num}/{num_chunks}**\n")
                    outfile.write(f"**Continue in**: PANACEA_CHUNK_{chunk_num+1:02d}_of_{num_chunks:02d}.md\n")
                    
                    chunk_num += 1
                    current_chunk_file = os.path.join(base_path, f"PANACEA_CHUNK_{chunk_num:02d}_of_{num_chunks:02d}.md")
                    chunk_files.append(current_chunk_file)
                    
                    outfile.close()
                    outfile = open(current_chunk_file, 'w', encoding='utf-8')
                    
                    # Write new chunk header
                    outfile.write(f"# 🧠 PANACEA COMPLETE ARCHIVE - CHUNK {chunk_num}/{num_chunks} 🧠\n")
                    outfile.write(f"# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    outfile.write(f"# Chunk Size: ~{chunk_size_mb}MB | Total Archive: {total_bytes/1024/1024:.2f}MB\n")
                    outfile.write(f"**Previous chunk**: PANACEA_CHUNK_{chunk_num-1:02d}_of_{num_chunks:02d}.md\n\n")
                    
                    current_chunk_size = 0
                
                outfile.write(line)
                current_chunk_size += line_bytes
            
            # Close final chunk
            if chunk_num == num_chunks:
                outfile.write(f"\n\n---\n**END OF FINAL CHUNK {chunk_num}/{num_chunks}**\n")
    
    # Remove temporary file
    os.remove(temp_file)
    
    print(f"   ✅ Created {len(chunk_files)} chunk files:")
    for i, chunk_file in enumerate(chunk_files, 1):
        chunk_size_mb = get_file_size_mb(chunk_file)
        print(f"     📦 Chunk {i}: {os.path.basename(chunk_file)} ({chunk_size_mb:.2f} MB)")
    
    # Ask about deleting original files
    print(f"\n🗑️  Ready to delete {len(files_to_merge)} original files...")
    response = input(f"   Delete original Panacea files (keeping Panacea_Bravery.md)? (y/N): ").strip().lower()
    
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
        print(f"   💾 Kept: Panacea_Bravery.md")
    else:
        print(f"   ⏭️  Skipped deletion - original files preserved")
    
    return chunk_files

if __name__ == "__main__":
    print("🚀 Panacea Files Merger (Excluding Bravery) Starting...")
    chunk_files = merge_panacea_files()
    print(f"\n✨ Merge process complete!")
    print(f"📊 Summary: Created {len(chunk_files) if chunk_files else 0} chunks of ~10MB each")
