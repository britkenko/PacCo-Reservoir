#!/usr/bin/env python3
"""
Comprehensive Panacea Dialogue Cleaner
Removes coding dialogues and negative content with no learning value
"""

import re
import os

def identify_coding_sections(content):
    """Identify sections that contain coding content"""
    coding_patterns = [
        r'#!/usr/bin/env python',
        r'import \w+',
        r'def \w+\(',
        r'class \w+\(',
        r'```python',
        r'```javascript',
        r'```bash',
        r'```sql',
        r'```json',
        r'function\s+\w+\(',
        r'console\.log\(',
        r'document\.',
        r'window\.',
        r'<script',
        r'</script>',
        r'npm install',
        r'pip install',
        r'git clone',
        r'docker run',
        r'FROM ubuntu',
        r'SELECT \* FROM',
        r'CREATE TABLE',
        r'INSERT INTO',
        r'UPDATE SET',
        r'DELETE FROM',
        r'algorithm',
        r'debugging',
        r'compile',
        r'syntax error',
        r'stack trace',
        r'null pointer',
        r'exception',
        r'try:\s*\n',
        r'except:',
        r'if __name__ == "__main__"',
        r'mkdir -p',
        r'chmod \+x',
        r'sudo apt',
        r'yum install',
        r'brew install',
    ]
    
    coding_sections = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        for pattern in coding_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                coding_sections.append(i)
                break
    
    return coding_sections

def identify_negative_content(content):
    """Identify sections with negative content that has no learning value"""
    negative_patterns = [
        r'\b(hate|hatred|hateful)\b',
        r'\b(stupid|idiot|dumb|moron)\b', 
        r'\b(useless|worthless|pointless)\b',
        r'\b(terrible|awful|horrible|disgusting)\b',
        r'\b(waste|wasted|wasting)\s+(time|effort|energy)',
        r'\b(annoying|irritating|frustrating)\b',
        r'\b(angry|mad|furious|rage)\b',
        r'\bfuck\b',
        r'\bshit\b',
        r'\bdamn\b',
        r'\bhell\b',
        r'\b(kill|die|death)\s+(yourself|myself)\b',
    ]
    
    negative_sections = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        for pattern in negative_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Check if this is actually instructional/learning content
                learning_indicators = [
                    r'learn',
                    r'understand',
                    r'example',
                    r'teach',
                    r'explain',
                    r'demonstrate',
                    r'insight',
                    r'wisdom',
                    r'principle'
                ]
                
                is_learning = False
                # Check surrounding context (3 lines before and after)
                context_start = max(0, i-3)
                context_end = min(len(lines), i+4)
                context = ' '.join(lines[context_start:context_end])
                
                for learning_pattern in learning_indicators:
                    if re.search(learning_pattern, context, re.IGNORECASE):
                        is_learning = True
                        break
                
                if not is_learning:
                    negative_sections.append(i)
                break
    
    return negative_sections

def find_dialogue_boundaries(content, problematic_lines):
    """Find the start and end of dialogue sections containing problematic content"""
    lines = content.split('\n')
    sections_to_remove = []
    
    for line_num in problematic_lines:
        # Find the dialogue section this line belongs to
        section_start = line_num
        section_end = line_num
        
        # Find section start (look backwards for "User" or "AI")
        for i in range(line_num, -1, -1):
            if re.match(r'^(User|AI)$', lines[i].strip()):
                section_start = i
                break
        
        # Find section end (look forwards for next "User" or "AI") 
        for i in range(line_num + 1, len(lines)):
            if re.match(r'^(User|AI)$', lines[i].strip()):
                section_end = i
                break
        else:
            section_end = len(lines)
            
        sections_to_remove.append((section_start, section_end))
    
    return sections_to_remove

def remove_sections(content, sections_to_remove):
    """Remove specified sections from content"""
    lines = content.split('\n')
    
    # Sort sections in reverse order to remove from end to beginning
    sections_to_remove.sort(reverse=True, key=lambda x: x[0])
    
    # Remove duplicate/overlapping sections
    merged_sections = []
    for start, end in sections_to_remove:
        if not merged_sections or start >= merged_sections[-1][1]:
            merged_sections.append((start, end))
        else:
            # Merge overlapping sections
            merged_sections[-1] = (min(merged_sections[-1][0], start), 
                                 max(merged_sections[-1][1], end))
    
    # Remove sections
    for start, end in reversed(merged_sections):
        del lines[start:end]
    
    return '\n'.join(lines)

def clean_panacea_file(input_file, output_file):
    """Main cleaning function"""
    print(f"Reading file: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Original file size: {len(content.split())} lines")
    
    # Identify problematic content
    coding_lines = identify_coding_sections(content)
    negative_lines = identify_negative_content(content)
    
    print(f"Found {len(coding_lines)} lines with coding content")
    print(f"Found {len(negative_lines)} lines with negative content")
    
    # Combine problematic lines
    all_problematic_lines = list(set(coding_lines + negative_lines))
    
    if not all_problematic_lines:
        print("No problematic content found. File is already clean.")
        return
    
    # Find dialogue sections to remove
    sections_to_remove = find_dialogue_boundaries(content, all_problematic_lines)
    
    print(f"Will remove {len(sections_to_remove)} dialogue sections")
    
    # Remove sections
    cleaned_content = remove_sections(content, sections_to_remove)
    
    print(f"Cleaned file size: {len(cleaned_content.split())} lines")
    
    # Write cleaned content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"Cleaned file saved as: {output_file}")
    
    # Generate report
    report = {
        'original_lines': len(content.split('\n')),
        'cleaned_lines': len(cleaned_content.split('\n')),
        'removed_sections': len(sections_to_remove),
        'coding_lines_found': len(coding_lines),
        'negative_lines_found': len(negative_lines)
    }
    
    return report

if __name__ == "__main__":
    input_file = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea/panacea_1.md"
    output_file = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea/panacea_1_cleaned.md"
    
    if os.path.exists(input_file):
        report = clean_panacea_file(input_file, output_file)
        print("\nCleaning Report:")
        for key, value in report.items():
            print(f"  {key}: {value}")
    else:
        print(f"Input file not found: {input_file}")
