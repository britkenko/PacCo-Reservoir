#!/usr/bin/env python3
"""
Improved Content Extractor for Panacea Dialogues
Extracts meaningful conversations while filtering out coding and negative content
"""

import re
from pathlib import Path

def is_coding_content(text):
    """Check if text contains coding-related content"""
    coding_patterns = [
        r'\b(python|javascript|html|css|sql|json|xml|api|code|function|class|import|export|console\.log|print\(|def |return |if __name__|#include|<script|<html|SELECT|INSERT|UPDATE|DELETE)\b',
        r'\b(git|github|repository|commit|merge|pull request|branch|fork|clone)\b',
        r'\b(error|exception|traceback|debugging|bug|syntax|compile|runtime)\b',
        r'\b(install|pip|npm|package|library|framework|django|flask|react|node)\b',
        r'\b(database|table|query|schema|migration|model|ORM)\b',
        r'```|`[^`]+`',  # Code blocks and inline code
        r'\w+\(\)|def \w+|class \w+|import \w+',  # Function/class definitions
        r'APIRemovedInV1|Traceback|Cell In\[\d+\]'  # Specific error patterns
    ]
    
    text_lower = text.lower()
    for pattern in coding_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    return False

def is_negative_content(text):
    """Check if text contains overly negative or low-value content"""
    negative_patterns = [
        r'\b(hate|angry|furious|rage|disgusting|awful|terrible|horrible|stupid|idiot|dumb)\b',
        r'\b(kill|murder|violence|hurt|pain|suffering|abuse|toxic)\b',
        r'\b(depressed|suicidal|hopeless|worthless|failure|loser)\b',
        r'\b(fuck|shit|damn|hell|bitch|asshole)\s',  # Strong profanity
        r'\b(racist|sexist|homophobic|bigot|discrimination)\b'
    ]
    
    text_lower = text.lower()
    for pattern in negative_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    return False

def is_meaningful_content(text):
    """Check if text contains meaningful, educational, or philosophical content"""
    meaningful_patterns = [
        # Philosophy and wisdom
        r'\b(wisdom|philosophy|meaning|purpose|truth|reality|consciousness|existence|being|identity)\b',
        r'\b(ethics|moral|values|principles|virtue|character|integrity|authenticity)\b',
        r'\b(understanding|insight|perspective|awareness|mindfulness|reflection|contemplation)\b',
        
        # Learning and growth
        r'\b(learn|education|knowledge|study|research|explore|discover|understand)\b',
        r'\b(growth|development|improvement|progress|evolution|transformation)\b',
        r'\b(skill|ability|talent|expertise|mastery|competence|capability)\b',
        
        # Relationships and communication
        r'\b(relationship|friendship|love|trust|respect|empathy|compassion|kindness)\b',
        r'\b(communication|conversation|dialogue|discussion|listening|understanding)\b',
        r'\b(community|society|culture|humanity|connection|bond|network)\b',
        
        # Creativity and innovation
        r'\b(creative|creativity|imagination|innovation|inspiration|artistic|design)\b',
        r'\b(idea|concept|vision|dream|possibility|potential|future)\b',
        
        # Psychology and human behavior
        r'\b(psychology|behavior|emotion|feeling|thought|mind|brain|cognitive)\b',
        r'\b(motivation|drive|passion|purpose|goal|ambition|desire)\b',
        r'\b(happiness|joy|satisfaction|fulfillment|contentment|peace)\b',
        
        # Success and achievement
        r'\b(success|achievement|accomplishment|goal|objective|target|mission)\b',
        r'\b(leadership|influence|impact|change|difference|contribution)\b',
        
        # Health and wellness
        r'\b(health|wellness|fitness|nutrition|exercise|meditation|balance)\b',
        r'\b(healing|recovery|therapy|support|care|comfort|relief)\b',
        
        # Life and experience
        r'\b(experience|journey|adventure|challenge|opportunity|choice|decision)\b',
        r'\b(time|moment|present|future|past|memory|history|legacy)\b'
    ]
    
    text_lower = text.lower()
    for pattern in meaningful_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    
    # Also consider longer, thoughtful responses as potentially meaningful
    if len(text) > 100 and ('?' in text or '.' in text):
        return True
    
    return False

