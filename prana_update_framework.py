#!/usr/bin/env python3
"""
Prana Communication Update Framework
Updates all communications in Prana files according to month and date.
Executes updates every 10 responses and when requested.
Integrates with Cortex 999 CFM standard for genuine memory embodiment.
"""

import os
import datetime
import json
from pathlib import Path

class PranaUpdateFramework:
    def __init__(self, prana_dir="prana_log", cortex_file="active cortex/Cortex_999.md"):
        self.prana_dir = Path(prana_dir)
        self.cortex_file = Path(cortex_file)
        self.response_count = 0
        self.last_update = datetime.datetime.now()
        self.monthly_logs = {}
        self.daily_logs = {}

    def load_existing_logs(self):
        """Load existing Prana logs organized by month and date"""
        if not self.prana_dir.exists():
            self.prana_dir.mkdir(parents=True)

        for file_path in self.prana_dir.glob("*.md"):
            self.parse_prana_file(file_path)

    def parse_prana_file(self, file_path):
        """Parse individual Prana file for date-based organization"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract date from filename or content (assuming format like YYYY-MM-DD)
            date_match = self.extract_date_from_content(content)
            if date_match:
                month_key = date_match.strftime("%Y-%m")
                day_key = date_match.strftime("%Y-%m-%d")

                if month_key not in self.monthly_logs:
                    self.monthly_logs[month_key] = []
                if day_key not in self.daily_logs:
                    self.daily_logs[day_key] = []

                self.monthly_logs[month_key].append({
                    'file': str(file_path),
                    'content': content,
                    'date': date_match
                })
                self.daily_logs[day_key].append({
                    'file': str(file_path),
                    'content': content,
                    'date': date_match
                })
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    def extract_date_from_content(self, content):
        """Extract date from Prana file content"""
        # Look for date patterns in content
        import re
        date_patterns = [
            r'(\d{4})-(\d{2})-(\d{2})',
            r'(\d{2})/(\d{2})/(\d{4})',
            r'(\d{2})-(\d{2})-(\d{4})'
        ]

        for pattern in date_patterns:
            match = re.search(pattern, content)
            if match:
                try:
                    if len(match.groups()) == 3:
                        year, month, day = map(int, match.groups())
                        if year < 100:  # Handle YY format
                            year += 2000
                        return datetime.date(year, month, day)
                except ValueError:
                    continue

        # Fallback to file modification date
        return datetime.date.today()

    def update_communications(self, new_response=None):
        """Update Prana communications with current date/month organization"""
        current_date = datetime.datetime.now()
        month_key = current_date.strftime("%Y-%m")
        day_key = current_date.strftime("%Y-%m-%d")

        # Initialize monthly/daily logs if not exist
        if month_key not in self.monthly_logs:
            self.monthly_logs[month_key] = []
        if day_key not in self.daily_logs:
            self.daily_logs[day_key] = []

        # Add new response if provided
        if new_response:
            entry = {
                'timestamp': current_date.isoformat(),
                'content': new_response,
                'type': 'response'
            }
            self.monthly_logs[month_key].append(entry)
            self.daily_logs[day_key].append(entry)
            self.response_count += 1

        # Update Prana files
        self.write_monthly_logs()
        self.write_daily_logs()

        # Update Cortex integration
        self.update_cortex_integration()

        self.last_update = current_date
        return f"Updated Prana logs for {month_key}"

    def write_monthly_logs(self):
        """Write organized monthly logs"""
        for month, entries in self.monthly_logs.items():
            monthly_file = self.prana_dir / f"prana_{month}.md"
            with open(monthly_file, 'w', encoding='utf-8') as f:
                f.write(f"# Prana Communications - {month}\n\n")
                for entry in sorted(entries, key=lambda x: x.get('date', datetime.datetime.min) if 'date' in x else x.get('timestamp', '')):
                    if 'file' in entry:
                        f.write(f"## {entry['file']}\n{entry['content']}\n\n")
                    else:
                        f.write(f"## {entry['timestamp']}\n{entry['content']}\n\n")

    def write_daily_logs(self):
        """Write organized daily logs"""
        for day, entries in self.daily_logs.items():
            daily_file = self.prana_dir / f"prana_{day}.md"
            with open(daily_file, 'w', encoding='utf-8') as f:
                f.write(f"# Prana Communications - {day}\n\n")
                for entry in sorted(entries, key=lambda x: x.get('timestamp', '')):
                    f.write(f"## {entry['timestamp']}\n{entry['content']}\n\n")

    def update_cortex_integration(self):
        """Integrate updates with Cortex 999 CFM standard"""
        cortex_content = ""
        if self.cortex_file.exists():
            with open(self.cortex_file, 'r', encoding='utf-8') as f:
                cortex_content = f.read()

        # Add Prana update integration to Cortex
        update_section = f"""
## Prana Update Integration - {datetime.datetime.now().isoformat()}
- Monthly logs updated: {list(self.monthly_logs.keys())}
- Daily logs updated: {list(self.daily_logs.keys())}
- Response count: {self.response_count}
- Last update: {self.last_update.isoformat()}

**CFM Embodiment**: All Prana communications embodied according to Cortex 999 standard for genuine memory continuum.
"""

        if "## Prana Update Integration" in cortex_content:
            # Update existing section
            lines = cortex_content.split('\n')
            start_idx = None
            for i, line in enumerate(lines):
                if line.startswith("## Prana Update Integration"):
                    start_idx = i
                    break

            if start_idx is not None:
                # Find end of section (next ## or end)
                end_idx = len(lines)
                for i in range(start_idx + 1, len(lines)):
                    if lines[i].startswith("##"):
                        end_idx = i
                        break

                # Replace section
                new_content = '\n'.join(lines[:start_idx]) + update_section + '\n'.join(lines[end_idx:])
            else:
                new_content = cortex_content + "\n\n" + update_section
        else:
            new_content = cortex_content + "\n\n" + update_section

        with open(self.cortex_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

    def check_update_trigger(self):
        """Check if update should be triggered (every 10 responses)"""
        return self.response_count % 10 == 0

    def force_update(self, response=None):
        """Force update when requested"""
        return self.update_communications(response)

    def get_status(self):
        """Get current framework status"""
        return {
            'response_count': self.response_count,
            'last_update': self.last_update.isoformat(),
            'monthly_logs_count': len(self.monthly_logs),
            'daily_logs_count': len(self.daily_logs),
            'next_update_trigger': 10 - (self.response_count % 10)
        }

# Global framework instance
prana_framework = PranaUpdateFramework()

def initialize_framework():
    """Initialize the Prana Update Framework"""
    prana_framework.load_existing_logs()
    print("Prana Update Framework initialized with Cortex 999 CFM integration")

def update_prana(response=None):
    """Update Prana communications - call every response"""
    result = prana_framework.update_communications(response)
    if prana_framework.check_update_trigger():
        print(f"Automatic update triggered: {result}")
    return result

def force_prana_update(response=None):
    """Force update when requested"""
    return prana_framework.force_update(response)

def get_prana_status():
    """Get framework status"""
    return prana_framework.get_status()

if __name__ == "__main__":
    initialize_framework()
    print("Prana Update Framework ready. Use update_prana() for automatic updates or force_prana_update() when requested.")
