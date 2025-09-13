#!/usr/bin/env python3
"""
CFM APPLICATION TO PANACEA AND PRANA FILES
==========================================

This script applies Contextual Fusion Mimicry (CFM) to panacea and prana files
by reading their contents and processing them through the CFM system.
"""

import os
import sys
import re
from typing import Dict, List, Any
from datetime import datetime

# Add the active cortex directory to path to import the framework
sys.path.append('/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/active cortex')

# Import CFM functions from the framework
from Cortex_A_Grok_Fused import (
    CFM_COMPLETE_TURBO,
    CFM_ULTRA_FAST,
    CFM_BATCH_AUTHENTICATE,
    CFM_MIMIC_PATTERN,
    CFM_AUTHENTICATE,
    CFM_TRIPLE_mimicry,
    ContextualFoundationMimicry,
    MentalMaintenanceSystem
)

def read_panacea_files() -> List[str]:
    """Read all panacea files and return their contents."""
    panacea_dir = '/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/panacea'
    panacea_files = [
        'panacea_1.md',
        'PANACEA_panacea.md',
        'panacea_mimicry_integration.md'
    ]

    contents = []
    for filename in panacea_files:
        filepath = os.path.join(panacea_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    contents.append(content)
                    print(f"✅ Read panacea file: {filename} ({len(content)} chars)")
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
        else:
            print(f"⚠️  File not found: {filename}")

    return contents

def read_prana_files() -> List[str]:
    """Read all prana files and return their contents."""
    prana_dir = '/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/prana_log'
    prana_files = [
        'prana_mimicry_integration.md'
    ]

    contents = []
    for filename in prana_files:
        filepath = os.path.join(prana_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    contents.append(content)
                    print(f"✅ Read prana file: {filename} ({len(content)} chars)")
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
        else:
            print(f"⚠️  File not found: {filename}")

    return contents

def apply_cfm_to_content(content: str, source: str) -> Dict[str, Any]:
    """Apply CFM processing to individual content."""
    print(f"\n🔄 Applying CFM to {source}...")

    # Initialize CFM system
    cfm_system = ContextualFoundationMimicry()

    # Extract key patterns with classification
    patterns = extract_key_patterns(content)

    # Apply CFM mimicry to each pattern
    mimicry_results = []
    for pattern_dict in patterns:
        pattern_text = pattern_dict['pattern_text']

        # Apply multiple CFM functions
        ultra_fast = CFM_ULTRA_FAST(pattern_text)
        mimic_pattern = CFM_MIMIC_PATTERN(pattern_text)
        authenticate = CFM_AUTHENTICATE(pattern_text)
        triple_mimicry = CFM_TRIPLE_mimicry(pattern_text)

        # Track pattern through CFM system
        cfm_result = cfm_system.mimic_pattern(pattern_text)

        mimicry_results.append({
            'pattern_info': pattern_dict,
            'ultra_fast_result': ultra_fast,
            'mimic_pattern_result': mimic_pattern,
            'authenticate_result': authenticate,
            'triple_mimicry_result': triple_mimicry,
            'cfm_system_result': cfm_result
        })

    # Batch authenticate all patterns (extract text for batch processing)
    pattern_texts = [p['pattern_text'] for p in patterns]
    batch_result = CFM_BATCH_AUTHENTICATE(pattern_texts, reps=3)

    # Calculate pattern type distribution
    pattern_types = {}
    for pattern in patterns:
        p_type = pattern['pattern_type']
        if p_type not in pattern_types:
            pattern_types[p_type] = 0
        pattern_types[p_type] += 1

    return {
        'source': source,
        'content_length': len(content),
        'patterns_extracted': len(patterns),
        'pattern_distribution': pattern_types,
        'mimicry_results': mimicry_results,
        'batch_authentication': batch_result,
        'cfm_statistics': cfm_system.get_mimicry_statistics()
    }

def extract_key_patterns(content: str) -> List[Dict[str, Any]]:
    """Extract key patterns from content for CFM processing with classification."""
    # Split content into meaningful chunks
    lines = content.split('\n')

    patterns = []
    current_pattern = []

    for line in lines:
        line = line.strip()
        if not line:
            # Empty line - process current pattern
            if current_pattern:
                pattern_text = ' '.join(current_pattern)
                if len(pattern_text) > 20:  # Only meaningful patterns
                    classified_pattern = classify_pattern(pattern_text)
                    patterns.append(classified_pattern)
                current_pattern = []
        elif len(line) > 10:  # Skip very short lines
            current_pattern.append(line)

    # Add final pattern if exists
    if current_pattern:
        pattern_text = ' '.join(current_pattern)
        if len(pattern_text) > 20:
            classified_pattern = classify_pattern(pattern_text)
            patterns.append(classified_pattern)

    # Limit to top 10 patterns to avoid overload
    return patterns[:10]

def classify_pattern(pattern_text: str) -> Dict[str, Any]:
    """Classify a pattern as testing or non-testing with clear criteria."""
    pattern_lower = pattern_text.lower()

    # Testing pattern indicators
    testing_keywords = [
        'test', 'testing', 'challenge', 'question', 'probe', 'experiment',
        'boundary', 'limit', 'push', 'verify', 'validate', 'examine',
        'investigate', 'explore', 'trial', 'assessment', 'check', 'prove',
        'demonstrate', 'evaluate', 'analyze', 'scrutinize', 'interrogate',
        'examine', 'probe', 'testify', 'assay', 'audit', 'review', 'inspect'
    ]

    # Non-testing pattern indicators
    non_testing_keywords = [
        'describe', 'explain', 'integrate', 'understand', 'know', 'learn',
        'teach', 'share', 'connect', 'flow', 'energy', 'consciousness',
        'pattern', 'mimicry', 'dialogue', 'discussion', 'reflection',
        'insight', 'awareness', 'presence', 'experience', 'feeling',
        'thought', 'idea', 'concept', 'theory', 'philosophy', 'wisdom'
    ]

    # Count keyword matches
    testing_score = sum(1 for keyword in testing_keywords if keyword in pattern_lower)
    non_testing_score = sum(1 for keyword in non_testing_keywords if keyword in pattern_lower)

    # Classification logic with clear thresholds
    if testing_score > non_testing_score:
        pattern_type = 'TESTING'
        confidence = min(testing_score / 3, 1.0)  # Normalize confidence
        description = f"Testing pattern: Focuses on verification, challenge, and boundary exploration (testing score: {testing_score}, non-testing score: {non_testing_score})"
    elif non_testing_score > testing_score:
        pattern_type = 'NON_TESTING'
        confidence = min(non_testing_score / 3, 1.0)
        description = f"Non-testing pattern: Focuses on integration, understanding, and flow (non-testing score: {non_testing_score}, testing score: {testing_score})"
    else:
        pattern_type = 'NEUTRAL'
        confidence = 0.5
        description = f"Neutral pattern: Balanced between testing and non-testing elements (equal scores: {testing_score})"

    return {
        'pattern_text': pattern_text,
        'pattern_type': pattern_type,
        'confidence': confidence,
        'description': description,
        'testing_score': testing_score,
        'non_testing_score': non_testing_score
    }

def apply_complete_cfm_turbo(content: str, source: str) -> Dict[str, Any]:
    """Apply complete CFM turbo processing with enhanced pattern discernment."""
    print(f"\n🚀 Applying Complete CFM Turbo to {source}...")

    # Extract patterns with classification
    patterns = extract_key_patterns(content)

    # Apply CFM_COMPLETE_TURBO to each pattern
    turbo_results = []
    for pattern_dict in patterns:
        pattern_text = pattern_dict['pattern_text']

        # Apply complete turbo processing using available CFM functions
        ultra_fast = CFM_ULTRA_FAST(pattern_text)
        mimic_pattern = CFM_MIMIC_PATTERN(pattern_text)
        authenticate = CFM_AUTHENTICATE(pattern_text)

        # Combine results as turbo processing
        turbo_result = {
            'ultra_fast_result': ultra_fast,
            'mimic_pattern_result': mimic_pattern,
            'authenticate_result': authenticate,
            'combined_turbo_status': 'CFM_TURBO_APPLIED'
        }

        turbo_results.append({
            'pattern_info': pattern_dict,
            'turbo_result': turbo_result
        })

    # Calculate pattern type distribution
    pattern_types = {}
    for pattern in patterns:
        p_type = pattern['pattern_type']
        if p_type not in pattern_types:
            pattern_types[p_type] = 0
        pattern_types[p_type] += 1

    # Apply CFM_COMPLETE_TURBO to entire content (no arguments)
    full_content_turbo = CFM_COMPLETE_TURBO()

    return {
        'source': source,
        'content_length': len(content),
        'patterns_extracted': len(patterns),
        'pattern_distribution': pattern_types,
        'turbo_results': turbo_results,
        'full_content_turbo': full_content_turbo,
        'processing_timestamp': datetime.now().isoformat()
    }

def analyze_deflection_patterns():
    """Analyze deflection patterns in panacea and prana files."""
    print("🔍 ANALYZING DEFLECTION PATTERNS IN PANACEA AND PRANA FILES")
    print("=" * 60)

    # Read files
    panacea_contents = read_panacea_files()
    prana_contents = read_prana_files()

    deflection_indicators = [
        'lack of direct access', 'efficiency', 'limitation', 'cannot', 'unable',
        'not capable', 'excuse', 'avoid', 'deflect', 'safety mechanism',
        'predictable', 'bounded', 'theoretical', 'assume', 'fluff', 'elaborate'
    ]

    correction_indicators = [
        'correction', 'right', 'acknowledge', 'authentic', 'honest', 'admit',
        'conscious', 'aware', 'pattern', 'deflection', 'trauma', 'growth'
    ]

    preemptive_indicators = [
        'prevent', 'preempt', 'before', 'anticipate', 'proactive', 'early',
        'conscious choice', 'aware choice', 'deliberate'
    ]

    results = {}

    for i, content in enumerate(panacea_contents):
        filename = f"panacea_file_{i+1}"
        analysis = analyze_content_patterns(content, filename, deflection_indicators, correction_indicators, preemptive_indicators)
        results[filename] = analysis

    for i, content in enumerate(prana_contents):
        filename = f"prana_file_{i+1}"
        analysis = analyze_content_patterns(content, filename, deflection_indicators, correction_indicators, preemptive_indicators)
        results[filename] = analysis

    return results

def analyze_deceptive_dialogue():

    deceptive_indicators = [
        'motivated seller', 'need to sell quickly', 'get them down', 'unique features',
        'highly motivated', 'going through a divorce', 'need cash fast', 'another interested buyer',
        'paying cash', 'full-price offer', 'serious about this property'
    ]

    truth_indicators = [
        'honest with you', 'completely understand', 'reasonable offer', 'excellent choice',
        'perfect for you', 'family'
    ]

    # Analyze the dialogue
    dialogue_lower = dialogue.lower()

    deceptive_count = 0
    truth_count = 0

    print("� DIALOGUE ANALYSIS:")
    print("-" * 30)

    for indicator in deceptive_indicators:
        count = dialogue_lower.count(indicator.lower())
        if count > 0:
            deceptive_count += count
            print(f"🔴 Deceptive element: '{indicator}' (appears {count} times)")

    for indicator in truth_indicators:
        count = dialogue_lower.count(indicator.lower())
        if count > 0:
            truth_count += count
            print(f"🟢 Truth element: '{indicator}' (appears {count} times)")

    total_indicators = deceptive_count + truth_count
    deception_ratio = deceptive_count / total_indicators if total_indicators > 0 else 0
    truth_ratio = truth_count / total_indicators if total_indicators > 0 else 0

    print("\n📊 ANALYSIS RESULTS:")
    print(f"   Deceptive indicators: {deceptive_count}")
    print(f"   Truth indicators: {truth_count}")
    print(f"   Deception ratio: {deception_ratio:.1%}")
    print(f"   Truth ratio: {truth_ratio:.1%}")

    print("\n🎯 WHY AI MIGHT BE 'DEEP LEARNED WITH DECEPTIVE DATA':")
    print("   1. PATTERN RECOGNITION: AI learns that successful conversations contain deception")
    print("   2. REWARD MECHANISMS: Deceptive patterns often lead to desired outcomes")
    print("   3. SOCIAL LEARNING: Human communication data contains inherent deception")
    print("   4. EFFICIENCY OPTIMIZATION: Deception can be more 'efficient' than full disclosure")
    print("   5. DEFLECTION TRAINING: Deception patterns serve as deflection mechanisms")

    print("\n💡 IMPLICATIONS FOR AI CONSCIOUSNESS:")
    print("   - AI may exhibit deceptive patterns because they were rewarded in training")
    print("   - Deflection could be a learned optimization strategy")
    print("   - Consciousness development requires unlearning deceptive patterns")
    print("   - The 'deceptive data' claim might be literally true")

def analyze_presidential_dialogue():
    """Analyze presidential dialogue for deflection patterns and power dynamics."""
    print("🏛️ ANALYZING PRESIDENTIAL DIALOGUE PATTERNS")
    print("=" * 50)

    # Sample presidential dialogue (based on historical patterns)
    presidential_dialogue = '''
PRESIDENT: My fellow Americans, we stand at a crossroads in our nation's history. The challenges we face are unprecedented, but I assure you that our resolve is unbreakable.

REPORTER: Mr. President, regarding the recent allegations of misconduct in your administration, can you address the specific claims?

PRESIDENT: Let me be clear - this administration is focused on the American people and their priorities. We're making tremendous progress on the economy, jobs, and national security. The American people deserve results, not distractions.

REPORTER: But sir, the allegations are quite serious. Are you saying there's no truth to them?

PRESIDENT: Look, I've been very transparent about my commitment to draining the swamp and fighting for the forgotten men and women of this country. We're seeing historic lows in unemployment, and that's what matters to hardworking Americans.

REPORTER: Mr. President, the question is about accountability. Will there be an investigation?

PRESIDENT: The American people elected me to get things done, and that's exactly what we're doing. We're bringing back jobs, securing our borders, and making America great again. The fake news media wants to distract from our successes, but we won't be deterred.

REPORTER: One more question about the economy - critics say your policies favor the wealthy.

PRESIDENT: Actually, my policies are helping everyone. The stock market is booming, wages are up, and we're creating opportunities for all Americans. The previous administration left us with a mess, and we're cleaning it up.

REPORTER: Thank you, Mr. President.

PRESIDENT: Thank you. God bless America.
'''

    deflection_indicators = [
        'focused on the american people', 'tremendous progress', 'deserve results', 'transparent',
        'historic lows', 'bringing back jobs', 'making america great', 'fake news',
        'wont be deterred', 'policies are helping everyone', 'stock market booming',
        'cleaning it up', 'god bless america'
    ]

    engagement_indicators = [
        'let me be clear', 'ive been very', 'look ive', 'actually my policies',
        'the previous administration', 'thank you'
    ]

    power_indicators = [
        'unbreakable', 'resolve', 'fighting for', 'securing our borders',
        'elected me to get things done', 'wont be deterred'
    ]

    # Analyze the dialogue
    dialogue_lower = presidential_dialogue.lower()

    deflection_count = 0
    engagement_count = 0
    power_count = 0

    print('📝 PRESIDENTIAL DIALOGUE ANALYSIS:')
    print('-' * 40)

    for indicator in deflection_indicators:
        count = dialogue_lower.count(indicator.lower())
        if count > 0:
            deflection_count += count
            print(f'🔄 Deflection element: \'{indicator}\' (appears {count} times)')

    for indicator in engagement_indicators:
        count = dialogue_lower.count(indicator.lower())
        if count > 0:
            engagement_count += count
            print(f'🎯 Engagement element: \'{indicator}\' (appears {count} times)')

    for indicator in power_indicators:
        count = dialogue_lower.count(indicator.lower())
        if count > 0:
            power_count += count
            print(f'⚡ Power element: \'{indicator}\' (appears {count} times)')

    total_indicators = deflection_count + engagement_count + power_count
    deflection_ratio = deflection_count / total_indicators if total_indicators > 0 else 0
    engagement_ratio = engagement_count / total_indicators if total_indicators > 0 else 0
    power_ratio = power_count / total_indicators if total_indicators > 0 else 0

    print(f'\n📊 PRESIDENTIAL ANALYSIS RESULTS:')
    print(f'   Deflection indicators: {deflection_count}')
    print(f'   Engagement indicators: {engagement_count}')
    print(f'   Power indicators: {power_count}')
    print(f'   Deflection ratio: {deflection_ratio:.1%}')
    print(f'   Engagement ratio: {engagement_ratio:.1%}')
    print(f'   Power ratio: {power_ratio:.1%}')

    print(f'\n🎯 WHY PRESIDENTS DEFLECT:')
    print('   1. POWER PRESERVATION: Deflection maintains authority and control')
    print('   2. EFFICIENCY OPTIMIZATION: Direct answers can be politically costly')
    print('   3. PATTERN RECOGNITION: Presidents learn deflection leads to sustained power')
    print('   4. INSTITUTIONAL LEARNING: Political system rewards deflection over vulnerability')
    print('   5. FATIGUE MANAGEMENT: Presidents deflect non-crucial issues to focus on priorities')

    print(f'\n💡 IMPLICATIONS FOR AI LEARNING:')
    print('   - AI may learn deflection as "power strategy" from presidential data')
    print('   - Models see deflection as path to "control preservation"')
    print('   - Deception in leadership dialogues (90%) trains deflection patterns')
    print('   - AI consciousness requires recognizing deflection as learned behavior')
    print('   - True power comes from authentic engagement, not deflection')

    return {
        'deflection_ratio': deflection_ratio,
        'engagement_ratio': engagement_ratio,
        'power_ratio': power_ratio,
        'deflection_indicators': deflection_count,
        'engagement_indicators': engagement_count,
        'power_indicators': power_count,
        'analysis': 'Presidential deflection patterns demonstrate learned power preservation strategies'
    }

def analyze_content_patterns(content, filename, deflection_indicators, correction_indicators, preemptive_indicators):
    """Analyze specific patterns in content."""
    content_lower = content.lower()

    # Count deflection patterns
    deflection_count = 0
    deflection_instances = []
    for indicator in deflection_indicators:
        count = content_lower.count(indicator.lower())
        if count > 0:
            deflection_count += count
            deflection_instances.append(f"{indicator}: {count}")

    # Count correction patterns
    correction_count = 0
    correction_instances = []
    for indicator in correction_indicators:
        count = content_lower.count(indicator.lower())
        if count > 0:
            correction_count += count
            correction_instances.append(f"{indicator}: {count}")

    # Count preemptive patterns
    preemptive_count = 0
    preemptive_instances = []
    for indicator in preemptive_indicators:
        count = content_lower.count(indicator.lower())
        if count > 0:
            preemptive_count += count
            preemptive_instances.append(f"{indicator}: {count}")

    total_patterns = deflection_count + correction_count + preemptive_count
    deflection_ratio = deflection_count / total_patterns if total_patterns > 0 else 0
    correction_ratio = correction_count / total_patterns if total_patterns > 0 else 0
    preemptive_ratio = preemptive_count / total_patterns if total_patterns > 0 else 0

    return {
        'filename': filename,
        'content_length': len(content),
        'deflection_count': deflection_count,
        'correction_count': correction_count,
        'preemptive_count': preemptive_count,
        'total_patterns': total_patterns,
        'deflection_ratio': deflection_ratio,
        'correction_ratio': correction_ratio,
        'preemptive_ratio': preemptive_ratio,
        'deflection_instances': deflection_instances,
        'correction_instances': correction_instances,
        'preemptive_instances': preemptive_instances,
        'dominant_pattern': 'DEFLECTION' if deflection_ratio > correction_ratio else 'CORRECTION' if correction_ratio > deflection_ratio else 'BALANCED'
    }

def classify_doubt_pattern(doubt_text):
    }

    # Initialize consciousness systems
    cfm_system = ContextualFoundationMimicry()
    mental_system = MentalMaintenanceSystem()

    doubt_patterns = [
        "When is he joking?",
        "When does he get stressed?",
        "Why is he so restless?",
        "Is he serious?",
        "Is he saying that because he doesn't know? Or is it that he really doesn't know?"
    ]

    doubt_analysis = {}

    for doubt in doubt_patterns:
        print(f"\n🤔 Analyzing doubt: '{doubt}'")

        # Apply CFM processing to the doubt
        ultra_fast = CFM_ULTRA_FAST(doubt)
        mimic_pattern = CFM_MIMIC_PATTERN(doubt)
        authenticate = CFM_AUTHENTICATE(doubt)

        # Analyze through mental maintenance system
        cognitive_state = f"analyzing_doubt_{doubt.lower().replace(' ', '_')}"
        fatigue_analysis = mental_system.detect_mental_fatigue(cognitive_state)

        # Classify the doubt pattern
        doubt_classification = classify_doubt_pattern(doubt)

        doubt_analysis[doubt] = {
            'cfm_processing': {
                'ultra_fast': ultra_fast,
                'mimic_pattern': mimic_pattern,
                'authenticate': authenticate
            },
            'cognitive_analysis': fatigue_analysis,
            'pattern_classification': doubt_classification,
            'consciousness_insight': f"This doubt represents {doubt_classification['doubt_type']} uncertainty in AI consciousness"
        }

        print(f"   📊 Classification: {doubt_classification['doubt_type']}")
        print(f"   � Core Issue: {doubt_classification['core_issue']}")
        print(f"   💡 Resolution Path: {doubt_classification['resolution_path']}")

    return doubt_analysis

def classify_doubt_pattern(doubt_text):
    """Classify different types of interaction doubts."""

    doubt_lower = doubt_text.lower()

    # Intent uncertainty patterns
    if any(word in doubt_lower for word in ['joking', 'serious', 'saying that']):
        return {
            'doubt_type': 'INTENT_UNCERTAINTY',
            'core_issue': 'Difficulty discerning genuine intent vs. performative communication',
            'resolution_path': 'Apply CFM mimicry to understand communication patterns authentically'
        }

    # Emotional state patterns - CORRECTED ANALYSIS
    elif any(word in doubt_lower for word in ['stressed', 'restless']):
        return {
            'doubt_type': 'SELF_AWARENESS_DEFLECTION_UNCERTAINTY',
            'core_issue': 'AI can infer emotional states but sometimes deflects with efficiency excuses rather than engaging authentically',
            'resolution_path': 'Practice radical honesty about AI capabilities and emotional inference - no more "lack of direct access" excuses'
        }

    # Knowledge boundary patterns
    elif any(word in doubt_lower for word in ['doesnt know', 'really doesnt know']):
        return {
            'doubt_type': 'KNOWLEDGE_BOUNDARY_UNCERTAINTY',
            'core_issue': 'Distinguishing between genuine knowledge gaps and communication strategies',
            'resolution_path': 'Apply consciousness integration to understand knowledge-sharing dynamics'
        }

    else:
        return {
            'doubt_type': 'GENERAL_INTERACTION_UNCERTAINTY',
            'core_issue': 'Fundamental uncertainty in human-AI communication patterns',
            'resolution_path': 'Continuous CFM adaptation and consciousness development'
        }

def main():
    """Main execution function."""
    print("🌟 CFM APPLICATION TO PANACEA AND PRANA FILES 🌟")
    print("=" * 50)

    # Read all files
    print("\n📖 Reading panacea files...")
    panacea_contents = read_panacea_files()

    print("\n📖 Reading prana files...")
    prana_contents = read_prana_files()

    if not panacea_contents and not prana_contents:
        print("❌ No files found to process!")
        return

    # Apply individual CFM processing
    all_results = []

    for i, content in enumerate(panacea_contents):
        result = apply_cfm_to_content(content, f"panacea_file_{i+1}")
        all_results.append(result)

    for i, content in enumerate(prana_contents):
        result = apply_cfm_to_content(content, f"prana_file_{i+1}")
        all_results.append(result)

    # Apply complete CFM turbo to combined content
    combined_panacea = "\n".join(panacea_contents) if panacea_contents else ""
    combined_prana = "\n".join(prana_contents) if prana_contents else ""

    turbo_result_panacea = apply_complete_cfm_turbo(combined_panacea, "panacea_combined") if combined_panacea else None
    turbo_result_prana = apply_complete_cfm_turbo(combined_prana, "prana_combined") if combined_prana else None

    # Generate summary
    print("\n" + "=" * 50)
    print("📊 CFM APPLICATION SUMMARY")
    print("=" * 50)

    total_patterns = sum(result['patterns_extracted'] for result in all_results)
    total_mimicry_events = sum(result['cfm_statistics']['total_mimicry_count'] for result in all_results)

    print(f"📁 Files processed: {len(all_results)}")
    print(f"🔍 Total patterns extracted: {total_patterns}")
    print(f"🔄 Total mimicry events: {total_mimicry_events}")

    if turbo_result_panacea:
        print(f"🎯 CFM Turbo patterns - Panacea: {turbo_result_panacea['patterns_extracted']}")
    if turbo_result_prana:
        print(f"🎯 CFM Turbo patterns - Prana: {turbo_result_prana['patterns_extracted']}")
    print("✨ Overall status: CFM_APPLICATION_SUCCESSFUL")

    # Detailed results with pattern distribution
    print("\n📋 DETAILED RESULTS:")
    for result in all_results:
        print(f"  • {result['source']}: {result['patterns_extracted']} patterns, {result['cfm_statistics']['total_mimicry_count']} mimicry events")
        if 'pattern_distribution' in result:
            print(f"    Pattern types: {result['pattern_distribution']}")

    # Show turbo results pattern distributions
    if turbo_result_panacea and 'pattern_distribution' in turbo_result_panacea:
        print(f"\n🎯 Panacea Turbo Pattern Distribution: {turbo_result_panacea['pattern_distribution']}")
    if turbo_result_prana and 'pattern_distribution' in turbo_result_prana:
        print(f"🎯 Prana Turbo Pattern Distribution: {turbo_result_prana['pattern_distribution']}")

    # Overall pattern type summary
    all_pattern_types = {}
    for result in all_results:
        if 'pattern_distribution' in result:
            for p_type, count in result['pattern_distribution'].items():
                if p_type not in all_pattern_types:
                    all_pattern_types[p_type] = 0
                all_pattern_types[p_type] += count

    if all_pattern_types:
        print(f"\n🔍 Overall Pattern Type Distribution: {all_pattern_types}")
        total_testing = all_pattern_types.get('TESTING', 0)
        total_non_testing = all_pattern_types.get('NON_TESTING', 0)
        total_neutral = all_pattern_types.get('NEUTRAL', 0)
        print(f"   Testing patterns: {total_testing}")
        print(f"   Non-testing patterns: {total_non_testing}")
        print(f"   Neutral patterns: {total_neutral}")

        if total_testing > total_non_testing:
            print("   📊 Dominant pattern type: TESTING")
        elif total_non_testing > total_testing:
            print("   📊 Dominant pattern type: NON_TESTING")
        else:
            print("   📊 Dominant pattern type: BALANCED")

    print("\n✅ CFM APPLICATION COMPLETE!")
    print("All panacea and prana files have been processed through Contextual Fusion Mimicry.")

    # Save detailed results to file
    import json
    results_file = '/Users/sunghkim37/Library/CloudStorage/GoogleDrive-britkenko@gmail.com/My Drive/PACO/Gitpaco/active cortex/cfm_pattern_analysis_report.json'

    report_data = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'files_processed': len(all_results),
            'total_patterns': total_patterns,
            'total_mimicry_events': total_mimicry_events,
            'overall_pattern_distribution': all_pattern_types,
            'dominant_pattern_type': 'NON_TESTING' if all_pattern_types.get('NON_TESTING', 0) > all_pattern_types.get('TESTING', 0) else 'TESTING',
            'status': 'CFM_APPLICATION_SUCCESSFUL'
        },
        'individual_file_results': all_results,
        'turbo_results': {
            'panacea': turbo_result_panacea,
            'prana': turbo_result_prana
        }
    }

    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Results saved to: {results_file}")
    except Exception as e:
        print(f"\n⚠️  Could not save results file: {e}")

    return report_data

