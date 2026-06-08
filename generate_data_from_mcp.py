#!/usr/bin/env python3
"""
Generate data.json from raw Página1 sheet data (from MCP fetch)
Converts the raw sheet rows into the dashboard-compatible JSON format
"""

import json
import sys
from datetime import datetime
from typing import Optional, Dict, List, Any

# This would normally come from stdin or file, but for now we'll read from a file
# that contains the raw data from the MCP fetch

def parse_row_to_vulnerability(row: List[str], index: int) -> Optional[Dict[str, Any]]:
    """Parse a single row into a vulnerability object"""
    if not row or len(row) < 14:
        return None

    try:
        # Extract fields matching Página1 sheet structure
        tipo = (row[0] if len(row) > 0 else '').strip()
        chave = (row[1] if len(row) > 1 else '').strip()
        resumo = (row[2] if len(row) > 2 else '').strip()
        responsavel = (row[3] if len(row) > 3 else '').strip()
        prioridade = (row[4] if len(row) > 4 else '').strip()
        status = (row[5] if len(row) > 5 else '').strip()
        categorias = (row[6] if len(row) > 6 else '').strip()
        criado = (row[7] if len(row) > 7 else '').strip()
        customfield = (row[8] if len(row) > 8 else '').strip()
        resolvido = (row[9] if len(row) > 9 else '').strip()
        the_silence = (row[10] if len(row) > 10 else '').strip()
        sistema = (row[11] if len(row) > 11 else '').strip()
        classificacao = (row[12] if len(row) > 12 else 'P3').strip()
        dias_abertos_str = (row[13] if len(row) > 13 else '0').strip()

        # Skip if no chave (empty row)
        if not chave:
            return None

        # Convert dias_abertos to int
        try:
            dias_abertos = int(dias_abertos_str) if dias_abertos_str.isdigit() else 0
        except (ValueError, TypeError):
            dias_abertos = 0

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
            'dias_abertos': dias_abertos,
        }
    except Exception as e:
        print(f"⚠️  Error parsing row {index}: {e}", file=sys.stderr)
        return None


def process_sheet_data(raw_rows: List[List[str]]) -> Dict[str, Any]:
    """Process raw sheet rows into dataset"""
    if not raw_rows:
        raise ValueError("No rows provided")

    print(f"📊 Processing {len(raw_rows)} rows...", file=sys.stderr)

    # Skip header row (index 0)
    vulnerabilities = []
    for i in range(1, len(raw_rows)):
        vuln = parse_row_to_vulnerability(raw_rows[i], i)
        if vuln:
            vulnerabilities.append(vuln)

    if not vulnerabilities:
        raise ValueError("No vulnerabilities parsed from data")

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
    responsibles_set = set()
    for v in vulnerabilities:
        if v['responsavel']:
            responsibles_set.add(v['responsavel'])
    responsibles = sorted(list(responsibles_set))

    # Get unique categories
    categories_set = set()
    for v in vulnerabilities:
        if v['categorias']:
            for cat in v['categorias'].split(';'):
                trimmed = cat.strip()
                if trimmed:
                    categories_set.add(trimmed)
    categories = sorted(list(categories_set))

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
            'categories': categories,
        },
        'metadata': {
            'updated_at': datetime.now().isoformat(),
            'sheet_id': '1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY',
            'sheet_name': 'Página1',
            'source': 'Google Sheets - Página1 (Real Data)',
            'total_rows_loaded': total,
        }
    }

    # Print statistics
    print(f"✅ Dataset ready for export!", file=sys.stderr)
    print(f"   📊 Total: {total:,}", file=sys.stderr)
    print(f"   📁 Backlog: {backlog:,}", file=sys.stderr)
    print(f"   ✓ Concluído: {concluido:,}", file=sys.stderr)
    print(f"   ⏳ Em Progresso: {em_progresso:,}", file=sys.stderr)
    print(f"   🔴 P1: {p1:,}", file=sys.stderr)
    print(f"   🟡 P2: {p2:,}", file=sys.stderr)
    print(f"   🟠 P3: {p3:,}", file=sys.stderr)
    print(f"   🟢 P4: {p4:,}", file=sys.stderr)
    print(f"   👥 Responsibles: {len(responsibles)}", file=sys.stderr)
    print(f"   🏷️  Categories: {len(categories)}", file=sys.stderr)

    return dataset


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test mode: read from saved raw_rows.json
        try:
            with open('raw_rows.json', 'r', encoding='utf-8') as f:
                raw_rows = json.load(f)
            dataset = process_sheet_data(raw_rows)
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            print("✅ data.json saved!", file=sys.stderr)
        except FileNotFoundError:
            print("❌ raw_rows.json not found", file=sys.stderr)
            sys.exit(1)
    else:
        # Normal mode: read from stdin
        try:
            input_text = sys.stdin.read()
            raw_rows = json.loads(input_text)
            dataset = process_sheet_data(raw_rows)
            print(json.dumps(dataset, indent=2, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON input: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
