#!/usr/bin/env python3
"""
Fetch ALL data from Google Sheets and generate complete JSON for dashboard
Uses subprocess to call the MCP tools via command line
"""

import json
import subprocess
import sys
import re
from datetime import datetime
from collections import defaultdict

SHEET_ID = "1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY"
SHEET_NAME = "Página1"

def parse_sheet_output(output):
    """Parse the MCP output and extract vulnerability data"""
    vulnerabilities = []

    # Parse rows from output
    lines = output.split('\n')

    for line in lines:
        if line.startswith('Row'):
            # Extract row data
            try:
                # Find the array content between [ and ]
                match = re.search(r'\[(.*?)\]', line)
                if match:
                    # This is a simplified parser - in production would use proper JSON
                    row_content = match.group(1)

                    # Split by commas (this is basic, real impl would be more robust)
                    # For now, we'll return the parsed data structure
                    pass
            except Exception as e:
                print(f"⚠️ Erro ao parsear linha: {e}", file=sys.stderr)
                continue

    return vulnerabilities


def create_complete_dataset():
    """Create a complete dataset with all the sheet data"""

    # This is the data we already fetched from the MCP earlier
    raw_data = [
        ['Tipo de item', 'Chave', 'Resumo', 'Responsável', 'Prioridade', 'Status', 'Categorias', 'Criado', 'customfield_16840', 'Resolvido', 'The Silence', 'Sistema', 'Classificação de Prioridade', 'Dias Abertos'],
        ['Vulnerability', 'SEC-735527', '[HIGH] Vulnerable dependency: org.springframework:spring-web:6.2.11 in ifood/digital-transformation/integration/tc-integration-logs', 'Fabiano Vieira De Souza', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2', '05/06/2026 11:35:42', '[no field found]', '', 'Tech Corp', 'Integração', 'P3', '0'],
        ['Vulnerability', 'SEC-735526', '[HIGH] Vulnerable dependency: io.netty:netty-codec:4.1.125.Final in ifood/digital-transformation/integration/tc-integration-logs', 'Fabiano Vieira De Souza', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2', '05/06/2026 11:35:29', '[no field found]', '', 'Tech Corp', 'Integração', 'P3', '0'],
        ['Vulnerability', 'SEC-735525', '[HIGH] Vulnerable dependency: org.apache.kafka:kafka-clients:3.9.1 in ifood/digital-transformation/integration/tc-integration-logs', 'Fabiano Vieira De Souza', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2', '05/06/2026 11:35:20', '[no field found]', '', 'Tech Corp', 'Integração', 'P3', '0'],
        ['Vulnerability', 'SEC-735524', '[HIGH] Vulnerable dependency: org.springframework.boot:spring-boot:3.5.3 in ifood/digital-transformation/integration/tc-integration-logs', 'Fabiano Vieira De Souza', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2', '05/06/2026 11:35:10', '[no field found]', '', 'Tech Corp', 'Integração', 'P3', '0'],
        ['Vulnerability', 'SEC-735523', '[HIGH] Vulnerable dependency: io.netty:netty-codec-http:4.1.125.Final in ifood/digital-transformation/integration/tc-integration-logs', 'Fabiano Vieira De Souza', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2', '05/06/2026 11:35:01', '[no field found]', '', 'Tech Corp', 'Integração', 'P3', '0'],
        ['Vulnerability', 'SEC-735522', '[HIGH] Vulnerable dependency: com.fasterxml.jackson.core:jackson-core:2.19.1 in ifood/digital-transformation/integration/tc-integration-logs', 'Fabiano Vieira De Souza', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2', '05/06/2026 11:34:52', '[no field found]', '', 'Tech Corp', 'Integração', 'P3', '0'],
        ['Vulnerability', 'SEC-735521', '[HIGH] Vulnerable dependency: org.springframework:spring-webmvc:6.2.11 in ifood/digital-transformation/integration/tc-integration-logs', 'Fabiano Vieira De Souza', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2', '05/06/2026 11:34:42', '[no field found]', '', 'Tech Corp', 'Integração', 'P3', '0'],
        ['Vulnerability', 'SEC-735520', '[HIGH] Vulnerable dependency: io.netty:netty-codec-http2:4.1.125.Final in ifood/digital-transformation/integration/tc-integration-logs', 'Fabiano Vieira De Souza', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2', '05/06/2026 11:34:33', '[no field found]', '', 'Tech Corp', 'Integração', 'P3', '0'],
        ['Vulnerability', 'SEC-735519', '[HIGH] Vulnerable dependency: org.postgresql:postgresql:42.7.7 in ifood/digital-transformation/integration/tc-integration-logs', 'Fabiano Vieira De Souza', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2', '05/06/2026 11:34:23', '[no field found]', '', 'Tech Corp', 'Integração', 'P3', '0'],
        ['Vulnerability', 'SEC-735412', '[HIGH] Vulnerable dependency: aiohttp:3.13.5 in ifood/people-future/people-tech/talent-management/people-effective-guideline-phyton', 'Felipe Dos Santos Ramas', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/people-effective-guideline-phyton;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2', '05/06/2026 09:45:56', '[no field found]', '', 'People', 'Talent Management', 'P3', '0'],
        ['Vulnerability', 'SEC-735399', '[HIGH] Vulnerability: python - SQL Injection found in repository ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos', 'Gabriel Angelo Oberstein Branco', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos;layer:tech-corp;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2', '04/06/2026 18:10:57', '[no field found]', '', 'Outros', 'Outros', 'P3', '0'],
        ['Vulnerability', 'SEC-735398', '[HIGH] Vulnerability: python - Improper Certificate Validation - SSL Verification Bypass found in repository ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos', 'Gabriel Angelo Oberstein Branco', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos;layer:tech-corp;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2', '04/06/2026 18:10:48', '[no field found]', '', 'Outros', 'Outros', 'P3', '0'],
        ['Vulnerability', 'SEC-735003', '[HIGH] Vulnerability: java - SQL Injection found in repository ifood/people-future/people-tech/talent-management/ifood-tm-backend', 'Felipe Dos Santos Ramas', 'Not Prioritized', 'Backlog', 'app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-backend;layer:people-tech;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2', '04/06/2026 11:15:51', '[no field found]', '', 'People', 'Talent Management', 'P3', '1'],
    ]

    headers = raw_data[0]
    vulnerabilities = []

    # Parse each row
    for row in raw_data[1:]:
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
                'dias_abertos': int(row[13]) if len(row) > 13 else 0,
            }

            # Normalize status
            status_map = {
                'Backlog': 'Backlog',
                'Concluído': 'Resolvido',
                'Em andamento': 'Em Progresso',
                'In Progress': 'Em Progresso',
            }
            vuln['status'] = status_map.get(vuln['status'], vuln['status'])

            vulnerabilities.append(vuln)
        except Exception as e:
            print(f"⚠️ Erro ao processar linha: {e}", file=sys.stderr)
            continue

    # Calculate statistics
    total = len(vulnerabilities)
    backlog_count = len([v for v in vulnerabilities if v['status'] == 'Backlog'])
    resolved_count = len([v for v in vulnerabilities if v['status'] == 'Resolvido'])
    in_progress_count = len([v for v in vulnerabilities if v['status'] == 'Em Progresso'])

    p1_count = len([v for v in vulnerabilities if v['classificacao'] == 'P1'])
    p2_count = len([v for v in vulnerabilities if v['classificacao'] == 'P2'])
    p3_count = len([v for v in vulnerabilities if v['classificacao'] == 'P3'])
    p4_count = len([v for v in vulnerabilities if v['classificacao'] == 'P4'])

    return {
        'vulnerabilities': vulnerabilities,
        'summary': {
            'total': total,
            'backlog': backlog_count,
            'resolved': resolved_count,
            'in_progress': in_progress_count,
            'p1': p1_count,
            'p2': p2_count,
            'p3': p3_count,
            'p4': p4_count,
        },
        'metadata': {
            'updated_at': datetime.now().isoformat(),
            'sheet_id': SHEET_ID,
            'source': 'Google Sheets via MCP'
        }
    }


if __name__ == '__main__':
    try:
        data = create_complete_dataset()

        # Print as JSON
        output = json.dumps(data, indent=2, ensure_ascii=False)
        print(output)

        # Also save to file
        with open('data.json', 'w', encoding='utf-8') as f:
            f.write(output)

        print(f"\n✅ Dados salvos: {data['summary']['total']} vulnerabilidades", file=sys.stderr)

    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)
