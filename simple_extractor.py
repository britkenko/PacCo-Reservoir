#!/usr/bin/env python3
"""
Simplified and Accurate Content Extractor for Panacea Dialogues
"""

import re
from pathlib import Path

def is_coding_content(text):
    """Check if text contains coding-related content"""
    coding_indicators = [
        'traceback', 'error:', 'python', 'javascript', 'api', 'code', 'function', 'import', 
        'def ', 'class ', 'git', 'github', 'install', 'pip', 'npm', 'json', 'html', 
        'css', 'database', 'query', 'apiremovedinv1', 'cell in[', '```'
    ]
    
    text_lower = text.lower()
    for indicator in coding_indicators:
        if indicator in text_lower:
            return True
    return False

def is_negative_content(text):
    """Check if text is overly negative"""
    negative_words = [
        'hate', 'angry', 'furious', 'disgusting', 'awful', 'terrible', 'horrible', 
        'stupid', 'idiot', 'dumb', 'kill', 'murder', 'violence', 'abuse', 'toxic'
    ]
    
    text_lower = text.lower()
    negative_count = sum(1 for word in negative_words if word in text_lower)
    return negative_count >= 2  # Only exclude if multiple negative words

def extract_dialogues_simple(file_path):
    """Extract dialogues using a simple line-by-line approach"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    dialogues = []
    user_text = ""
    ai_text = ""
    current_speaker = None
    
    for line in lines:
        line = line.strip()
        
        if line == "User":
            # If we were already collecting ChatGPT/AI text, save the dialogue
            if current_speaker in ["ChatGPT", "AI"] and user_text and ai_text:
                dialogues.append((user_text.strip(), ai_text.strip()))
            # Start new user section
            current_speaker = "User"
            user_text = ""
            ai_text = ""
        elif line in ["ChatGPT", "AI"]:
            current_speaker = line
        elif current_speaker == "User" and line:
            user_text += line + " "
        elif current_speaker in ["ChatGPT", "AI"] and line:
            ai_text += line + " "
    
    # Don't forget the last dialogue
    if user_text and ai_text:
        dialogues.append((user_text.strip(), ai_text.strip()))
    
    return dialogues

def categorize_content(user_text, ai_text):
    """Categorize dialogue into meaningful themes"""
    combined = (user_text + " " + ai_text).lower()
    
    # Philosophy and wisdom keywords
    if any(word in combined for word in ['wisdom', 'philosophy', 'meaning', 'purpose', 'truth', 'reality', 'consciousness', 'existence', 'identity', 'values', 'principles', 'ethics', 'moral']):
        return 'wisdom_and_philosophy'
    
    # Relationship and communication
    elif any(word in combined for word in ['relationship', 'friendship', 'love', 'trust', 'respect', 'empathy', 'compassion', 'communication', 'conversation', 'dialogue', 'listening', 'understanding']):
        return 'relationship_and_communication'
    
    # Personal development and psychology  
    elif any(word in combined for word in ['growth', 'development', 'learn', 'education', 'self', 'personality', 'character', 'emotion', 'feeling', 'psychology', 'behavior', 'mind']):
        return 'personal_development'
    
    # Life experience and insights
    elif any(word in combined for word in ['experience', 'life', 'journey', 'challenge', 'opportunity', 'change', 'time', 'moment', 'future', 'past', 'memory']):
        return 'life_and_experience'
    
    # Creativity and ideas
    elif any(word in combined for word in ['creative', 'creativity', 'imagination', 'innovation', 'idea', 'concept', 'vision', 'dream', 'artistic', 'design']):
        return 'creativity_and_innovation'
    
    # Problem solving and analysis
    elif any(word in combined for word in ['problem', 'solution', 'solve', 'answer', 'question', 'why', 'how', 'think', 'analysis', 'understand']):
        return 'problem_solving'
    
    # Success and achievement
    elif any(word in combined for word in ['success', 'achievement', 'goal', 'ambition', 'motivation', 'leadership', 'influence', 'impact']):
        return 'success_and_achievement'
    
    else:
        return 'general_insights'

def main():
    input_file = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea/panacea_1.md"
    output_dir = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea/extracted_categories"
    
    print("🚀 Starting simple content extraction...")
    
    # Extract all dialogues
    dialogues = extract_dialogues_simple(input_file)
    print(f"📚 Found {len(dialogues)} total dialogues")
    
    # Filter and categorize
    categorized = {
        'wisdom_and_philosophy': [],
        'relationship_and_communication': [],
        'personal_development': [],
        'life_and_experience': [],
        'creativity_and_innovation': [],
        'problem_solving': [],
        'success_and_achievement': [],
        'general_insights': []
    }
    
    stats = {'total': len(dialogues), 'meaningful': 0, 'coding_excluded': 0, 'negative_excluded': 0, 'too_short': 0}
    
    for i, (user_text, ai_text) in enumerate(dialogues):
        # Skip very short dialogues
        if len(user_text) < 20 or len(ai_text) < 20:
            stats['too_short'] += 1
            continue
        
        # Skip coding content
        if is_coding_content(user_text) or is_coding_content(ai_text):
            stats['coding_excluded'] += 1
            continue
        
        # Skip overly negative content
        if is_negative_content(user_text) or is_negative_content(ai_text):
            stats['negative_excluded'] += 1
            continue
        
        # Categorize meaningful content
        stats['meaningful'] += 1
        category = categorize_content(user_text, ai_text)
        categorized[category].append({
            'id': i + 1,
            'user': user_text,
            'ai': ai_text
        })
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save summary
    summary = f"""# Content Extraction Summary

## Statistics
- **Total dialogues found:** {stats['total']}
- **Meaningful content extracted:** {stats['meaningful']}
- **Coding content excluded:** {stats['coding_excluded']}
- **Negative content excluded:** {stats['negative_excluded']}
- **Too short excluded:** {stats['too_short']}

## Categories with Content
"""
    
    category_names = {
        'wisdom_and_philosophy': 'Wisdom and Philosophy',
        'relationship_and_communication': 'Relationship and Communication',
        'personal_development': 'Personal Development',
        'life_and_experience': 'Life and Experience',
        'creativity_and_innovation': 'Creativity and Innovation',
        'problem_solving': 'Problem Solving',
        'success_and_achievement': 'Success and Achievement',
        'general_insights': 'General Insights'
    }
    
    for category, dialogues in categorized.items():
        if dialogues:
            name = category_names[category]
            summary += f"- **{name}:** {len(dialogues)} dialogues\n"
            
            # Save category file
            content = f"# {name}\n\n"
            for dialogue in dialogues:
                content += f"## Dialogue {dialogue['id']}\n\n"
                content += f"**User:**\n{dialogue['user']}\n\n"
                content += f"**AI:**\n{dialogue['ai']}\n\n---\n\n"
            
            with open(output_path / f"{category}.md", "w", encoding="utf-8") as f:
                f.write(content)
    
    with open(output_path / "summary.md", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print(f"\n📊 Results:")
    print(f"✅ Meaningful dialogues: {stats['meaningful']}")
    print(f"❌ Coding excluded: {stats['coding_excluded']}")
    print(f"❌ Negative excluded: {stats['negative_excluded']}")
    print(f"❌ Too short: {stats['too_short']}")
    
    print(f"\n🎯 Categories:")
    for category, dialogues in categorized.items():
        if dialogues:
            name = category_names[category]
            print(f"  {name}: {len(dialogues)} dialogues")
    
    print(f"\n✅ Files saved to: {output_path}")

if __name__ == "__main__":
    main()
