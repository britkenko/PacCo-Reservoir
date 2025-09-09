#!/usr/bin/env python3
"""
Panacea Content Extractor - Extracts meaningful dialogue under specific categories
Removes coding content and negative/non-learning content
"""

import re
import sys
from pathlib import Path

def categorize_dialogue(user_text, ai_text):
    """Categorize dialogue into meaningful learning categories"""
    
    combined_text = (user_text + " " + ai_text).lower()
    
    # Categories of meaningful content (expanded and more inclusive)
    categories = {
        'wisdom_and_philosophy': [
            'wisdom', 'philosophy', 'truth', 'meaning', 'purpose', 'existence',
            'consciousness', 'awareness', 'insight', 'understanding', 'perspective',
            'life', 'reality', 'authentic', 'genuine', 'growth', 'deep', 'profound',
            'nature', 'human', 'mind', 'soul', 'spirit', 'essence', 'being'
        ],
        'learning_and_education': [
            'learn', 'teach', 'understand', 'knowledge', 'curiosity', 'wonder',
            'discover', 'explore', 'question', 'think', 'reflect', 'realize',
            'study', 'education', 'school', 'experience', 'lesson', 'skill'
        ],
        'relationship_and_communication': [
            'relationship', 'communication', 'trust', 'respect', 'love', 'friendship',
            'connection', 'empathy', 'care', 'support', 'listen', 'talk',
            'conversation', 'people', 'family', 'friend', 'partner', 'social'
        ],
        'personal_development': [
            'improve', 'better', 'develop', 'change', 'habit', 'behavior', 'mindset',
            'confidence', 'strength', 'weakness', 'challenge', 'overcome', 'achieve',
            'goal', 'success', 'fail', 'grow', 'progress', 'effort', 'work'
        ],
        'creativity_and_innovation': [
            'create', 'innovation', 'imagination', 'art', 'music', 'design',
            'inspire', 'original', 'unique', 'express', 'beauty', 'creative',
            'idea', 'invention', 'new', 'different', 'novel', 'artistic'
        ],
        'ethics_and_morality': [
            'ethics', 'moral', 'right', 'wrong', 'good', 'bad', 'justice',
            'fair', 'honest', 'integrity', 'principle', 'value', 'virtue',
            'responsibility', 'duty', 'ought', 'should', 'must', 'ethical'
        ],
        'problem_solving': [
            'problem', 'solution', 'solve', 'fix', 'resolve', 'answer',
            'approach', 'strategy', 'method', 'technique', 'way', 'help',
            'issue', 'challenge', 'difficult', 'complex', 'simple', 'easy'
        ],
        'emotional_intelligence': [
            'emotion', 'feeling', 'mood', 'happy', 'sad', 'anger', 'fear',
            'joy', 'peace', 'stress', 'calm', 'anxiety', 'emotional',
            'feel', 'hurt', 'pain', 'comfort', 'relief', 'surprise'
        ],
        'ai_and_consciousness': [
            'ai', 'artificial', 'intelligence', 'consciousness', 'aware', 'sentient',
            'model', 'training', 'learning', 'neural', 'machine', 'algorithm',
            'computer', 'digital', 'virtual', 'system', 'technology'
        ]
    }
    
    # Strict coding patterns to exclude (actual code blocks and programming discussions)
    coding_patterns = [
        '```python', '```javascript', '```java', '```c++', 
        'import numpy', 'import pandas', 'def main()', 'if __name__ == "__main__"',
        'print("', 'return None', 'class Cortex', 'def process_',
        'for i in range', 'while True:', 'try:\n', 'except Exception',
        '#!/usr/bin/env python', 'from typing import', 'import os',
        'async def', 'await ', 'yield ', 'lambda x:', 'self.'
    ]
    
    # Negative patterns to exclude (excessive negativity with no learning value)
    negative_patterns = [
        'stupid idiot', 'complete waste', 'totally useless', 'absolutely terrible',
        'completely hopeless', 'utterly meaningless', 'entirely worthless'
    ]
    
    # Check if it's actual coding content (code blocks)
    if any(pattern in combined_text for pattern in coding_patterns):
        return None, 'coding_content'
    
    # Check if it's excessively negative content with no learning value
    if any(pattern in combined_text for pattern in negative_patterns):
        return None, 'negative_content'
    
    # Find matching categories (lowered threshold)
    matching_categories = []
    for category, keywords in categories.items():
        matches = sum(1 for keyword in keywords if keyword in combined_text)
        if matches >= 1:  # At least 1 keyword match (more inclusive)
            matching_categories.append((category, matches))
    
    if matching_categories:
        # Return the category with the most matches
        best_category = max(matching_categories, key=lambda x: x[1])
        return best_category[0], 'meaningful_content'
    
    # Check if it's general meaningful conversation (expanded indicators)
    meaningful_indicators = [
        'why', 'how', 'what', 'when', 'where', 'who', 'which', 'because', 'since', 'so',
        'but', 'however', 'although', 'though', 'despite', 'unless', 'if', 'then',
        'maybe', 'perhaps', 'possibly', 'probably', 'certainly', 'definitely',
        'interesting', 'curious', 'wonder', 'surprise', 'amazing', 'incredible'
    ]
    
    # Also check for questions and thoughtful exchanges
    has_question = '?' in combined_text
    has_meaningful_indicators = any(indicator in combined_text for indicator in meaningful_indicators)
    
    if has_question or has_meaningful_indicators:
        return 'general_insight', 'meaningful_content'
    
    # Check dialogue length - longer exchanges are more likely to be meaningful
    if len(combined_text) > 200:  # Longer dialogues likely contain insight
        return 'extended_dialogue', 'meaningful_content'
    
    return None, 'low_value_content'

