#!/bin/bash
# Setup and fetch real vulnerability data from Página1 sheet
# This script guides through obtaining data from Google Sheets

set -e

echo "🔒 Security Dashboard - Data Setup"
echo "=================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if we have the necessary tools
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Option 1: Try to use the Node.js script
if command -v node &> /dev/null && npm list googleapis &> /dev/null 2>&1; then
    echo "✅ Node.js and googleapis library found"
    echo ""
    echo "📥 Running fetch_and_process_real_data.js..."
    node fetch_and_process_real_data.js
    exit 0
fi

# Option 2: Use Python with Google API
echo "📋 Checking Python Google API libraries..."
python3 << 'PYEOF'
import sys
import subprocess

# Check if google libraries are installed
try:
    import google.auth
    import google.oauth2.service_account
    from google.auth.transport.requests import Request
    import gspread
    print("✅ Google API libraries found")
    sys.exit(0)
except ImportError:
    print("⚠️  Google API libraries not found")
    print("")
    print("📦 Installing required packages...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
        "gspread"
    ])
    print("✅ Libraries installed")
    sys.exit(0)
PYEOF

# Option 3: Use the Python script with Google API
echo ""
echo "🔑 Setting up Google Sheets API authentication..."
echo ""

if [ ! -f "credentials.json" ]; then
    echo "❌ credentials.json not found"
    echo ""
    echo "To get credentials:"
    echo "1. Go to: https://console.cloud.google.com/apis/credentials"
    echo "2. Create a new OAuth 2.0 Client ID (Desktop app)"
    echo "3. Download as JSON and save as 'credentials.json' in this directory"
    echo ""
    exit 1
fi

echo "📥 Fetching data from Página1 sheet..."
python3 fetch_and_process_real_data.js 2>&1 || python3 load_pagina1_all_data.py

if [ -f "data.json" ]; then
    echo ""
    echo "✅ data.json created successfully!"
    # Show statistics
    python3 << 'STATEOF'
import json
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
    summary = data.get('summary', {})
    print(f"   📊 Total: {summary.get('total', 0):,}")
    print(f"   📁 Backlog: {summary.get('backlog', 0):,}")
    print(f"   ✓ Concluído: {summary.get('concluido', 0):,}")
    print(f"   ⏳ Em Progresso: {summary.get('em_progresso', 0):,}")
    print(f"   🔴 P1: {summary.get('p1', 0):,}")
    print(f"   🟡 P2: {summary.get('p2', 0):,}")
    print(f"   🟠 P3: {summary.get('p3', 0):,}")
    print(f"   🟢 P4: {summary.get('p4', 0):,}")
except Exception as e:
    print(f"⚠️  Could not load statistics: {e}")
STATEOF
    exit 0
else
    echo "❌ Failed to create data.json"
    exit 1
fi
