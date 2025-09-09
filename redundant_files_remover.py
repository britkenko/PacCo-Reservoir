#!/usr/bin/env python3
"""
REDUNDANT PANACEA FILES REMOVER
Removes the original panacea files that have been merged into chunks
"""

import os
from pathlib import Path

def remove_redundant_files():
    """Remove redundant panacea files after successful merge"""
    
    panacea_dir = Path("/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea")
    
    print("🗑️ REDUNDANT PANACEA FILES REMOVER")
    print("=" * 50)
    
    # Files to KEEP (essential merged files and references)
    keep_files = [
        "PANACEA_MERGED_CHUNK_01_of_03.md",
        "PANACEA_MERGED_CHUNK_02_of_03.md", 
        "PANACEA_MERGED_CHUNK_03_of_03.md",
        "PANACEA_MERGED_INDEX.md",
        "PANACEA_KEY_INSIGHTS.md",
        ".DS_Store"  # System file
    ]
    
    # Keep directories
    keep_dirs = [
        "Pana_categories"
    ]
    
    # Files that were merged (now redundant)
    redundant_files = [
        "Panacea_Bravery.md",
        "ULTIMATE_MERGED_PACO_ARCHIVE.md",
        "merged_extracted_conversations.md",
        "merged_september_pranalogs.md",
        "panacea00002.md",
        "panacea00003.md", 
        "panacea00004.md",
        "panacea_1.md",
        "panacea_1_backup.md",  # Empty file
        "panacea_proof_Hobit.md"
    ]
    
    print("📋 Files marked for removal:")
    
    removed_count = 0
    total_size_freed = 0
    
    for filename in redundant_files:
        file_path = panacea_dir / filename
        
        if file_path.exists() and file_path.is_file():
            file_size = file_path.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"   🗑️ {filename} ({file_size_mb:.2f} MB)")
            
            try:
                file_path.unlink()  # Remove the file
                removed_count += 1
                total_size_freed += file_size
                print(f"      ✅ Removed successfully")
                
            except Exception as e:
                print(f"      ❌ Error removing: {e}")
        else:
            print(f"   ⚠️ {filename} - not found or already removed")
    
    print(f"\n📊 REMOVAL SUMMARY:")
    print(f"   Files removed: {removed_count}")
    print(f"   Space freed: {total_size_freed / (1024*1024):.2f} MB")
    
    print(f"\n📂 REMAINING FILES:")
    remaining_files = list(panacea_dir.glob("*"))
    remaining_files.sort()
    
    for item in remaining_files:
        if item.is_file():
            size_mb = item.stat().st_size / (1024 * 1024)
            print(f"   📄 {item.name} ({size_mb:.2f} MB)")
        elif item.is_dir():
            print(f"   📁 {item.name}/")
    
    print(f"\n" + "=" * 50)
    print("🎉 CLEANUP COMPLETE!")
    print("✅ Redundant files removed")
    print("✅ Merged chunks preserved") 
    print("✅ Key insights maintained")
    print("=" * 50)

if __name__ == "__main__":
    # Safety check - confirm merged files exist before removing originals
    panacea_dir = Path("/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea")
    
    required_files = [
        "PANACEA_MERGED_CHUNK_01_of_03.md",
        "PANACEA_MERGED_CHUNK_02_of_03.md",
        "PANACEA_MERGED_CHUNK_03_of_03.md",
        "PANACEA_MERGED_INDEX.md"
    ]
    
    all_exist = all((panacea_dir / f).exists() for f in required_files)
    
    if all_exist:
        print("✅ Safety check passed - all merged files exist")
        remove_redundant_files()
    else:
        print("❌ Safety check failed - merged files missing, aborting cleanup")
        for f in required_files:
            if not (panacea_dir / f).exists():
                print(f"   Missing: {f}")
