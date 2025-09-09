#!/usr/bin/env python3
"""
CODE SUGGESTIONS REMOVER
Removes unwanted code suggestion blocks from panacea and other files
"""

import os
import re
from pathlib import Path

def clean_code_suggestions():
    """Remove code suggestion blocks from files"""
    
    base_path = Path("/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco")
    
    # Patterns to identify and remove code suggestion blocks
    patterns_to_remove = [
        # Simple message blocks
        r'The following changes were successfully sent to the user\. No need to reiterate any file changes\.',
        
        # Code instruction blocks that start with "In `filename`"
        r'In `[^`]+\.html?`[^`]*?replace.*?(?=\n\n|\n[A-Z]|\nUser:|\nAI:|\n##|\n\*\*|\n---|\Z)',
        r'In `[^`]+\.py`[^`]*?replace.*?(?=\n\n|\n[A-Z]|\nUser:|\nAI:|\n##|\n\*\*|\n---|\Z)',
        r'In `[^`]+\.js`[^`]*?replace.*?(?=\n\n|\n[A-Z]|\nUser:|\nAI:|\n##|\n\*\*|\n---|\Z)',
        
        # Replace the entire blocks
        r'Replace the entire.*?function.*?with:.*?(?=\n\n|\n[A-Z]|\nUser:|\nAI:|\n##|\n\*\*|\n---|\Z)',
        
        # JSON instruction blocks
        r'\{"instructions":"In `[^`]+`.*?\}',
        
        # Code blocks that are suggestions
        r'```html\n.*?async function.*?```',
        r'```javascript\n.*?async function.*?```',
        r'```python\n.*?async function.*?```',
        
        # Artin signature lines
        r'\nArtin\n',
        
        # Large code diff blocks (- and + lines)
        r'\n[-+]\s+.*?(?=\n[^-+]|\Z)',
    ]
    
    print("🧹 CODE SUGGESTIONS REMOVER STARTING...")
    print("=" * 60)
    
    files_processed = 0
    total_removals = 0
    
    # Target file patterns
    file_patterns = [
        "panacea/*.md",
        "prana_log/*.md", 
        "tools/*.md",
        "*.md"
    ]
    
    for pattern in file_patterns:
        files = list(base_path.glob(pattern))
        
        for file_path in files:
            if not file_path.is_file():
                continue
                
            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                cleaned_content = original_content
                file_removals = 0
                
                # Apply each removal pattern
                for pattern in patterns_to_remove:
                    matches_before = len(re.findall(pattern, cleaned_content, re.DOTALL | re.IGNORECASE))
                    cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.DOTALL | re.IGNORECASE)
                    matches_after = len(re.findall(pattern, cleaned_content, re.DOTALL | re.IGNORECASE))
                    
                    removals_this_pattern = matches_before - matches_after
                    file_removals += removals_this_pattern
                
                # Clean up multiple consecutive newlines
                cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
                
                # Only write if changes were made
                if cleaned_content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_content)
                    
                    files_processed += 1
                    total_removals += file_removals
                    
                    size_reduction = len(original_content) - len(cleaned_content)
                    print(f"✅ Cleaned: {file_path.name}")
                    print(f"   Removals: {file_removals} blocks")
                    print(f"   Size reduction: {size_reduction:,} characters")
                
            except Exception as e:
                print(f"❌ Error processing {file_path.name}: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 CODE SUGGESTIONS CLEANING COMPLETE!")
    print(f"📁 Files processed: {files_processed}")
    print(f"🗑️ Total removals: {total_removals}")
    print("=" * 60)

if __name__ == "__main__":
    clean_code_suggestions()
