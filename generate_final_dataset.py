#!/usr/bin/env python3
"""
Parse complete Página1 sheet data and generate final data.json for dashboard
This script processes all 6,348 vulnerabilities from the Google Sheet
"""

import json
import sys
from datetime import datetime

# All 6348 rows of data from Página1 sheet will be processed here
# Format: List of lists where each inner list is a row

def parse_vulnerability_row(row):
    """Parse a single row into a vulnerability object"""
    if not row or len(row) < 14:
        return None

    try:
        # Strip whitespace from all fields
        fields = [str(f).strip() if f else '' for f in row]

        vuln = {
            'tipo': fields[0],
            'chave': fields[1],
            'resumo': fields[2],
            'responsavel': fields[3],
            'prioridade': fields[4],
            'status': fields[5],
            'categorias': fields[6],
            'criado': fields[7],
            'customfield': fields[8],
            'resolvido': fields[9],
            'the_silence': fields[10],
            'sistema': fields[11],
            'classificacao': fields[12],
            'dias_abertos': int(fields[13]) if fields[13].isdigit() else 0,
        }

        # Normalize status values
        status_map = {
            'Backlog': 'Backlog',
            'Concluído': 'Resolvido',
            'Em andamento': 'Em Progresso',
            'In Progress': 'Em Progresso',
            'Resolvido': 'Resolvido',
        }
        vuln['status'] = status_map.get(vuln['status'], vuln['status'])

        # Normalize classification/priority
        if vuln['classificacao'] not in ['P1', 'P2', 'P3', 'P4']:
            vuln['classificacao'] = 'P3'

        # Skip empty rows (no chave)
        if not vuln['chave']:
            return None

        return vuln
    except Exception as e:
        print(f"⚠️  Error parsing row: {e}", file=sys.stderr)
        return None


def generate_complete_dataset(raw_data_lines):
    """
    Generate complete dataset from raw sheet data
    raw_data_lines: List of lines from sheet output
    """
    vulnerabilities = []

    # Parse the raw data - expecting format like "Row N: [...]"
    current_row_index = 0

    for line in raw_data_lines:
        if line.startswith('Row ') and '[' in line and ']' in line:
            try:
                # Extract the array part
                start = line.index('[')
                end = line.rindex(']') + 1
                row_str = line[start:end]

                # Simple eval - be careful with untrusted input
                # In production, use ast.literal_eval instead
                import ast
                row_data = ast.literal_eval(row_str)

                if current_row_index > 0:  # Skip header row
                    parsed = parse_vulnerability_row(row_data)
                    if parsed:
                        vulnerabilities.append(parsed)

                current_row_index += 1

            except Exception as e:
                print(f"⚠️  Error parsing row data: {e}", file=sys.stderr)
                continue

    if not vulnerabilities:
        print("❌ No vulnerabilities were parsed", file=sys.stderr)
        return None

    # Calculate statistics
    total = len(vulnerabilities)
    backlog = len([v for v in vulnerabilities if v['status'] == 'Backlog'])
    resolved = len([v for v in vulnerabilities if v['status'] == 'Resolvido'])
    in_progress = len([v for v in vulnerabilities if v['status'] == 'Em Progresso'])

    p1 = len([v for v in vulnerabilities if v['classificacao'] == 'P1'])
    p2 = len([v for v in vulnerabilities if v['classificacao'] == 'P2'])
    p3 = len([v for v in vulnerabilities if v['classificacao'] == 'P3'])
    p4 = len([v for v in vulnerabilities if v['classificacao'] == 'P4'])

    return {
        'vulnerabilities': vulnerabilities,
        'summary': {
            'total': total,
            'backlog': backlog,
            'resolved': resolved,
            'in_progress': in_progress,
            'p1': p1,
            'p2': p2,
            'p3': p3,
            'p4': p4,
        },
        'metadata': {
            'updated_at': datetime.now().isoformat(),
            'sheet_id': '1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY',
            'sheet_name': 'Página1',
            'source': 'Google Sheets - Página1 (ALL 6348 vulnerabilities)',
            'total_rows_loaded': total,
        }
    }


if __name__ == '__main__':
    # Import hardcoded test data first - will read from stdin in production
    print("📥 Preparing to parse Página1 sheet data...", file=sys.stderr)

    # Read from stdin or use hardcoded data
    import sys
    if not sys.stdin.isatty():
        raw_data = sys.stdin.read()
    else:
        # Fall back to file if it exists
        try:
            with open('pagina1_raw.txt', 'r', encoding='utf-8') as f:
                raw_data = f.read()
        except FileNotFoundError:
            print("❌ No input data provided", file=sys.stderr)
            print("   Usage: python generate_final_dataset.py < pagina1_raw.txt", file=sys.stderr)
            sys.exit(1)

    lines = raw_data.split('\n')
    data = generate_complete_dataset(lines)

    if data:
        # Save to file
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ data.json gerado com sucesso!", file=sys.stderr)
        print(f"   📊 Total: {data['summary']['total']:,}", file=sys.stderr)
        print(f"   📁 Backlog: {data['summary']['backlog']:,}", file=sys.stderr)
        print(f"   ✓ Resolvido: {data['summary']['resolved']:,}", file=sys.stderr)
        print(f"   🔴 P1: {data['summary']['p1']:,}", file=sys.stderr)
        print(f"   🟡 P2: {data['summary']['p2']:,}", file=sys.stderr)
        print(f"   🟠 P3: {data['summary']['p3']:,}", file=sys.stderr)
        print(f"   🟢 P4: {data['summary']['p4']:,}", file=sys.stderr)
        print(f"\n✅ Dashboard is ready at index.html", file=sys.stderr)
    else:
        print("❌ Failed to generate dataset", file=sys.stderr)
        sys.exit(1)
