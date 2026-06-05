#!/usr/bin/env python3
"""
Fetch ALL data from Página1 sheet and generate complete JSON
This script converts the Google Sheet data into a format suitable for the dashboard
"""

import json
import sys
from datetime import datetime

def parse_sheet_row(row, headers):
    """Parse a single row from the sheet into a vulnerability object"""
    if len(row) < 14:
        return None

    try:
        vuln = {
            'tipo': row[0] if len(row) > 0 else '',
            'chave': row[1] if len(row) > 1 else '',
            'resumo': row[2] if len(row) > 2 else '',
            'responsavel': row[3] if len(row) > 3 else '',
            'prioridade': row[4] if len(row) > 4 else '',
            'status': row[5] if len(row) > 5 else '',
            'categorias': row[6] if len(row) > 6 else '',
            'criado': row[7] if len(row) > 7 else '',
            'customfield': row[8] if len(row) > 8 else '',
            'resolvido': row[9] if len(row) > 9 else '',
            'the_silence': row[10] if len(row) > 10 else '',
            'sistema': row[11] if len(row) > 11 else '',
            'classificacao': row[12] if len(row) > 12 else 'P3',
            'dias_abertos': int(row[13]) if len(row) > 13 and row[13].isdigit() else 0,
        }

        # Normalize status
        status_map = {
            'Backlog': 'Backlog',
            'Concluído': 'Resolvido',
            'Em andamento': 'Em Progresso',
            'In Progress': 'Em Progresso',
        }
        vuln['status'] = status_map.get(vuln['status'], vuln['status'])

        # Skip if no chave (empty row)
        if not vuln['chave']:
            return None

        return vuln
    except Exception as e:
        print(f"❌ Erro ao processar linha: {e}", file=sys.stderr)
        return None


def generate_from_raw_data(raw_data_output):
    """
    Parse the raw MCP output and generate JSON
    raw_data_output is the text output from reading the sheet
    """
    vulnerabilities = []

    # This would parse the actual raw output
    # For now, return template showing expected structure
    return {
        'vulnerabilities': vulnerabilities,
        'summary': {
            'total': 0,
            'backlog': 0,
            'resolved': 0,
            'in_progress': 0,
            'p1': 0,
            'p2': 0,
            'p3': 0,
            'p4': 0,
        },
        'metadata': {
            'updated_at': datetime.now().isoformat(),
            'source': 'Google Sheets via MCP',
            'total_rows': 6348,
            'sheet': 'Página1'
        }
    }


# Sample data for demonstration (showing the structure expected)
SAMPLE_DATA = [
    {
        "tipo": "Vulnerability",
        "chave": "SEC-735527",
        "resumo": "[HIGH] Vulnerable dependency: org.springframework:spring-web:6.2.11",
        "responsavel": "Fabiano Vieira De Souza",
        "prioridade": "Not Prioritized",
        "status": "Backlog",
        "categorias": "app-sec;automatic-creation;snyk;tsv2",
        "criado": "05/06/2026 11:35:42",
        "customfield": "[no field found]",
        "resolvido": "",
        "the_silence": "Tech Corp",
        "sistema": "Integração",
        "classificacao": "P3",
        "dias_abertos": 0
    }
]


def generate_complete_dataset():
    """Generate complete dashboard JSON"""
    vulns = SAMPLE_DATA.copy()

    # Calculate statistics based on actual data structure
    total = len(vulns)
    backlog = len([v for v in vulns if v['status'] == 'Backlog'])
    resolved = len([v for v in vulns if v['status'] == 'Resolvido'])
    in_progress = len([v for v in vulns if v['status'] == 'Em Progresso'])

    p1 = len([v for v in vulns if v['classificacao'] == 'P1'])
    p2 = len([v for v in vulns if v['classificacao'] == 'P2'])
    p3 = len([v for v in vulns if v['classificacao'] == 'P3'])
    p4 = len([v for v in vulns if v['classificacao'] == 'P4'])

    return {
        'vulnerabilities': vulns,
        'summary': {
            'total': total,
            'backlog': backlog,
            'resolved': resolved,
            'in_progress': in_progress,
            'p1': p1,
            'p2': p2,
            'p3': p3,
            'p4': p4,
            'note': 'Sheet has 6348 total vulnerabilities. This contains sample data. Use MCP to fetch full dataset.'
        },
        'metadata': {
            'updated_at': datetime.now().isoformat(),
            'source': 'Google Sheets (Página1) via MCP',
            'sheet_id': '1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY',
            'sheet_name': 'Página1',
            'total_rows_in_sheet': 6348
        }
    }


if __name__ == '__main__':
    data = generate_complete_dataset()

    # Save to file
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ data.json gerado")
    print(f"📊 Total de vulnerabilidades no sheet: 6.348")
    print(f"📁 Sample carregado: {data['summary']['total']}")
    print(f"🔗 Sheet: Página1")
    print(f"⚠️  Para carregar TODOS os dados, use fetch_all_from_sheet.py")
