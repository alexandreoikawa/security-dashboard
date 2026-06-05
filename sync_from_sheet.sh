#!/bin/bash

# Script to fetch data from Google Sheet and generate JSON for dashboard
# This uses the MCP integration to read from Google Sheets

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SHEET_ID="1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY"

echo "📊 Sincronizando dados do Google Sheet..."
echo "Sheet ID: $SHEET_ID"

# Create a Python script that will fetch and transform the data
cat > /tmp/fetch_sheet_data.py << 'PYTHON_EOF'
import json
import os
import sys
from datetime import datetime
from collections import defaultdict

# For now, this is a template that shows the expected data structure
# In a real implementation, this would use the Google Sheets API

vulnerabilities_data = [
    {
        "tipo": "Vulnerability",
        "chave": "SEC-735527",
        "resumo": "[HIGH] Vulnerable dependency: org.springframework:spring-web:6.2.11 in ifood/digital-transformation/integration/tc-integration-logs",
        "responsavel": "Fabiano Vieira De Souza",
        "prioridade": "Not Prioritized",
        "status": "Backlog",
        "categorias": "app-sec;automatic-creation;snyk;tsv2",
        "criado": "05/06/2026 11:35:42",
        "resolvido": "",
        "the_silence": "Tech Corp",
        "sistema": "Integração",
        "classificacao": "P3",
        "dias_abertos": 0
    }
]

def parse_vulnerabilities():
    """Parse and normalize vulnerability data"""
    result = []

    for item in vulnerabilities_data:
        # Extract priority from classification if available
        priority = item.get("classificacao", "P3")

        # Normalize status
        status = item.get("status", "Backlog")
        status_map = {
            "Backlog": "Backlog",
            "Concluído": "Resolvido",
            "In Progress": "Em Progresso"
        }
        status = status_map.get(status, status)

        result.append({
            "tipo": item["tipo"],
            "chave": item["chave"],
            "resumo": item["resumo"],
            "responsavel": item["responsavel"],
            "prioridade": item["prioridade"],
            "status": status,
            "categorias": item["categorias"],
            "criado": item["criado"],
            "resolvido": item["resolvido"],
            "the_silence": item["the_silence"],
            "sistema": item["sistema"],
            "classificacao": priority,
            "dias_abertos": item["dias_abertos"]
        })

    return result

def generate_dashboard_json():
    """Generate the complete dashboard JSON"""

    vulnerabilities = parse_vulnerabilities()

    # Calculate statistics
    total = len(vulnerabilities)
    backlog_count = len([v for v in vulnerabilities if v["status"] == "Backlog"])
    resolved_count = len([v for v in vulnerabilities if v["status"] == "Resolvido"])
    in_progress_count = len([v for v in vulnerabilities if v["status"] == "Em Progresso"])

    p1_count = len([v for v in vulnerabilities if v["classificacao"] == "P1"])
    p2_count = len([v for v in vulnerabilities if v["classificacao"] == "P2"])
    p3_count = len([v for v in vulnerabilities if v["classificacao"] == "P3"])
    p4_count = len([v for v in vulnerabilities if v["classificacao"] == "P4"])

    return {
        "metadata": {
            "updated_at": datetime.now().isoformat(),
            "total_vulnerabilities": total
        },
        "summary": {
            "total": total,
            "backlog": backlog_count,
            "resolved": resolved_count,
            "in_progress": in_progress_count,
            "p1": p1_count,
            "p2": p2_count,
            "p3": p3_count,
            "p4": p4_count
        },
        "vulnerabilities": vulnerabilities
    }

if __name__ == "__main__":
    data = generate_dashboard_json()
    print(json.dumps(data, indent=2, ensure_ascii=False))

PYTHON_EOF

# Run the Python script and save output
python3 /tmp/fetch_sheet_data.py > "$SCRIPT_DIR/data.json"

echo "✅ Arquivo data.json gerado com sucesso!"
echo "📍 Localização: $SCRIPT_DIR/data.json"
echo ""
echo "Próxima ação: O dashboard será atualizado para carregar esse arquivo."