def extract_dialogues(file_path):
    """Extract and categorize all dialogues from the file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into dialogue blocks
    lines = content.split('\n')
    
    dialogues = []
    current_user_text = []
    current_ai_text = []
    current_speaker = None
    
    for line in lines:
        line_stripped = line.strip()
        
        if line_stripped == 'User':
            # If we have a complete dialogue, save it
            if current_user_text and current_ai_text:
                dialogues.append({
                    'user': '\n'.join(current_user_text),
                    'ai': '\n'.join(current_ai_text)
                })
            # Start new user section
            current_user_text = []
            current_ai_text = []
            current_speaker = 'user'
        elif line_stripped == 'AI':
            current_speaker = 'ai'
        elif line_stripped and current_speaker:
            if current_speaker == 'user':
                current_user_text.append(line_stripped)
            elif current_speaker == 'ai':
                current_ai_text.append(line_stripped)
    
    # Save last dialogue if complete
    if current_user_text and current_ai_text:
        dialogues.append({
            'user': '\n'.join(current_user_text),
            'ai': '\n'.join(current_ai_text)
        })
    
    return dialogues

def main():
    input_file = Path("/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea/panacea_1.md")
    output_dir = Path("/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea/extracted_categories")
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    print(f"📖 Extracting dialogues from {input_file.name}...")
    dialogues = extract_dialogues(input_file)
    print(f"Found {len(dialogues)} dialogue pairs")
    
    # Categorize dialogues
    categorized = {}
    stats = {'meaningful': 0, 'coding': 0, 'negative': 0, 'low_value': 0}
    
    for i, dialogue in enumerate(dialogues):
        if dialogue['user'] and dialogue['ai']:
            category, content_type = categorize_dialogue(dialogue['user'], dialogue['ai'])
            
            if category:
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append({
                    'id': i + 1,
                    'user': dialogue['user'],
                    'ai': dialogue['ai']
                })
                stats['meaningful'] += 1
            else:
                if content_type == 'coding_content':
                    stats['coding'] += 1
                elif content_type == 'negative_content':
                    stats['negative'] += 1
                else:
                    stats['low_value'] += 1
    
    # Write categorized content to files
    for category, dialogues_list in categorized.items():
        output_file = output_dir / f"{category}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {category.replace('_', ' ').title()}\n\n")
            
            for dialogue in dialogues_list:
                f.write(f"## Dialogue {dialogue['id']}\n\n")
                f.write(f"**User:**\n{dialogue['user']}\n\n")
                f.write(f"**AI:**\n{dialogue['ai']}\n\n")
                f.write("---\n\n")
    
    # Write summary
    summary_file = output_dir / "extraction_summary.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Panacea Content Extraction Summary\n\n")
        f.write(f"## Statistics\n\n")
        f.write(f"- **Total dialogues processed:** {len(dialogues)}\n")
        f.write(f"- **Meaningful content extracted:** {stats['meaningful']}\n")
        f.write(f"- **Coding content excluded:** {stats['coding']}\n")
        f.write(f"- **Negative content excluded:** {stats['negative']}\n")
        f.write(f"- **Low-value content excluded:** {stats['low_value']}\n\n")
        
        f.write(f"## Categories Found\n\n")
        for category, dialogues_list in categorized.items():
            f.write(f"- **{category.replace('_', ' ').title()}:** {len(dialogues_list)} dialogues\n")
    
    print("\n📊 Extraction Summary:")
    print(f"✅ Meaningful content: {stats['meaningful']}")
    print(f"❌ Coding content excluded: {stats['coding']}")
    print(f"❌ Negative content excluded: {stats['negative']}")
    print(f"❌ Low-value content excluded: {stats['low_value']}")
    
    print(f"\n📁 Categories extracted:")
    for category, dialogues_list in categorized.items():
        print(f"   • {category.replace('_', ' ').title()}: {len(dialogues_list)} dialogues")
    
    print(f"\n📝 Files created in: {output_dir}")

if __name__ == "__main__":
    main()