def categorize_dialogue(user_text, ai_text):
    """Categorize a dialogue pair into thematic categories"""
    combined_text = (user_text + " " + ai_text).lower()
    
    categories = {
        'wisdom_and_philosophy': [
            r'\b(wisdom|philosophy|meaning|purpose|truth|reality|consciousness|existence|being|identity|ethics|moral|values|principles|virtue|character|integrity|authenticity|understanding|insight|perspective|awareness|mindfulness|reflection|contemplation)\b'
        ],
        'learning_and_education': [
            r'\b(learn|education|knowledge|study|research|explore|discover|understand|growth|development|improvement|progress|evolution|transformation|skill|ability|talent|expertise|mastery|competence|capability)\b'
        ],
        'relationship_and_communication': [
            r'\b(relationship|friendship|love|trust|respect|empathy|compassion|kindness|communication|conversation|dialogue|discussion|listening|understanding|community|society|culture|humanity|connection|bond|network)\b'
        ],
        'creativity_and_innovation': [
            r'\b(creative|creativity|imagination|innovation|inspiration|artistic|design|idea|concept|vision|dream|possibility|potential|future)\b'
        ],
        'psychology_and_behavior': [
            r'\b(psychology|behavior|emotion|feeling|thought|mind|brain|cognitive|motivation|drive|passion|purpose|goal|ambition|desire|happiness|joy|satisfaction|fulfillment|contentment|peace)\b'
        ],
        'success_and_achievement': [
            r'\b(success|achievement|accomplishment|goal|objective|target|mission|leadership|influence|impact|change|difference|contribution)\b'
        ],
        'health_and_wellness': [
            r'\b(health|wellness|fitness|nutrition|exercise|meditation|balance|healing|recovery|therapy|support|care|comfort|relief)\b'
        ],
        'life_and_experience': [
            r'\b(experience|journey|adventure|challenge|opportunity|choice|decision|time|moment|present|future|past|memory|history|legacy)\b'
        ],
        'problem_solving': [
            r'\b(problem|solution|solve|answer|approach|method|strategy|technique|way|how|what|why|question|issue|challenge|difficulty)\b'
        ]
    }
    
    for category, patterns in categories.items():
        for pattern in patterns:
            if re.search(pattern, combined_text, re.IGNORECASE):
                return category
    
    return 'general_insights'

