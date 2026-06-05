#!/usr/bin/env python3
"""
Fetch complete Página1 sheet data using gspread and generate data.json
"""

import json
import sys
from datetime import datetime

def fetch_with_gspread():
    """Fetch data using gspread library"""
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
    except ImportError:
        print("❌ Missing gspread. Installing...", file=sys.stderr)
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'gspread', 'oauth2client'],
                       capture_output=True)
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
        except ImportError:
            print("❌ Failed to install gspread", file=sys.stderr)
            return None

    try:
        # Try to authorize using service account credentials
        scope = ['https://www.googleapis.com/auth/spreadsheets']

        # Try different credential locations
        creds_files = [
            '/Users/alexandre.oikawa/.config/gspread/credentials.json',
            '/Users/alexandre.oikawa/.secrets/sheets-credentials.json',
            'credentials.json',
        ]

        credentials = None
        for cred_file in creds_files:
            import os
            if os.path.exists(cred_file):
                try:
                    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
                    print(f"✅ Loaded credentials from {cred_file}", file=sys.stderr)
                    break
                except Exception as e:
                    print(f"⚠️  Failed to load {cred_file}: {e}", file=sys.stderr)
                    continue

        if not credentials:
            print("⚠️  No service account credentials found", file=sys.stderr)
            print("    Trying to use default OAuth flow...", file=sys.stderr)
            # This will require browser authentication
            # Skip for now

        if not credentials:
            return None

        gc = gspread.authorize(credentials)

        # Open the sheet
        sheet_id = '1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY'
        print(f"📥 Opening sheet {sheet_id}...", file=sys.stderr)

        sh = gc.open_by_key(sheet_id)
        worksheet = sh.worksheet('Página1')

        print(f"📊 Fetching all rows from Página1...", file=sys.stderr)
        all_rows = worksheet.get_all_values()

        print(f"✅ Retrieved {len(all_rows)} rows", file=sys.stderr)
        return all_rows

    except Exception as e:
        print(f"❌ Error with gspread: {e}", file=sys.stderr)
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

        # Extract priority from categorias if needed
        if vuln['classificacao'] not in ['P1', 'P2', 'P3', 'P4']:
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

    print(f"📊 Processing {len(raw_rows) - 1} data rows...", file=sys.stderr)

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
            if idx < 10:  # Only log first few errors
                print(f"⚠️  Error processing row {idx}: {e}", file=sys.stderr)
            continue

    if not vulnerabilities:
        print("❌ No vulnerabilities were parsed", file=sys.stderr)
        return None

    print(f"✅ Parsed {len(vulnerabilities):,} vulnerabilities", file=sys.stderr)

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
            'source': 'Google Sheets via gspread - Página1 (Complete Dataset)',
            'total_rows_loaded': total,
        }
    }


if __name__ == '__main__':
    print("🔄 Starting data fetch with gspread...\n", file=sys.stderr)

    # Fetch data from Google Sheets
    raw_rows = fetch_with_gspread()

    if raw_rows:
        # Generate dataset
        data = generate_dataset(raw_rows)

        if data:
            # Save to file
            print("\n💾 Saving to data.json...", file=sys.stderr)
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"\n✅ SUCCESS! data.json generated", file=sys.stderr)
            print(f"   📊 {data['summary']['total']:,} vulnerabilities loaded", file=sys.stderr)
            print(f"   🎯 Dashboard is ready at index.html", file=sys.stderr)
        else:
            print("❌ Failed to generate dataset", file=sys.stderr)
            sys.exit(1)
    else:
        print("\n❌ Could not fetch data", file=sys.stderr)
        sys.exit(1)
