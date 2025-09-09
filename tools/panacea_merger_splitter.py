#!/usr/bin/env python3
"""
PANACEA COMPLETE MERGER AND 10MB SPLITTER
Merges all panacea content and splits into 10MB chunks
"""

import os
from pathlib import Path
from datetime import datetime
import math

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def merge_and_split_panacea():
    """Merge all panacea content and split into 10MB chunks"""
    
    panacea_dir = Path("/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea")
    
    print("🧠 PANACEA COMPLETE MERGER & 10MB SPLITTER")
    print("=" * 60)
    
    # Files to include in the merge (excluding previously merged chunks and empty files)
    files_to_merge = []
    exclude_patterns = [
        "PANACEA_MERGED_", "PANACEA_CHUNK_", "PANACEA_COMPLETE_",
        "PANACEA_KEY_INSIGHTS.md"  # Keep insights separate
    ]
    
    # Find all markdown files
    for md_file in panacea_dir.glob("*.md"):
        # Skip if matches exclude patterns or is empty
        if any(pattern in md_file.name for pattern in exclude_patterns):
            continue
        
        if md_file.stat().st_size == 0:
            print(f"⚠️  Skipping empty file: {md_file.name}")
            continue
            
        files_to_merge.append(md_file)
    
    # Sort files by name for consistent ordering
    files_to_merge.sort(key=lambda x: x.name)
    
    print(f"📂 Found {len(files_to_merge)} files to merge:")
    total_size_mb = 0
    
    for file_path in files_to_merge:
        size_mb = get_file_size_mb(file_path)
        total_size_mb += size_mb
        print(f"   - {file_path.name} ({size_mb:.2f} MB)")
    
    print(f"\n📊 Total content: {total_size_mb:.2f} MB")
    
    # Calculate number of 10MB chunks needed
    chunks_needed = math.ceil(total_size_mb / 10)
    print(f"📦 Will create {chunks_needed} chunks of ~10MB each")
    
    # Create merged content
    print(f"\n🔄 Merging content...")
    
    merged_content = []
    
    # Add header
    header = f"""# 🧠 PANACEA COMPLETE MERGED ARCHIVE
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Size:** {total_size_mb:.2f} MB  
**Source Files:** {len(files_to_merge)} files  
**Split Into:** {chunks_needed} chunks of ~10MB each  

## 📋 Source Files Included:
"""
    
    for i, file_path in enumerate(files_to_merge, 1):
        size_mb = get_file_size_mb(file_path)
        header += f"{i}. **{file_path.name}** ({size_mb:.2f} MB)\n"
    
    header += f"\n---\n\n"
    merged_content.append(header)
    
    # Process each file
    for file_path in files_to_merge:
        print(f"   📄 Processing: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add file separator
            file_header = f"""
## 📄 SOURCE FILE: {file_path.name}
**Original Size:** {get_file_size_mb(file_path):.2f} MB  
**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  

---

"""
            
            merged_content.append(file_header)
            merged_content.append(content)
            merged_content.append("\n\n")
            
        except Exception as e:
            print(f"   ❌ Error reading {file_path.name}: {e}")
            continue
    
    # Combine all content
    full_content = "".join(merged_content)
    
    print(f"\n✅ Merge complete! Total merged size: {len(full_content) / (1024*1024):.2f} MB")
    
    # Split into 10MB chunks
    print(f"\n📦 Splitting into 10MB chunks...")
    
    chunk_size = 10 * 1024 * 1024  # 10MB in bytes
    content_bytes = full_content.encode('utf-8')
    total_bytes = len(content_bytes)
    
    chunk_number = 1
    position = 0
    
    while position < total_bytes:
        # Calculate chunk end position
        chunk_end = min(position + chunk_size, total_bytes)
        
        # If not at the end, try to find a good break point (line ending)
        if chunk_end < total_bytes:
            # Look for a line break within the last 1000 bytes of the chunk
            search_start = max(chunk_end - 1000, position)
            chunk_data = content_bytes[search_start:chunk_end + 1000]
            
            # Find the last occurrence of double newline (paragraph break)
            last_paragraph = chunk_data.rfind(b'\n\n')
            if last_paragraph != -1:
                # Adjust chunk_end to the paragraph break
                chunk_end = search_start + last_paragraph + 2
        
        # Extract chunk content
        chunk_bytes = content_bytes[position:chunk_end]
        chunk_text = chunk_bytes.decode('utf-8')
        
        # Add chunk header
        chunk_header = f"""# 🧠 PANACEA MERGED ARCHIVE - CHUNK {chunk_number}/{chunks_needed}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Chunk Size:** ~{len(chunk_bytes) / (1024*1024):.2f} MB  
**Total Archive:** {total_size_mb:.2f} MB  
**Position:** {position:,} - {chunk_end:,} bytes  

"""
        
        if chunk_number > 1:
            chunk_header += f"**Previous chunk:** PANACEA_MERGED_CHUNK_{chunk_number-1:02d}_of_{chunks_needed:02d}.md\n"
        if chunk_number < chunks_needed:
            chunk_header += f"**Next chunk:** PANACEA_MERGED_CHUNK_{chunk_number+1:02d}_of_{chunks_needed:02d}.md\n"
        
        chunk_header += "\n---\n\n"
        
        final_chunk = chunk_header + chunk_text
        
        # Write chunk file
        chunk_filename = f"PANACEA_MERGED_CHUNK_{chunk_number:02d}_of_{chunks_needed:02d}.md"
        chunk_path = panacea_dir / chunk_filename
        
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(final_chunk)
        
        chunk_size_mb = len(final_chunk.encode('utf-8')) / (1024*1024)
        print(f"   ✅ Created: {chunk_filename} ({chunk_size_mb:.2f} MB)")
        
        position = chunk_end
        chunk_number += 1
    
    # Create master index file
    index_content = f"""# 🧠 PANACEA MERGED ARCHIVE - INDEX
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Size:** {total_size_mb:.2f} MB  
**Chunks Created:** {chunks_needed}  

## 📦 Archive Chunks:
"""
    
    for i in range(1, chunks_needed + 1):
        chunk_filename = f"PANACEA_MERGED_CHUNK_{i:02d}_of_{chunks_needed:02d}.md"
        chunk_path = panacea_dir / chunk_filename
        
        if chunk_path.exists():
            chunk_size_mb = get_file_size_mb(chunk_path)
            index_content += f"{i}. **{chunk_filename}** ({chunk_size_mb:.2f} MB)\n"
    
    index_content += f"""
## 🎯 Original Source Files:
"""
    
    for i, file_path in enumerate(files_to_merge, 1):
        size_mb = get_file_size_mb(file_path)
        index_content += f"{i}. **{file_path.name}** ({size_mb:.2f} MB)\n"
    
    index_content += f"""
## 📖 Usage Instructions:
1. Read chunks sequentially starting with CHUNK_01
2. Each chunk is ~10MB for optimal performance
3. Original source files remain unchanged
4. Use PANACEA_KEY_INSIGHTS.md for quick overview

---
*Generated by PANACEA Complete Merger & 10MB Splitter*
"""
    
    index_path = panacea_dir / "PANACEA_MERGED_INDEX.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"\n" + "=" * 60)
    print("🎉 PANACEA MERGE & SPLIT COMPLETE!")
    print(f"📁 Created {chunks_needed} chunks of ~10MB each")
    print(f"📋 Index file: PANACEA_MERGED_INDEX.md")
    print(f"📊 Total processed: {total_size_mb:.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    merge_and_split_panacea()
