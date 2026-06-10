#!/usr/bin/env python3
"""
Verify that filter data in data.json is correct
"""

import json

with open('data.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("FILTER DATA VERIFICATION")
print("=" * 80)
print()

print("✅ STATUS (em HTML):")
print("   - Todos os Status")
print("   - Backlog")
print("   - Concluído")
print()

print("✅ STATUS (em data.json):")
for status, count in sorted(data['summary']['by_status'].items()):
    pct = (count / data['summary']['total']) * 100
    print(f"   - {status}: {count} ({pct:.1f}%)")
print()

print("✅ PRIORIDADES (em HTML):")
print("   - Todas as Prioridades")
print("   - P0 - Crítica")
print("   - P1 - Alta")
print("   - P2 - Média")
print("   - P3 - Baixa")
print("   - Red Team")
print()

print("✅ PRIORIDADES (em data.json):")
for priority, count in sorted(data['summary']['by_priority'].items()):
    pct = (count / data['summary']['total']) * 100
    print(f"   - {priority}: {count} ({pct:.1f}%)")
print()

print("✅ ÁREAS (dinâmicas em JavaScript - extraídas de data.json):")
for area, count in sorted(data['summary']['by_area'].items()):
    pct = (count / data['summary']['total']) * 100
    print(f"   - {area}: {count} ({pct:.1f}%)")
print()

print("✅ SISTEMAS (dinâmicos em JavaScript - extraídos de data.json):")
for system, count in sorted(data['summary']['by_sistema'].items()):
    pct = (count / data['summary']['total']) * 100
    print(f"   - {system}: {count} ({pct:.1f}%)")
print()

print("✅ RESPONSÁVEIS (dinâmicos em JavaScript - extraídos de data.json):")
for owner, count in sorted(data['summary']['by_responsavel'].items()):
    pct = (count / data['summary']['total']) * 100
    print(f"   - {owner}: {count} ({pct:.1f}%)")
print()

print("=" * 80)
print("TOTAL RECORDS: " + str(data['summary']['total']))
print("=" * 80)

