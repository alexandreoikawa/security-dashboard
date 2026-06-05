#!/usr/bin/env python3
"""Extract real filters from generated dataset"""

import json

# Load existing data.json
with open('data.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

vulnerabilities = dataset['vulnerabilities']

print(f"📊 Extraindo filtros dinâmicos de {len(vulnerabilities)} registros...\n")

# Extract unique responsibles
responsibles = set()
for v in vulnerabilities:
    if v.get('responsavel'):
        responsibles.add(v['responsavel'])

# Extract unique categories
categories = set()
for v in vulnerabilities:
    if v.get('categorias'):
        for cat in v['categorias'].split(';'):
            cat_clean = cat.strip()
            if cat_clean:
                categories.add(cat_clean)

# Sort for consistency
responsibles_sorted = sorted(list(responsibles))
categories_sorted = sorted(list(categories))

print(f"✅ Responsáveis únicos: {len(responsibles_sorted)}")
for r in responsibles_sorted:
    print(f"   - {r}")

print(f"\n✅ Categorias únicas: {len(categories_sorted)}")
for c in categories_sorted:
    print(f"   - {c}")

# Update dataset with real filters
dataset['filters'] = {
    'responsibles': responsibles_sorted,
    'categories': categories_sorted
}

# Save back to data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print(f"\n✅ data.json atualizado com filtros dinâmicos")
print(f"   📊 Responsáveis: {len(responsibles_sorted)}")
print(f"   🏷️  Categorias: {len(categories_sorted)}")
