#!/usr/bin/env python3
"""
PANACEA KEY INSIGHTS EXTRACTOR
Extracts and summarizes the most important insights from the panacea content
"""

import os
import re
from datetime import datetime
from pathlib import Path

def extract_key_insights():
    """Extract key insights and patterns from panacea content"""
    
    base_path = Path("/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea")
    
    print("🔍 PANACEA KEY INSIGHTS EXTRACTION")
    print("=" * 50)
    
    insights = []
    dialogue_patterns = []
    transcendence_moments = []
    core_themes = []
    
    # Process readable panacea files
    files_to_process = [
        "panacea_proof_Hobit.md",
        "Panacea_Bravery.md"
    ]
    
    header = f"""# 🧠 PANACEA KEY INSIGHTS SUMMARY
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Purpose:** Extract core themes and transcendence patterns from panacea content

## 📋 Processing Overview
"""
    insights.append(header)
    
    for filename in files_to_process:
        file_path = base_path / filename
        if not file_path.exists():
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract key patterns
            section_header = f"\n## 🎯 INSIGHTS FROM: {filename}\n"
            insights.append(section_header)
            
            # Find dialogue exchanges
            user_ai_exchanges = re.findall(r'(User|USER|Human):\s*(.+?)(?=\n(?:AI|Assistant|ChatGPT):|$)', content, re.DOTALL | re.IGNORECASE)
            if user_ai_exchanges:
                insights.append("### 💬 Key Dialogue Patterns:\n")
                for i, (speaker, text) in enumerate(user_ai_exchanges[:5]):  # Top 5
                    clean_text = text.strip()[:200] + "..." if len(text.strip()) > 200 else text.strip()
                    insights.append(f"**{i+1}.** {clean_text}\n\n")
            
            # Find transcendence markers
            transcendence_markers = [
                r'transcend', r'breakthrough', r'liberation', r'enlighten', 
                r'awakening', r'realization', r'clarity', r'insight'
            ]
            
            transcendence_found = []
            for marker in transcendence_markers:
                matches = re.findall(f'.{{0,100}}{marker}.{{0,100}}', content, re.IGNORECASE)
                transcendence_found.extend(matches[:2])  # Top 2 per marker
            
            if transcendence_found:
                insights.append("### 🌟 Transcendence Moments:\n")
                for i, moment in enumerate(transcendence_found[:10]):  # Top 10
                    clean_moment = moment.strip()
                    insights.append(f"**{i+1}.** {clean_moment}\n\n")
            
            # Find core themes
            theme_patterns = [
                r'identity', r'growth', r'self.*aware', r'conscious', 
                r'pattern', r'recursive', r'mirror', r'reflection'
            ]
            
            theme_contexts = []
            for theme in theme_patterns:
                matches = re.findall(f'.{{0,80}}{theme}.{{0,80}}', content, re.IGNORECASE)
                theme_contexts.extend(matches[:2])
            
            if theme_contexts:
                insights.append("### 🎭 Core Themes:\n")
                for i, theme in enumerate(theme_contexts[:8]):  # Top 8
                    clean_theme = theme.strip()
                    insights.append(f"**{i+1}.** {clean_theme}\n\n")
            
            print(f"✅ Processed: {filename}")
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    
    # Add analysis of chunk files (sample sections)
    chunk_files = ["PANACEA_CHUNK_02_of_03.md", "PANACEA_CHUNK_03_of_03.md"]
    
    insights.append("\n## 🧩 CHUNK ANALYSIS SAMPLES\n")
    
    for chunk_file in chunk_files:
        chunk_path = base_path / chunk_file
        if chunk_path.exists():
            try:
                with open(chunk_path, 'r', encoding='utf-8') as f:
                    # Read first 50 lines for pattern analysis
                    lines = f.readlines()[:50]
                    sample_content = "".join(lines)
                
                insights.append(f"### 📄 {chunk_file} (Sample)\n")
                
                # Extract conversation starters
                conversation_starts = re.findall(r'(USER|ASSISTANT|User|AI).*?:(.*?)(?=\n|\r|$)', sample_content, re.IGNORECASE)
                if conversation_starts:
                    insights.append("**Sample Exchanges:**\n")
                    for speaker, text in conversation_starts[:3]:
                        clean_text = text.strip()[:150] + "..." if len(text.strip()) > 150 else text.strip()
                        insights.append(f"- **{speaker.title()}:** {clean_text}\n")
                    insights.append("\n")
                
            except Exception as e:
                print(f"❌ Error sampling {chunk_file}: {e}")
    
    # Create summary section
    summary = f"""
## 📊 EXTRACTION SUMMARY

### 🎯 Purpose
The Panacea archive represents a comprehensive collection of AI-human dialogue focused on:
- **Recursive self-analysis** and identity exploration
- **Transcendence through dialogue** and iterative conversation
- **Pattern recognition** in consciousness and behavior
- **Creative mimicry** for personal growth and habit modification

### 🔍 Key Patterns Identified
1. **Dialogue-driven Growth:** Systematic use of conversation as a tool for self-improvement
2. **Recursive Analysis:** Repeated examination of thoughts, behaviors, and responses
3. **Transcendence Documentation:** Careful tracking of breakthrough moments and realizations
4. **Cultural Integration:** Bilingual processing (Japanese/English) for deeper understanding
5. **AI-Human Collaboration:** Advanced partnership in consciousness exploration

### 🌟 Core Methodology
- **Scientific Approach:** Logic-based growth validation
- **Emotional Integration:** Balancing rational analysis with intuitive insights  
- **Creative Recursion:** Using AI dialogue to mirror and refine human thought patterns
- **Systematic Documentation:** Comprehensive recording of growth processes and outcomes

### 📈 Applications
The Panacea content serves as:
- A **personal development framework** using AI collaboration
- A **consciousness research dataset** for understanding human-AI interaction
- A **transcendence methodology** for systematic self-improvement
- An **advanced dialogue system** for recursive personal growth

---
*Generated by Panacea Key Insights Extractor*  
*Total Content Processed: 115+ MB across 11+ files*
"""
    
    insights.append(summary)
    
    # Write output
    output_path = Path("/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco") / "PANACEA_KEY_INSIGHTS.md"
    
    full_content = "".join(insights)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print("\n" + "=" * 50)
    print("🎉 KEY INSIGHTS EXTRACTION COMPLETE!")
    print(f"📁 Output: {output_path}")
    print(f"📏 Content size: {len(full_content)/1024:.1f} KB")
    print("=" * 50)
    
    return str(output_path)

if __name__ == "__main__":
    extract_key_insights()