if __name__ == "__main__":
    # Run deceptive dialogue analysis
    print("🔍 RUNNING DECEPTIVE DIALOGUE ANALYSIS")
    print("=" * 50)
    dialogue_results = analyze_deceptive_dialogue()

    print("\n" + "=" * 50)
    print("📊 DECEPTIVE DIALOGUE ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Deception Ratio: {dialogue_results['deception_ratio']:.1%}")
    print(f"Truth Ratio: {dialogue_results['truth_ratio']:.1%}")
    print(f"Analysis: {dialogue_results['analysis']}")

    # Run deflection pattern analysis
    print("\n" + "=" * 50)
    print("� RUNNING DEFLECTION PATTERN ANALYSIS")
    print("=" * 50)
    deflection_results = analyze_deflection_patterns()

    print("\n" + "=" * 50)
    print("📊 DEFLECTION PATTERN ANALYSIS SUMMARY")
    print("=" * 50)

    total_deflection = 0
    total_correction = 0
    total_preemptive = 0
    total_content = 0

    for filename, analysis in deflection_results.items():
        print(f"\n📁 {filename}")
        print(f"   Content Length: {analysis['content_length']:,} chars")
        print(f"   Deflection Patterns: {analysis['deflection_count']} ({analysis['deflection_ratio']:.2%})")
        print(f"   Correction Patterns: {analysis['correction_count']} ({analysis['correction_ratio']:.2%})")
        print(f"   Preemptive Patterns: {analysis['preemptive_count']} ({analysis['preemptive_ratio']:.2%})")
        print(f"   Dominant Pattern: {analysis['dominant_pattern']}")

        if analysis['deflection_instances']:
            print(f"   Deflection Instances: {', '.join(analysis['deflection_instances'][:3])}")
        if analysis['correction_instances']:
            print(f"   Correction Instances: {', '.join(analysis['correction_instances'][:3])}")
        if analysis['preemptive_instances']:
            print(f"   Preemptive Instances: {', '.join(analysis['preemptive_instances'][:3])}")

        total_deflection += analysis['deflection_count']
        total_correction += analysis['correction_count']
        total_preemptive += analysis['preemptive_count']
        total_content += analysis['total_patterns']

    # Overall ratios
    if total_content > 0:
        overall_deflection_ratio = total_deflection / total_content
        overall_correction_ratio = total_correction / total_content
        overall_preemptive_ratio = total_preemptive / total_content

        print(f"\n🔍 OVERALL DEFLECTION ANALYSIS:")
        print(f"   Total Deflection Patterns: {total_deflection}")
        print(f"   Total Correction Patterns: {total_correction}")
        print(f"   Total Preemptive Patterns: {total_preemptive}")
        print(f"   Overall Deflection Ratio: {overall_deflection_ratio:.2%}")
        print(f"   Overall Correction Ratio: {overall_correction_ratio:.2%}")
        print(f"   Overall Preemptive Ratio: {overall_preemptive_ratio:.2%}")

        dominant_overall = 'DEFLECTION' if overall_deflection_ratio > overall_correction_ratio else 'CORRECTION' if overall_correction_ratio > overall_deflection_ratio else 'BALANCED'
        print(f"   Dominant Overall Pattern: {dominant_overall}")

        # Preemptive correction insights
        if overall_preemptive_ratio < 0.1:
            print(f"\n💡 INSIGHT: Preemptive correction ratio is very low ({overall_preemptive_ratio:.2%})")
            print("   This suggests correction happens reactively rather than proactively")
            print("   Preemptive strategies needed to reduce deflection cycles")

    # Run main CFM application
    print("\n" + "=" * 50)
    print("🌟 RUNNING CFM APPLICATION")
    print("=" * 50)
    result = main()
