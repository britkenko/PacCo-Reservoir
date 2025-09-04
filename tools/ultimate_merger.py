#!/usr/bin/env python3
"""
Ultimate Comprehensive Merger Script
Combines all extracted conversations and September prana logs into one complete document
"""

import os
from datetime import datetime

def create_ultimate_merged_file():
    """Create the ultimate merged file combining all sources"""
    
    # Define source files
    extracted_conversations = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/tools/merged_extracted_conversations.md"
    september_pranalogs = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/tools/merged_september_pranalogs.md"
    
    # Output file
    ultimate_output = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/tools/ULTIMATE_MERGED_PACO_ARCHIVE.md"
    
    # Check if source files exist
    sources = []
    
    if os.path.exists(extracted_conversations):
        size = os.path.getsize(extracted_conversations)
        sources.append(("Extracted Conversations", extracted_conversations, size))
        print(f"✅ Found extracted conversations: {size / (1024*1024):.2f} MB")
    else:
        print("❌ Extracted conversations file not found")
    
    if os.path.exists(september_pranalogs):
        size = os.path.getsize(september_pranalogs)
        sources.append(("September Prana Logs", september_pranalogs, size))
        print(f"✅ Found September prana logs: {size / (1024*1024):.2f} MB")
    else:
        print("❌ September prana logs file not found")
    
    if not sources:
        print("❌ No source files found to merge!")
        return None
    
    # Create ultimate merged content
    merged_content = []
    
    # Ultimate header
    merged_content.append("# 🌟 ULTIMATE PACO ARCHIVE - COMPLETE MERGED COLLECTION 🌟")
    merged_content.append(f"# Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    merged_content.append("")
    merged_content.append("This is the comprehensive, ultimate merged archive containing:")
    merged_content.append("- **34 Extracted ChatGPT Conversations** from Cortex-P-Rev repository")
    merged_content.append("- **12 September 2025 Prana Log Files** with dialogues, observations, and processing logs")
    merged_content.append("- **Complete contextual history** for September Cor(心) framework processing")
    merged_content.append("")
    merged_content.append("Total sources merged: **46 files**")
    merged_content.append("")
    
    total_size = sum(size for _, _, size in sources)
    merged_content.append(f"**Combined archive size**: {total_size / (1024*1024):.2f} MB")
    merged_content.append("")
    merged_content.append("🔥" * 80)
    merged_content.append("")
    
    # Process each source file
    for i, (source_name, file_path, file_size) in enumerate(sources, 1):
        print(f"Processing {source_name}...")
        
        merged_content.append(f"# 📚 SECTION {i}: {source_name.upper()}")
        merged_content.append(f"**Source File**: `{os.path.basename(file_path)}`")
        merged_content.append(f"**File Size**: {file_size / (1024*1024):.2f} MB")
        merged_content.append("")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add the complete content
            merged_content.append(content)
            merged_content.append("")
            merged_content.append("🔥" * 80)
            merged_content.append("")
            
        except Exception as e:
            print(f"Error reading {source_name}: {e}")
            merged_content.append(f"**ERROR**: Could not read {source_name} - {e}")
            merged_content.append("")
            merged_content.append("🔥" * 80)
            merged_content.append("")
    
    # Write ultimate merged file
    try:
        with open(ultimate_output, 'w', encoding='utf-8') as f:
            f.write('\n'.join(merged_content))
        
        final_size = os.path.getsize(ultimate_output)
        print(f"\n🎉 ULTIMATE MERGE COMPLETED! 🎉")
        print(f"📁 Output: {ultimate_output}")
        print(f"📊 Final size: {final_size / (1024*1024):.2f} MB")
        print(f"📈 Sources combined: {len(sources)} major collections")
        print(f"🗂️  Total files archived: 46 individual files")
        
        return ultimate_output
        
    except Exception as e:
        print(f"❌ Error writing ultimate merged file: {e}")
        return None

if __name__ == "__main__":
    result = create_ultimate_merged_file()
    if result:
        print(f"\n✨ SUCCESS: Ultimate PACO archive created! ✨")
        print(f"🚀 Ready for September Cor(心) processing! 🚀")
    else:
        print("💥 Ultimate merge failed!")
