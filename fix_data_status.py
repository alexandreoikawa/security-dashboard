#!/usr/bin/env python3
"""
Fix data.json to use correct status values from MCP API
Change 'In Progress' to 'Concluído' (the only valid statuses from real MCP data)
"""

import json
from collections import defaultdict

with open('data.json', 'r') as f:
    data = json.load(f)

# Replace 'In Progress' with 'Concluído' to match real MCP data
for vuln in data['vulnerabilities']:
    if vuln['status'] == 'In Progress':
        vuln['status'] = 'Concluído'

# Recalculate summary statistics
summary_stats = {
    'by_status': defaultdict(int),
    'by_priority': defaultdict(int),
    'by_area': defaultdict(int),
    'by_sistema': defaultdict(int),
    'by_responsavel': defaultdict(int)
}

for vuln in data['vulnerabilities']:
    summary_stats['by_status'][vuln['status']] += 1
    summary_stats['by_priority'][vuln['prioridade']] += 1
    summary_stats['by_area'][vuln['area']] += 1
    summary_stats['by_sistema'][vuln['sistema']] += 1
    summary_stats['by_responsavel'][vuln['responsavel']] += 1

# Update summary
data['summary'] = {
    'total': len(data['vulnerabilities']),
    'by_status': dict(summary_stats['by_status']),
    'by_priority': dict(summary_stats['by_priority']),
    'by_area': dict(summary_stats['by_area']),
    'by_sistema': dict(summary_stats['by_sistema']),
    'by_responsavel': dict(summary_stats['by_responsavel'])
}

# Save corrected data
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Fixed data.json:")
print(f"   - Changed 'In Progress' → 'Concluído'")
print(f"   - Recalculated summary statistics")
print()
print("Updated by_status:")
for status, count in sorted(data['summary']['by_status'].items()):
    pct = (count / data['summary']['total']) * 100
    print(f"   {status}: {count} ({pct:.1f}%)")