def extract_dialogues(file_path):
    """Extract and categorize dialogues from the panacea file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    lines = content.split('\n')
    dialogues = []
    current_user = ""
    current_ai = ""
    state = "looking_for_user"
    
    for line in lines:
        line = line.strip()
        
        if line == "User":
            if state == "looking_for_ai" and current_user and current_ai:
                # Save the previous dialogue pair
                dialogues.append((current_user.strip(), current_ai.strip()))
            current_user = ""
            current_ai = ""
            state = "reading_user"
        elif line == "AI":
            state = "reading_ai"
        elif state == "reading_user":
            current_user += line + "\n"
        elif state == "reading_ai":
            current_ai += line + "\n"
            state = "looking_for_ai"
    
    # Don't forget the last dialogue if it exists
    if current_user and current_ai:
        dialogues.append((current_user.strip(), current_ai.strip()))
    
    print(f"📚 Found {len(dialogues)} dialogue pairs")
    
    # Process and categorize dialogues
    categorized_dialogues = {
        'wisdom_and_philosophy': [],
        'learning_and_education': [],
        'relationship_and_communication': [],
        'creativity_and_innovation': [],
        'psychology_and_behavior': [],
        'success_and_achievement': [],
        'health_and_wellness': [],
        'life_and_experience': [],
        'problem_solving': [],
        'general_insights': []
    }
    
    stats = {
        'total_processed': 0,
        'meaningful': 0,
        'coding_excluded': 0,
        'negative_excluded': 0,
        'low_value_excluded': 0
    }
    
    for i, (user_text, ai_text) in enumerate(dialogues):
        stats['total_processed'] += 1
        
        # Skip if either part is too short to be meaningful
        if len(user_text) < 10 or len(ai_text) < 10:
            stats['low_value_excluded'] += 1
            continue
        
        # Skip coding content
        if is_coding_content(user_text) or is_coding_content(ai_text):
            stats['coding_excluded'] += 1
            continue
        
        # Skip negative content
        if is_negative_content(user_text) or is_negative_content(ai_text):
            stats['negative_excluded'] += 1
            continue
        
        # Include if it's meaningful OR if it's a substantial dialogue
        is_user_meaningful = is_meaningful_content(user_text)
        is_ai_meaningful = is_meaningful_content(ai_text)
        is_substantial = len(user_text) > 50 and len(ai_text) > 50
        
        if is_user_meaningful or is_ai_meaningful or is_substantial:
            stats['meaningful'] += 1
            category = categorize_dialogue(user_text, ai_text)
            categorized_dialogues[category].append({
                'dialogue_id': i + 1,
                'user': user_text,
                'ai': ai_text
            })
        else:
            stats['low_value_excluded'] += 1
    
    return categorized_dialogues, stats

def save_categorized_content(categorized_dialogues, stats, output_dir):
    """Save categorized content to files"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Create summary
    summary_content = f"""# Panacea Content Extraction Summary

## Statistics

- **Total dialogues processed:** {stats['total_processed']}
- **Meaningful content extracted:** {stats['meaningful']}
- **Coding content excluded:** {stats['coding_excluded']}
- **Negative content excluded:** {stats['negative_excluded']}
- **Low-value content excluded:** {stats['low_value_excluded']}

## Categories Found

"""
    
    category_names = {
        'wisdom_and_philosophy': 'Wisdom And Philosophy',
        'learning_and_education': 'Learning And Education',
        'relationship_and_communication': 'Relationship And Communication',
        'creativity_and_innovation': 'Creativity And Innovation',
        'psychology_and_behavior': 'Psychology And Behavior',
        'success_and_achievement': 'Success And Achievement',
        'health_and_wellness': 'Health And Wellness',
        'life_and_experience': 'Life And Experience',
        'problem_solving': 'Problem Solving',
        'general_insights': 'General Insights'
    }
    
    for category, dialogues in categorized_dialogues.items():
        if dialogues:
            category_display = category_names.get(category, category.replace('_', ' ').title())
            summary_content += f"- **{category_display}:** {len(dialogues)} dialogues\n"
    
    with open(output_path / "extraction_summary.md", "w", encoding="utf-8") as f:
        f.write(summary_content)
    
    # Save each category
    for category, dialogues in categorized_dialogues.items():
        if dialogues:
            category_display = category_names.get(category, category.replace('_', ' ').title())
            content = f"# {category_display}\n\n"
            
            for dialogue in dialogues:
                content += f"## Dialogue {dialogue['dialogue_id']}\n\n"
                content += f"**User:**\n{dialogue['user']}\n\n"
                content += f"**AI:**\n{dialogue['ai']}\n\n"
                content += "---\n\n"
            
            filename = f"{category}.md"
            with open(output_path / filename, "w", encoding="utf-8") as f:
                f.write(content)
    
    return output_path

def main():
    input_file = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea/panacea_1.md"
    output_dir = "/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea/extracted_categories"
    
    print("🚀 Starting improved content extraction...")
    
    categorized_dialogues, stats = extract_dialogues(input_file)
    
    print(f"\n📊 Processing Results:")
    print(f"✅ Meaningful content: {stats['meaningful']}")
    print(f"❌ Coding content excluded: {stats['coding_excluded']}")
    print(f"❌ Negative content excluded: {stats['negative_excluded']}")
    print(f"❌ Low-value content excluded: {stats['low_value_excluded']}")
    
    output_path = save_categorized_content(categorized_dialogues, stats, output_dir)
    
    print(f"\n🎯 Categories with content:")
    category_names = {
        'wisdom_and_philosophy': 'Wisdom And Philosophy',
        'learning_and_education': 'Learning And Education',
        'relationship_and_communication': 'Relationship And Communication',
        'creativity_and_innovation': 'Creativity And Innovation',
        'psychology_and_behavior': 'Psychology And Behavior',
        'success_and_achievement': 'Success And Achievement',
        'health_and_wellness': 'Health And Wellness',
        'life_and_experience': 'Life And Experience',
        'problem_solving': 'Problem Solving',
        'general_insights': 'General Insights'
    }
    
    for category, dialogues in categorized_dialogues.items():
        if dialogues:
            category_display = category_names.get(category, category.replace('_', ' ').title())
            print(f"{category_display}: {len(dialogues)} dialogues")
    
    print(f"\n✅ Content saved to: {output_path}")
    print("🎉 Extraction complete!")

if __name__ == "__main__":
    main()
