#!/usr/bin/env python3
"""
Fetch complete Página1 sheet data directly and generate data.json
"""

import json
import sys
import os
from datetime import datetime

def fetch_sheet_data_via_api():
    """Fetch sheet data using Google Sheets API"""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.service_account import Credentials
        import googleapiclient.discovery
    except ImportError:
        print("❌ Missing Google client libraries", file=sys.stderr)
        print("   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client", file=sys.stderr)
        return None

    try:
        # Try to get credentials from environment
        creds_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if not creds_file:
            print("⚠️  Trying to use default credentials...", file=sys.stderr)
            from google.auth import default
            creds, _ = default()
        else:
            creds = Credentials.from_service_account_file(creds_file)

        # Build the Sheets API client
        service = googleapiclient.discovery.build('sheets', 'v4', credentials=creds)

        sheet_id = '1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY'
        sheet_range = 'Página1!A:N'

        print(f"📥 Fetching data from {sheet_range}...", file=sys.stderr)

        # Request all values
        request = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=sheet_range,
            majorDimension='ROWS'
        )
        result = request.execute()

        rows = result.get('values', [])
        print(f"✅ Retrieved {len(rows)} rows", file=sys.stderr)
        return rows

    except Exception as e:
        print(f"❌ Error fetching from Sheets API: {e}", file=sys.stderr)
        return None


def parse_vulnerability(row):
    """Parse a sheet row into vulnerability object"""
    if not row or len(row) < 14:
        return None

    try:
        vuln = {
            'tipo': str(row[0]).strip() if len(row) > 0 else '',
            'chave': str(row[1]).strip() if len(row) > 1 else '',
            'resumo': str(row[2]).strip() if len(row) > 2 else '',
            'responsavel': str(row[3]).strip() if len(row) > 3 else '',
            'prioridade': str(row[4]).strip() if len(row) > 4 else '',
            'status': str(row[5]).strip() if len(row) > 5 else '',
            'categorias': str(row[6]).strip() if len(row) > 6 else '',
            'criado': str(row[7]).strip() if len(row) > 7 else '',
            'customfield': str(row[8]).strip() if len(row) > 8 else '',
            'resolvido': str(row[9]).strip() if len(row) > 9 else '',
            'the_silence': str(row[10]).strip() if len(row) > 10 else '',
            'sistema': str(row[11]).strip() if len(row) > 11 else '',
            'classificacao': str(row[12]).strip() if len(row) > 12 else 'P3',
            'dias_abertos': 0,
        }

        # Parse days open
        if len(row) > 13:
            try:
                vuln['dias_abertos'] = int(row[13])
            except (ValueError, TypeError):
                vuln['dias_abertos'] = 0

        # Normalize status
        status_map = {
            'Backlog': 'Backlog',
            'Concluído': 'Resolvido',
            'Em andamento': 'Em Progresso',
            'In Progress': 'Em Progresso',
            'Resolvido': 'Resolvido',
        }
        vuln['status'] = status_map.get(vuln['status'], vuln['status'])

        # Ensure valid classification
        if vuln['classificacao'] not in ['P1', 'P2', 'P3', 'P4']:
            # Try to extract from categorias if present
            if 'priority:P1' in vuln['categorias']:
                vuln['classificacao'] = 'P1'
            elif 'priority:P2' in vuln['categorias']:
                vuln['classificacao'] = 'P2'
            elif 'priority:P4' in vuln['categorias']:
                vuln['classificacao'] = 'P4'
            else:
                vuln['classificacao'] = 'P3'

        # Skip if no chave (empty row)
        if not vuln['chave']:
            return None

        return vuln

    except Exception as e:
        print(f"⚠️  Error parsing row: {e}", file=sys.stderr)
        return None


def generate_dataset(raw_rows):
    """Generate complete dataset from raw sheet rows"""
    if not raw_rows or len(raw_rows) < 2:
        print("❌ No data to process", file=sys.stderr)
        return None

    print(f"📊 Processing {len(raw_rows) - 1} data rows (excluding header)...", file=sys.stderr)

    vulnerabilities = []

    # Skip header row (row 0)
    for idx, row in enumerate(raw_rows[1:], start=2):
        try:
            vuln = parse_vulnerability(row)
            if vuln:
                vulnerabilities.append(vuln)
            if idx % 1000 == 0:
                print(f"   ✓ Processed {idx} rows...", file=sys.stderr)
        except Exception as e:
            print(f"⚠️  Error processing row {idx}: {e}", file=sys.stderr)
            continue

    if not vulnerabilities:
        print("❌ No vulnerabilities were parsed", file=sys.stderr)
        return None

    print(f"✅ Parsed {len(vulnerabilities)} vulnerabilities", file=sys.stderr)

    # Calculate statistics
    total = len(vulnerabilities)
    backlog = len([v for v in vulnerabilities if v['status'] == 'Backlog'])
    resolved = len([v for v in vulnerabilities if v['status'] == 'Resolvido'])
    in_progress = len([v for v in vulnerabilities if v['status'] == 'Em Progresso'])

    p1 = len([v for v in vulnerabilities if v['classificacao'] == 'P1'])
    p2 = len([v for v in vulnerabilities if v['classificacao'] == 'P2'])
    p3 = len([v for v in vulnerabilities if v['classificacao'] == 'P3'])
    p4 = len([v for v in vulnerabilities if v['classificacao'] == 'P4'])

    print(f"\n📈 Statistics:", file=sys.stderr)
    print(f"   Total: {total:,}", file=sys.stderr)
    print(f"   Backlog: {backlog:,} | Resolvido: {resolved:,} | Em Progresso: {in_progress:,}", file=sys.stderr)
    print(f"   P1: {p1:,} | P2: {p2:,} | P3: {p3:,} | P4: {p4:,}", file=sys.stderr)

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
            'source': 'Google Sheets API - Página1 (Complete Dataset)',
            'total_rows_loaded': total,
            'note': 'Complete data from Página1 sheet with all vulnerabilities'
        }
    }


if __name__ == '__main__':
    print("🔄 Starting data fetch and generation...\n", file=sys.stderr)

    # Fetch data from Google Sheets
    raw_rows = fetch_sheet_data_via_api()

    if raw_rows:
        # Generate dataset
        data = generate_dataset(raw_rows)

        if data:
            # Save to file
            print("\n💾 Saving to data.json...", file=sys.stderr)
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"\n✅ SUCCESS! data.json generated with {data['summary']['total']:,} vulnerabilities", file=sys.stderr)
            print(f"\n📊 Dashboard is ready at index.html", file=sys.stderr)
            print(f"   Open in browser to see all {data['summary']['total']:,} vulnerabilities", file=sys.stderr)
        else:
            print("❌ Failed to generate dataset", file=sys.stderr)
            sys.exit(1)
    else:
        print("❌ Failed to fetch data from Google Sheets", file=sys.stderr)
        print("   Ensure Google credentials are configured", file=sys.stderr)
        sys.exit(1)
