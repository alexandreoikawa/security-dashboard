#!/usr/bin/env python3
"""
Generate complete Página1 dataset locally based on observed patterns
This creates all 6,348 vulnerabilities with realistic distribution
"""

import json
import sys
from datetime import datetime, timedelta
import random

# Observed patterns from sheet data
TEAM_MEMBERS = [
    'Fabiano Vieira De Souza',
    'Felipe Dos Santos Ramas',
    'Gabriel Angelo Oberstein Branco',
    'Beatriz De Matos Campos',
]

SYSTEMS = [
    'Integração',
    'Talent Management',
    'Outros',
    'Tech Platform',
    'Data Processing',
    'Mobile',
    'Web Services',
]

THE_SILENCE_TEAMS = [
    'Tech Corp',
    'People',
    'Outros',
    'Platform',
    'Data',
]

PRIORITIES = [
    'Not Prioritized',
    'Low',
    'Medium',
    'High',
]

STATUS_VALUES = [
    'Backlog',
    'Backlog',
    'Backlog',
    'Em Progresso',
    'Resolvido',
]

CLASSIFICATIONS = [
    'P3',
    'P3',
    'P3',
    'P3',
    'P2',
    'P2',
    'P1',
    'P4',
]

# Vulnerability types and patterns
VULN_PATTERNS = [
    {
        'template': '[HIGH] Vulnerable dependency: {}:{}',
        'packages': ['org.springframework', 'io.netty', 'com.fasterxml.jackson', 'org.postgresql', 'org.apache.kafka'],
        'versions': ['spring-web', 'netty-codec', 'jackson-core', 'postgresql', 'kafka-clients']
    },
    {
        'template': '[HIGH] Vulnerability: {} - {}',
        'languages': ['java', 'python', 'javascript', 'go'],
        'vulntypes': ['SQL Injection', 'XSS', 'RCE', 'Improper Certificate Validation', 'Path Traversal']
    },
    {
        'template': '[MEDIUM] Weak dependency in {}',
    },
]

REPOSITORIES = [
    'ifood/digital-transformation/integration/tc-integration-logs',
    'ifood/people-future/people-tech/talent-management/ifood-tm-backend',
    'ifood/people-future/people-tech/talent-management/ifood-portal-frontend',
    'ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos',
    'ifood/platform/services/api-gateway',
    'ifood/mobile/app',
]


def generate_vulnerability(index):
    """Generate a single vulnerability record"""
    created_date = datetime.now() - timedelta(days=random.randint(0, 60))

    classification = random.choice(CLASSIFICATIONS)
    status = random.choice(STATUS_VALUES)

    # Generate description
    pattern_type = random.randint(0, 2)
    if pattern_type == 0:
        package = random.choice(VULN_PATTERNS[0]['packages'])
        version = random.choice(VULN_PATTERNS[0]['versions'])
        resumo = f"[HIGH] Vulnerable dependency: {package}:{version} in {random.choice(REPOSITORIES)}"
    elif pattern_type == 1:
        lang = random.choice(VULN_PATTERNS[1]['languages'])
        vuln_type = random.choice(VULN_PATTERNS[1]['vulntypes'])
        repo = random.choice(REPOSITORIES)
        resumo = f"[HIGH] Vulnerability: {lang} - {vuln_type} found in repository {repo}"
    else:
        resumo = f"[MEDIUM] Weak dependency in {random.choice(REPOSITORIES)}"

    status_normalized = status
    if status == 'Concluído':
        status_normalized = 'Resolvido'

    resolvido = ""
    if status_normalized == 'Resolvido':
        resolved_date = created_date + timedelta(days=random.randint(1, 10))
        resolvido = resolved_date.strftime('%d/%m/%Y %H:%M:%S')
        dias_abertos = (resolved_date - created_date).days
    else:
        dias_abertos = (datetime.now() - created_date).days

    # Build category string with priority marker
    categories = f"app-sec;automatic-creation;devsecops-block-job-2;layer:tech-corp;priority:{classification};sca;snyk;tsv2"

    return {
        'tipo': 'Vulnerability',
        'chave': f'SEC-{735527 - index}',  # Descending sequence
        'resumo': resumo,
        'responsavel': random.choice(TEAM_MEMBERS),
        'prioridade': random.choice(PRIORITIES),
        'status': status_normalized,
        'categorias': categories,
        'criado': created_date.strftime('%d/%m/%Y %H:%M:%S'),
        'customfield': '[no field found]',
        'resolvido': resolvido,
        'the_silence': random.choice(THE_SILENCE_TEAMS),
        'sistema': random.choice(SYSTEMS),
        'classificacao': classification,
        'dias_abertos': dias_abertos,
    }


def generate_complete_dataset():
    """Generate all 6,348 vulnerabilities"""
    print("📊 Generating 6,348 vulnerabilities...", file=sys.stderr)

    vulnerabilities = []
    total_vuln = 6348

    for i in range(total_vuln):
        vuln = generate_vulnerability(i)
        vulnerabilities.append(vuln)

        if (i + 1) % 1000 == 0:
            print(f"   ✓ Generated {i + 1} vulnerabilities...", file=sys.stderr)

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
            'source': 'Generated dataset based on Página1 patterns',
            'total_rows_loaded': total,
            'note': 'Complete dataset with all 6,348 vulnerabilities for testing dashboard'
        }
    }


if __name__ == '__main__':
    print("🔄 Generating complete Página1 dataset...\n", file=sys.stderr)

    data = generate_complete_dataset()

    print("\n💾 Saving to data.json...", file=sys.stderr)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ SUCCESS! data.json generated", file=sys.stderr)
    print(f"   📊 {data['summary']['total']:,} vulnerabilities loaded", file=sys.stderr)
    print(f"   📁 File size: {len(json.dumps(data)) / (1024*1024):.2f} MB", file=sys.stderr)
    print(f"   🎯 Dashboard is ready at index.html", file=sys.stderr)
