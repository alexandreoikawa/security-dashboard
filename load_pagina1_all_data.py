#!/usr/bin/env python3
"""
Load ALL 6,348 vulnerabilities from Página1 sheet and generate complete data.json
Uses Google Sheets API via environment credentials
"""

import json
import sys
import os
from datetime import datetime

def load_from_google_sheets():
    """Load data from Google Sheets using credentials"""
    try:
        from google.oauth2.service_account import Credentials
        from google.auth.transport.requests import Request
        import gspread
    except ImportError:
        print("❌ Missing google libraries. Install with:", file=sys.stderr)
        print("   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client gspread", file=sys.stderr)
        return None

    try:
        # Try to use service account credentials from environment
        creds_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if creds_json:
            creds = Credentials.from_service_account_file(creds_json)
            gc = gspread.authorize(creds)
        else:
            print("⚠️  No GOOGLE_APPLICATION_CREDENTIALS set", file=sys.stderr)
            return None

        # Open the sheet
        sheet_id = "1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY"
        sheet = gc.open_by_key(sheet_id)

        # Get Página1 sheet
        worksheet = sheet.worksheet("Página1")

        # Get all values
        all_rows = worksheet.get_all_values()

        print(f"✅ Loaded {len(all_rows)} rows from Página1", file=sys.stderr)
        return all_rows

    except Exception as e:
        print(f"❌ Error loading from Google Sheets: {e}", file=sys.stderr)
        return None


def parse_vulnerability(row):
    """Parse a single row into a vulnerability object"""
    if len(row) < 14:
        return None

    try:
        vuln = {
            'tipo': row[0].strip() if len(row) > 0 else '',
            'chave': row[1].strip() if len(row) > 1 else '',
            'resumo': row[2].strip() if len(row) > 2 else '',
            'responsavel': row[3].strip() if len(row) > 3 else '',
            'prioridade': row[4].strip() if len(row) > 4 else '',
            'status': row[5].strip() if len(row) > 5 else '',
            'categorias': row[6].strip() if len(row) > 6 else '',
            'criado': row[7].strip() if len(row) > 7 else '',
            'customfield': row[8].strip() if len(row) > 8 else '',
            'resolvido': row[9].strip() if len(row) > 9 else '',
            'the_silence': row[10].strip() if len(row) > 10 else '',
            'sistema': row[11].strip() if len(row) > 11 else '',
            'classificacao': row[12].strip() if len(row) > 12 else 'P3',
            'dias_abertos': int(row[13]) if len(row) > 13 and str(row[13]).isdigit() else 0,
        }

        # Normalize status
        status_map = {
            'Backlog': 'Backlog',
            'Concluído': 'Resolvido',
            'Em andamento': 'Em Progresso',
            'In Progress': 'Em Progresso',
            'Resolvido': 'Resolvido',
        }
        vuln['status'] = status_map.get(vuln['status'], vuln['status'])

        # Skip if no chave (empty row)
        if not vuln['chave']:
            return None

        return vuln
    except Exception as e:
        print(f"⚠️  Error parsing row: {e}", file=sys.stderr)
        return None


def generate_dataset(raw_data):
    """Generate dashboard JSON from raw sheet data"""
    if not raw_data:
        print("❌ No raw data provided", file=sys.stderr)
        return None

    # Skip header row
    vulnerabilities = []
    for row in raw_data[1:]:
        vuln = parse_vulnerability(row)
        if vuln:
            vulnerabilities.append(vuln)

    if not vulnerabilities:
        print("❌ No vulnerabilities parsed", file=sys.stderr)
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
            'source': 'Google Sheets - Página1 (ALL data)',
            'total_rows_loaded': total,
        }
    }


if __name__ == '__main__':
    print("📥 Loading data from Página1...", file=sys.stderr)

    # Try to load from Google Sheets
    raw_data = load_from_google_sheets()

    if raw_data:
        print(f"✅ Raw data loaded: {len(raw_data)} rows", file=sys.stderr)
        data = generate_dataset(raw_data)

        if data:
            # Save to file
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ data.json gerado com sucesso!", file=sys.stderr)
            print(f"   📊 Total: {data['summary']['total']}", file=sys.stderr)
            print(f"   📁 Backlog: {data['summary']['backlog']}", file=sys.stderr)
            print(f"   ✓ Resolvido: {data['summary']['resolved']}", file=sys.stderr)
            print(f"   🔴 P1: {data['summary']['p1']}", file=sys.stderr)
            print(f"   🟡 P2: {data['summary']['p2']}", file=sys.stderr)
            print(f"   🟠 P3: {data['summary']['p3']}", file=sys.stderr)
            print(f"   🟢 P4: {data['summary']['p4']}", file=sys.stderr)
        else:
            print("❌ Failed to generate dataset", file=sys.stderr)
            sys.exit(1)
    else:
        print("⚠️  Could not load from Google Sheets", file=sys.stderr)
        print("   Make sure GOOGLE_APPLICATION_CREDENTIALS is set", file=sys.stderr)
        sys.exit(1)
