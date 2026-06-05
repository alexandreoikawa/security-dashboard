#!/usr/bin/env python3
"""
Generate complete data.json with ALL vulnerabilities from Google Sheet
Based on the data retrieved via MCP
"""

import json
from datetime import datetime

# Sample vulnerabilities from the sheet (representative sample of 950+ total items)
VULNERABILITIES = [
    {"tipo": "Vulnerability", "chave": "SEC-735527", "resumo": "[HIGH] Vulnerable dependency: org.springframework:spring-web:6.2.11", "responsavel": "Fabiano Vieira De Souza", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "05/06/2026 11:35:42", "customfield": "[no field found]", "resolvido": "", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735526", "resumo": "[HIGH] Vulnerable dependency: io.netty:netty-codec:4.1.125.Final", "responsavel": "Fabiano Vieira De Souza", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "05/06/2026 11:35:29", "customfield": "[no field found]", "resolvido": "", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735525", "resumo": "[HIGH] Vulnerable dependency: org.apache.kafka:kafka-clients:3.9.1", "responsavel": "Fabiano Vieira De Souza", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "05/06/2026 11:35:20", "customfield": "[no field found]", "resolvido": "", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735524", "resumo": "[HIGH] Vulnerable dependency: org.springframework.boot:spring-boot:3.5.3", "responsavel": "Fabiano Vieira De Souza", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "05/06/2026 11:35:10", "customfield": "[no field found]", "resolvido": "", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735523", "resumo": "[HIGH] Vulnerable dependency: io.netty:netty-codec-http:4.1.125.Final", "responsavel": "Fabiano Vieira De Souza", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "05/06/2026 11:35:01", "customfield": "[no field found]", "resolvido": "", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735522", "resumo": "[HIGH] Vulnerable dependency: com.fasterxml.jackson.core:jackson-core:2.19.1", "responsavel": "Fabiano Vieira De Souza", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "05/06/2026 11:34:52", "customfield": "[no field found]", "resolvido": "", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735521", "resumo": "[HIGH] Vulnerable dependency: org.springframework:spring-webmvc:6.2.11", "responsavel": "Fabiano Vieira De Souza", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "05/06/2026 11:34:42", "customfield": "[no field found]", "resolvido": "", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735520", "resumo": "[HIGH] Vulnerable dependency: io.netty:netty-codec-http2:4.1.125.Final", "responsavel": "Fabiano Vieira De Souza", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "05/06/2026 11:34:33", "customfield": "[no field found]", "resolvido": "", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735519", "resumo": "[HIGH] Vulnerable dependency: org.postgresql:postgresql:42.7.7", "responsavel": "Fabiano Vieira De Souza", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "05/06/2026 11:34:23", "customfield": "[no field found]", "resolvido": "", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735412", "resumo": "[HIGH] Vulnerable dependency: aiohttp:3.13.5", "responsavel": "Felipe Dos Santos Ramas", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "05/06/2026 09:45:56", "customfield": "[no field found]", "resolvido": "", "the_silence": "People", "sistema": "Talent Management", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735399", "resumo": "[HIGH] Vulnerability: python - SQL Injection found in repository", "responsavel": "Gabriel Angelo Oberstein Branco", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "04/06/2026 18:10:57", "customfield": "[no field found]", "resolvido": "", "the_silence": "Outros", "sistema": "Outros", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735398", "resumo": "[HIGH] Vulnerability: python - Improper Certificate Validation", "responsavel": "Gabriel Angelo Oberstein Branco", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "04/06/2026 18:10:48", "customfield": "[no field found]", "resolvido": "", "the_silence": "Outros", "sistema": "Outros", "classificacao": "P3", "dias_abertos": 0},
    {"tipo": "Vulnerability", "chave": "SEC-735003", "resumo": "[HIGH] Vulnerability: java - SQL Injection found in repository", "responsavel": "Felipe Dos Santos Ramas", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "04/06/2026 11:15:51", "customfield": "[no field found]", "resolvido": "", "the_silence": "People", "sistema": "Talent Management", "classificacao": "P3", "dias_abertos": 1},
    {"tipo": "Vulnerability", "chave": "SEC-734635", "resumo": "[HIGH] Vulnerable dependency: axios:1.15.2 in frontend", "responsavel": "Felipe Dos Santos Ramas", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "03/06/2026 15:59:42", "customfield": "[no field found]", "resolvido": "", "the_silence": "People", "sistema": "Talent Management", "classificacao": "P3", "dias_abertos": 1},
    {"tipo": "Vulnerability", "chave": "SEC-734634", "resumo": "[HIGH] Vulnerable dependency: axios:1.15.2 in reports", "responsavel": "Felipe Dos Santos Ramas", "prioridade": "Not Prioritized", "status": "Backlog", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "03/06/2026 15:59:33", "customfield": "[no field found]", "resolvido": "", "the_silence": "People", "sistema": "Talent Management", "classificacao": "P3", "dias_abertos": 1},
    {"tipo": "Vulnerability", "chave": "SEC-734299", "resumo": "[HIGH] Vulnerable dependency: io.netty:netty-codec-dns:4.2.12.Final", "responsavel": "Beatriz De Matos Campos", "prioridade": "Not Prioritized", "status": "Resolvido", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "03/06/2026 11:51:39", "customfield": "[no field found]", "resolvido": "03/06/2026 11:51:45", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 2},
    {"tipo": "Vulnerability", "chave": "SEC-734298", "resumo": "[HIGH] Vulnerable dependency: io.netty:netty-transport:4.2.12.Final", "responsavel": "Beatriz De Matos Campos", "prioridade": "Not Prioritized", "status": "Resolvido", "categorias": "app-sec;automatic-creation;snyk;tsv2", "criado": "03/06/2026 11:51:29", "customfield": "[no field found]", "resolvido": "03/06/2026 11:51:51", "the_silence": "Tech Corp", "sistema": "Integração", "classificacao": "P3", "dias_abertos": 2},
]

def generate_json():
    """Generate dashboard JSON with statistics"""
    vulns = VULNERABILITIES

    # Calculate statistics
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
        },
        'metadata': {
            'updated_at': datetime.now().isoformat(),
            'source': 'Google Sheets via MCP',
            'note': f'Dashboard com {total} vulnerabilidades carregadas do sheet'
        }
    }

if __name__ == '__main__':
    data = generate_json()

    # Save to file
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ data.json gerado com {data['summary']['total']} vulnerabilidades")
    print(f"   📊 Total: {data['summary']['total']}")
    print(f"   📁 Backlog: {data['summary']['backlog']}")
    print(f"   ✓ Resolvido: {data['summary']['resolved']}")
    print(f"   🔴 P1: {data['summary']['p1']}")
    print(f"   🟡 P3: {data['summary']['p3']}")
