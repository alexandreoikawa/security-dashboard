# 📊 Real Data Setup Guide

This guide explains how to fetch real vulnerability data from the Página1 Google Sheet and populate the security dashboard.

## Quick Start

### Option 1: Using Node.js (Recommended)

If you have Node.js installed with the `googleapis` library:

```bash
npm install googleapis google-auth-library
node fetch_and_process_real_data.js
```

The script will:
1. Request authentication (opens browser)
2. Fetch all 6,348 rows from Página1
3. Generate `data.json` with real vulnerability data
4. Display statistics

### Option 2: Using Python

If you prefer Python:

```bash
# Install dependencies
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client gspread

# Run the setup script
bash setup_and_fetch_data.sh
```

Or directly:

```bash
python3 load_pagina1_all_data.py
```

### Option 3: Using the Automated Setup Script

```bash
chmod +x setup_and_fetch_data.sh
./setup_and_fetch_data.sh
```

---

## Manual Setup (For Troubleshooting)

### Step 1: Get Google API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project or select existing one
3. Enable the Google Sheets API:
   - Click "Enable APIs and Services"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop application"
   - Download the JSON file
   - Save as `credentials.json` in this directory

### Step 2: Run the Data Fetch Script

**Node.js Method:**
```bash
npm install googleapis
node fetch_and_process_real_data.js
```

**Python Method:**
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client gspread
python3 load_pagina1_all_data.py
```

### Step 3: Verify the Data

Check that `data.json` was created:

```bash
# Show file size
ls -lh data.json

# Show data statistics
python3 -c "import json; data=json.load(open('data.json')); print(f'Loaded {data[\"summary\"][\"total\"]:,} vulnerabilities')"
```

---

## Expected Data Statistics

When you have successfully fetched the real data, you should see:

```
✅ data.json generated successfully!
   📊 Total: 6,348
   📁 Backlog: 3,768
   ✓ Concluído: 1,316
   ⏳ Em Progresso: 1,264
   🔴 P1: 760
   🟡 P2: 1,642
   🟠 P3: 3,153
   🟢 P4: 793
   👥 Responsibles: 4
   🏷️  Categories: 11+
```

---

## Data Structure

The `data.json` file contains:

```json
{
  "vulnerabilities": [
    {
      "tipo": "Vulnerability",
      "chave": "SEC-735527",
      "resumo": "[HIGH] Vulnerable dependency...",
      "responsavel": "Fabiano Vieira De Souza",
      "prioridade": "Not Prioritized",
      "status": "Backlog",
      "categorias": "app-sec;automatic-creation;...",
      "criado": "05/06/2026 11:35:42",
      "customfield": "[no field found]",
      "resolvido": "",
      "the_silence": "",
      "sistema": "Tech Corp",
      "classificacao": "P3",
      "dias_abertos": 0
    }
    // ... 6,347 more vulnerabilities
  ],
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
    "responsibles": ["Beatriz De Matos Campos", "Fabiano Vieira De Souza", ...],
    "categories": ["app-sec", "automatic-creation", ...]
  },
  "metadata": {
    "updated_at": "2026-06-05T...",
    "sheet_id": "1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY",
    "sheet_name": "Página1",
    "source": "Google Sheets - Página1 (Real Data)",
    "total_rows_loaded": 6348
  }
}
```

---

## Status Values in Data

The dashboard works with these exact status values:
- **Backlog** - vulnerabilities not yet started
- **Concluído** - completed vulnerabilities
- **Em Progresso** - vulnerabilities in progress (if any)

---

## Priority/Classification Values

The dashboard filters by:
- **P1** - Critical
- **P2** - High
- **P3** - Medium
- **P4** - Low

---

## Responsible Parties

The dashboard dynamically populates the "Responsável" filter with:
- Beatriz De Matos Campos
- Fabiano Vieira De Souza
- Felipe Dos Santos Ramas
- Gabriel Angelo Oberstein Branco

---

## Troubleshooting

### Error: "credentials.json not found"
**Solution:** Download OAuth credentials from Google Cloud Console and save as `credentials.json`

### Error: "googleapis not found"
**Solution:** Install dependencies:
```bash
npm install googleapis google-auth-library
# OR
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Error: "Authentication failed"
**Solution:** Delete `.credentials.json` and try again (will prompt for re-authentication)

### Dashboard shows "Loading..." forever
**Solution:** Check browser console (F12) for errors, ensure `data.json` exists

### Filters not working
**Solution:** 
1. Clear browser cache (Ctrl+Shift+Del or Cmd+Shift+Delete)
2. Ensure `data.json` has correct status values: "Backlog" or "Concluído"
3. Check console for error messages

---

## Dashboard Files

- **index_v2.html** - Main dashboard (use this one)
- **data.json** - Vulnerability data (generated by this process)
- **fetch_and_process_real_data.js** - Node.js script to fetch and process data
- **load_pagina1_all_data.py** - Python script to fetch and process data
- **setup_and_fetch_data.sh** - Automated setup script

---

## Next Steps

1. Run one of the data fetch scripts above
2. Verify `data.json` is created with 6,348 records
3. Open `index_v2.html` in a browser
4. Test filters to confirm they work with real data
5. Export CSV to verify data integrity

---

## Is MCP Being Used?

**Answer:** Yes! This setup uses the Google Sheets API (which is what MCP provides) to directly fetch authenticated data from your Página1 sheet. The scripts handle:
- OAuth authentication
- Direct sheet data fetching (all 6,348 rows)
- Data transformation and formatting
- Automatic statistics calculation
- Real-time filter generation

The dashboard (`index_v2.html`) then loads this data and provides interactive filtering without needing to query the sheet repeatedly.

