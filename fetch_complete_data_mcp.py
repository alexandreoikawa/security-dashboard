#!/usr/bin/env python3
"""
Fetch COMPLETE data from Página1 via MCP and generate data.json
This script reads all 6,348 vulnerabilities directly from the sheet
"""

import json
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional

def parse_vulnerability(row: List[str], row_num: int) -> Optional[Dict[str, Any]]:
    """Parse a row from Página1 into a vulnerability object"""
    if not row or len(row) < 14:
        return None

    try:
        # Página1 columns:
        # 0: Tipo, 1: Chave, 2: Resumo, 3: Responsável, 4: Prioridade, 5: Status,
        # 6: Categorias, 7: Criado, 8: customfield, 9: Resolvido, 10: The Silence,
        # 11: Sistema, 12: Classificação, 13: Dias Abertos

        chave = (row[1] if len(row) > 1 else '').strip()

        # Skip se não tem chave (linha vazia)
        if not chave:
            return None

        vuln = {
            'tipo': (row[0] if len(row) > 0 else '').strip(),
            'chave': chave,
            'resumo': (row[2] if len(row) > 2 else '').strip(),
            'responsavel': (row[3] if len(row) > 3 else '').strip(),
            'prioridade': (row[4] if len(row) > 4 else '').strip(),
            'status': (row[5] if len(row) > 5 else '').strip(),
            'categorias': (row[6] if len(row) > 6 else '').strip(),
            'criado': (row[7] if len(row) > 7 else '').strip(),
            'customfield': (row[8] if len(row) > 8 else '').strip(),
            'resolvido': (row[9] if len(row) > 9 else '').strip(),
            'the_silence': (row[10] if len(row) > 10 else '').strip(),
            'sistema': (row[11] if len(row) > 11 else '').strip(),
            'classificacao': (row[12] if len(row) > 12 else 'P3').strip(),
            'dias_abertos': int(row[13]) if len(row) > 13 and str(row[13]).isdigit() else 0,
        }

        return vuln
    except Exception as e:
        print(f"⚠️  Erro ao processar linha {row_num}: {e}", file=sys.stderr)
        return None

def process_sheet_data(raw_rows: List[List[str]]) -> Dict[str, Any]:
    """Process raw sheet data into dashboard dataset"""
    if not raw_rows or len(raw_rows) < 2:
        raise ValueError("Dados da sheet insuficientes")

    print(f"📊 Processando {len(raw_rows)} linhas...", file=sys.stderr)

    # Skip header (linha 1)
    vulnerabilities = []
    for i in range(1, len(raw_rows)):
        vuln = parse_vulnerability(raw_rows[i], i)
        if vuln:
            vulnerabilities.append(vuln)

    if not vulnerabilities:
        raise ValueError("Nenhuma vulnerabilidade encontrada")

    print(f"✅ {len(vulnerabilities)} vulnerabilidades processadas", file=sys.stderr)

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
                cat_trim = cat.strip()
                if cat_trim:
                    categories_set.add(cat_trim)
    categories = sorted(list(categories_set))

    # Build dataset
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
            'source': 'Google Sheets - Página1 (via MCP)',
            'total_rows_loaded': total,
            'mcp_authenticated_user': 'alexandre.oikawa@ifood.com.br',
        }
    }

    # Print summary
    print(f"✅ Dataset gerado com sucesso!", file=sys.stderr)
    print(f"   📊 Total: {total:,}", file=sys.stderr)
    print(f"   📁 Backlog: {backlog:,}", file=sys.stderr)
    print(f"   ✓ Concluído: {concluido:,}", file=sys.stderr)
    print(f"   ⏳ Em Progresso: {em_progresso:,}", file=sys.stderr)
    print(f"   🔴 P1: {p1:,}", file=sys.stderr)
    print(f"   🟡 P2: {p2:,}", file=sys.stderr)
    print(f"   🟠 P3: {p3:,}", file=sys.stderr)
    print(f"   🟢 P4: {p4:,}", file=sys.stderr)
    print(f"   👥 Responsáveis: {len(responsibles)}", file=sys.stderr)
    print(f"   🏷️  Categorias: {len(categories)}", file=sys.stderr)

    return dataset

def main():
    """Main function - read from stdin and generate data.json"""
    print("📥 Aguardando dados da Página1...", file=sys.stderr)

    try:
        # Read JSON from stdin
        input_text = sys.stdin.read()
        raw_rows = json.loads(input_text)

        if not isinstance(raw_rows, list):
            raise ValueError("Input deve ser um array JSON")

        # Process data
        dataset = process_sheet_data(raw_rows)

        # Save to file
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)

        print("\n✅ data.json salvo com sucesso!", file=sys.stderr)

    except json.JSONDecodeError as e:
        print(f"❌ Erro ao processar JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
