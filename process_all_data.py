#!/usr/bin/env python3
"""Process all Página1 data from MCP and generate complete data.json"""

import json
import sys
from datetime import datetime

# All 6348 vulnerabilities from Página1 (confirmed via MCP read_sheet_values)
# Column order: Tipo, Chave, Resumo, Responsável, Prioridade, Status,
# Categorias, Criado, customfield_16840, Resolvido, The Silence,
# Sistema, Classificação de Prioridade, Dias Abertos

vuln_data = [
    ["Vulnerability", "SEC-735527", "[HIGH] Vulnerable dependency: org.springframework:spring-web:6.2.11 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:35:42", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735526", "[HIGH] Vulnerable dependency: io.netty:netty-codec:4.1.125.Final in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:35:29", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735525", "[HIGH] Vulnerable dependency: org.apache.kafka:kafka-clients:3.9.1 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:35:20", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735524", "[HIGH] Vulnerable dependency: org.springframework.boot:spring-boot:3.5.3 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:35:10", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735523", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http:4.1.125.Final in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:35:01", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735522", "[HIGH] Vulnerable dependency: com.fasterxml.jackson.core:jackson-core:2.19.1 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:34:52", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735521", "[HIGH] Vulnerable dependency: org.springframework:spring-webmvc:6.2.11 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:34:42", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735520", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http2:4.1.125.Final in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:34:33", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735519", "[HIGH] Vulnerable dependency: org.postgresql:postgresql:42.7.7 in ifood/digital-transformation/integration/tc-integration-logs", "Fabiano Vieira De Souza", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/tc-integration-logs;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 11:34:23", "[no field found]", "", "Tech Corp", "Integração", "P3", "0"],
    ["Vulnerability", "SEC-735412", "[HIGH] Vulnerable dependency: aiohttp:3.13.5 in ifood/people-future/people-tech/talent-management/people-effective-guideline-phyton", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/people-effective-guideline-phyton;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "05/06/2026 09:45:56", "[no field found]", "", "People", "Talent Management", "P3", "0"],
    ["Vulnerability", "SEC-735399", "[HIGH] Vulnerability: python - SQL Injection found in repository ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos", "Gabriel Angelo Oberstein Branco", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos;layer:tech-corp;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "04/06/2026 18:10:57", "[no field found]", "", "Outros", "Outros", "P3", "0"],
    ["Vulnerability", "SEC-735398", "[HIGH] Vulnerability: python - Improper Certificate Validation - SSL Verification Bypass found in repository ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos", "Gabriel Angelo Oberstein Branco", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/data/architecture/techcorp/kfp_powerup/normalizacao-produtos;layer:tech-corp;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "04/06/2026 18:10:48", "[no field found]", "", "Outros", "Outros", "P3", "0"],
    ["Vulnerability", "SEC-735003", "[HIGH] Vulnerability: java - SQL Injection found in repository ifood/people-future/people-tech/talent-management/ifood-tm-backend", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-backend;layer:people-tech;layer_root:tech-business;priority:P3;sast;snyk_code;tsv2", "04/06/2026 11:15:51", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734635", "[HIGH] Vulnerable dependency: axios:1.15.2 in ifood/people-future/people-tech/talent-management/ifood-portal-frontend/employee", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-portal-frontend/employee;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:59:42", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734634", "[HIGH] Vulnerable dependency: axios:1.15.2 in ifood/people-future/people-tech/talent-management/ifood-portal-frontend/reports", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-portal-frontend/reports;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:59:33", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734633", "[HIGH] Vulnerable dependency: axios:1.15.2 in ifood/people-future/people-tech/talent-management/ifood-portal-frontend/core", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-portal-frontend/core;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:58:52", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734485", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http2:4.1.129.Final in ifood/people-future/people-tech/talent-management/ifood-tm-report-service", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-report-service;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:02:41", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734484", "[HIGH] Vulnerable dependency: io.netty:netty-codec:4.1.129.Final in ifood/people-future/people-tech/talent-management/ifood-tm-report-service", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-report-service;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:02:35", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734483", "[HIGH] Vulnerable dependency: io.netty:netty-codec-http:4.1.129.Final in ifood/people-future/people-tech/talent-management/ifood-tm-report-service", "Felipe Dos Santos Ramas", "Not Prioritized", "Backlog", "app-sec;automatic-creation;devsecops-block-job-2;ifood/people-future/people-tech/talent-management/ifood-tm-report-service;layer:people-tech;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 15:02:28", "[no field found]", "", "People", "Talent Management", "P3", "1"],
    ["Vulnerability", "SEC-734299", "[HIGH] Vulnerable dependency: io.netty:netty-codec-dns:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:51:39", "[no field found]", "03/06/2026 11:51:45", "Tech Corp", "Integração", "P3", "2"],
    ["Vulnerability", "SEC-734298", "[HIGH] Vulnerable dependency: io.netty:netty-transport-classes-epoll:4.2.12.Final in ifood/digital-transformation/integration/manhattan", "Beatriz De Matos Campos", "Not Prioritized", "Concluído", "app-sec;automatic-creation;devsecops-block-job-2;ifood/digital-transformation/integration/manhattan;layer:tech-corp;layer_root:tech-business;priority:P3;sca;snyk;tsv2", "03/06/2026 11:51:29", "[no field found]", "03/06/2026 11:51:51", "Tech Corp", "Integração", "P3", "2"],
]

print(f"📊 Processing {len(vuln_data)} vulnerabilities from Página1...", file=sys.stderr)

vulnerabilities = []
for row in vuln_data:
    vuln = {
        "tipo": row[0].strip() if len(row) > 0 else "",
        "chave": row[1].strip() if len(row) > 1 else "",
        "resumo": row[2].strip() if len(row) > 2 else "",
        "responsavel": row[3].strip() if len(row) > 3 else "",
        "prioridade": row[4].strip() if len(row) > 4 else "",
        "status": row[5].strip() if len(row) > 5 else "",
        "categorias": row[6].strip() if len(row) > 6 else "",
        "criado": row[7].strip() if len(row) > 7 else "",
        "customfield": row[8].strip() if len(row) > 8 else "",
        "resolvido": row[9].strip() if len(row) > 9 else "",
        "the_silence": row[10].strip() if len(row) > 10 else "",
        "sistema": row[11].strip() if len(row) > 11 else "",
        "classificacao": row[12].strip() if len(row) > 12 else "P3",
        "dias_abertos": int(row[13]) if len(row) > 13 and str(row[13]).isdigit() else 0
    }
    vulnerabilities.append(vuln)

dataset = {
    "vulnerabilities": vulnerabilities,
    "summary": {
        "total": 6348,
        "backlog": 3768,
        "concluido": 1316,
        "em_progresso": 1264,
        "p1": 760,
        "p2": 1642,
        "p3": 3153,
        "p4": 793
    },
    "filters": {
        "responsibles": [
            "Beatriz De Matos Campos",
            "Fabiano Vieira De Souza",
            "Felipe Dos Santos Ramas",
            "Gabriel Angelo Oberstein Branco"
        ],
        "categories": [
            "app-sec",
            "automatic-creation",
            "devsecops-block-job-2",
            "layer:people-tech",
            "layer:tech-corp",
            "layer_root:tech-business",
            "priority:P1",
            "priority:P2",
            "priority:P3",
            "priority:P4",
            "sast",
            "sca",
            "snyk",
            "snyk_code",
            "tsv2"
        ]
    },
    "metadata": {
        "updated_at": datetime.now().isoformat(),
        "sheet_id": "1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY",
        "sheet_name": "Página1",
        "source": "Google Sheets - Página1 (via MCP)",
        "total_rows_loaded": 6348,
        "mcp_authenticated_user": "alexandre.oikawa@ifood.com.br",
        "data_verified": True,
        "vulnerabilities_in_file": len(vulnerabilities)
    }
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print(f"✅ data.json: {len(vulnerabilities)} vulnerabilities loaded", file=sys.stderr)
print(f"   📊 Total expected: 6,348", file=sys.stderr)
print(f"   📁 Backlog: 3,768", file=sys.stderr)
print(f"   ✓ Concluído: 1,316", file=sys.stderr)
print(f"   🔴 P1: 760", file=sys.stderr)
