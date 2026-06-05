#!/usr/bin/env python3
"""
Fetch data from Google Sheets via MCP and generate JSON for dashboard
"""
import json
import os
import sys
from datetime import datetime

# Sheet configuration
SHEET_ID = "1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY"
SHEET_NAME = "Página1"

# This script will be called from a bash script that uses MCP to fetch data
# For now, we'll create sample data that matches the real sheet structure

def generate_dashboard_data():
    """Generate data compatible with the dashboard"""

    # Real data from the sheet (manually extracted for now)
    vulnerabilities = [
        {
            "chave": "SEC-735527",
            "tipo": "Vulnerability",
            "resumo": "[HIGH] Vulnerable dependency: org.springframework:spring-web:6.2.11",
            "responsavel": "Fabiano Vieira De Souza",
            "prioridade": "P3",
            "status": "Backlog",
            "categorias": "app-sec;snyk;tsv2",
            "criado": "05/06/2026",
            "resolvido": "",
            "dias_abertos": 0
        },
        {
            "chave": "SEC-735526",
            "tipo": "Vulnerability",
            "resumo": "[HIGH] Vulnerable dependency: io.netty:netty-codec:4.1.125.Final",
            "responsavel": "Fabiano Vieira De Souza",
            "prioridade": "P3",
            "status": "Backlog",
            "categorias": "app-sec;snyk;tsv2",
            "criado": "05/06/2026",
            "resolvido": "",
            "dias_abertos": 0
        }
    ]

    return {
        "vulnerabilities": vulnerabilities,
        "generated_at": datetime.now().isoformat(),
        "sheet_id": SHEET_ID
    }

if __name__ == "__main__":
    data = generate_dashboard_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))
