#!/usr/bin/env python3
"""
Fetch real vulnerability data from Página1 sheet and generate data.json
Uses Google Sheets API (MCP compatible)
"""

import json
import sys
from datetime import datetime
from typing import Optional, Dict, List, Any

def parse_row_to_vulnerability(row: List[str], index: int) -> Optional[Dict[str, Any]]:
    """Parse a single row into a vulnerability object"""
    if len(row) < 14:
        return None

    try:
        # Extract fields
        tipo = row[0].strip() if len(row) > 0 else ''
        chave = row[1].strip() if len(row) > 1 else ''
        resumo = row[2].strip() if len(row) > 2 else ''
        responsavel = row[3].strip() if len(row) > 3 else ''
        prioridade = row[4].strip() if len(row) > 4 else ''
        status = row[5].strip() if len(row) > 5 else ''
        categorias = row[6].strip() if len(row) > 6 else ''
        criado = row[7].strip() if len(row) > 7 else ''
        customfield = row[8].strip() if len(row) > 8 else ''
        resolvido = row[9].strip() if len(row) > 9 else ''
        the_silence = row[10].strip() if len(row) > 10 else ''
        sistema = row[11].strip() if len(row) > 11 else ''
        classificacao = row[12].strip() if len(row) > 12 else 'P3'
        dias_abertos = row[13].strip() if len(row) > 13 else '0'

        # Skip if no chave (empty row)
        if not chave:
            return None

        # Convert dias_abertos to int
        try:
            dias_abertos_int = int(dias_abertos) if dias_abertos.isdigit() else 0
        except ValueError:
            dias_abertos_int = 0

        return {
            'tipo': tipo,
            'chave': chave,
            'resumo': resumo,
            'responsavel': responsavel,
            'prioridade': prioridade,
            'status': status,  # Keep original values: "Backlog", "Concluído"
            'categorias': categorias,
            'criado': criado,
            'customfield': customfield,
            'resolvido': resolvido,
            'the_silence': the_silence,
            'sistema': sistema,
            'classificacao': classificacao,  # P1, P2, P3, P4
            'dias_abertos': dias_abertos_int,
        }
    except Exception as e:
        print(f"⚠️  Error parsing row {index}: {e}", file=sys.stderr)
        return None

def main():
    """Main function to process sheet data"""
    print("📥 Reading Página1 data from standard input...", file=sys.stderr)

    # Read input from stdin (expecting JSON array of rows)
    try:
        input_data = sys.stdin.read()
        raw_rows = json.loads(input_data)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing input JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(raw_rows, list) or len(raw_rows) == 0:
        print("❌ Input must be a non-empty JSON array", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Read {len(raw_rows)} rows from input", file=sys.stderr)

    # Skip header row (index 0)
    vulnerabilities = []
    for i, row in enumerate(raw_rows[1:], start=2):
        vuln = parse_row_to_vulnerability(row, i)
        if vuln:
            vulnerabilities.append(vuln)

    if not vulnerabilities:
        print("❌ No vulnerabilities parsed", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Parsed {len(vulnerabilities)} vulnerabilities", file=sys.stderr)

    # Calculate statistics
    total = len(vulnerabilities)
    backlog = len([v for v in vulnerabilities if v['status'] == 'Backlog'])
    concluido = len([v for v in vulnerabilities if v['status'] == 'Concluído'])
    em_progresso = len([v for v in vulnerabilities if v['status'] == 'Em Progresso'])

    p1 = len([v for v in vulnerabilities if v['classificacao'] == 'P1'])
    p2 = len([v for v in vulnerabilities if v['classificacao'] == 'P2'])
    p3 = len([v for v in vulnerabilities if v['classificacao'] == 'P3'])
    p4 = len([v for v in vulnerabilities if v['classificacao'] == 'P4'])

    # Get unique responsible parties
    responsibles = sorted(list(set(v['responsavel'] for v in vulnerabilities if v['responsavel'])))

    # Get unique categories
    all_categories = set()
    for v in vulnerabilities:
        if v['categorias']:
            categories = [c.strip() for c in v['categorias'].split(';')]
            all_categories.update(categories)
    categories_list = sorted(list(all_categories))

    # Generate dataset
    dataset = {
        'vulnerabilities': vulnerabilities,
        'summary': {
            'total': total,
            'backlog': backlog,
            'concluido': concluido,
            'em_progresso': em_progresso,
            'p1': p1,
            'p2': p2,
            'p3': p3,
            'p4': p4,
        },
        'filters': {
            'responsibles': responsibles,
            'categories': categories_list,
        },
        'metadata': {
            'updated_at': datetime.now().isoformat(),
            'sheet_id': '1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY',
            'sheet_name': 'Página1',
            'source': 'Google Sheets - Página1 (Real Data)',
            'total_rows_loaded': total,
        }
    }

    # Save to file
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    # Print statistics
    print(f"✅ data.json generated successfully!", file=sys.stderr)
    print(f"   📊 Total: {total:,}", file=sys.stderr)
    print(f"   📁 Backlog: {backlog:,}", file=sys.stderr)
    print(f"   ✓ Concluído: {concluido:,}", file=sys.stderr)
    print(f"   ⏳ Em Progresso: {em_progresso:,}", file=sys.stderr)
    print(f"   🔴 P1: {p1:,}", file=sys.stderr)
    print(f"   🟡 P2: {p2:,}", file=sys.stderr)
    print(f"   🟠 P3: {p3:,}", file=sys.stderr)
    print(f"   🟢 P4: {p4:,}", file=sys.stderr)
    print(f"   👥 Responsibles: {len(responsibles)}", file=sys.stderr)
    print(f"   🏷️  Categories: {len(categories_list)}", file=sys.stderr)

if __name__ == '__main__':
    main()
