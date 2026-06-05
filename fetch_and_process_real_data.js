#!/usr/bin/env node
/**
 * Fetch real vulnerability data from Página1 sheet and generate data.json
 * Uses Google Sheets API with OAuth
 */

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');
const readline = require('readline');

const SPREADSHEET_ID = '1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY';
const SHEET_NAME = 'Página1';
const RANGE = `${SHEET_NAME}!A1:N6349`;

// Token cache file
const TOKEN_PATH = path.join(process.cwd(), '.credentials.json');
const CREDENTIALS_PATH = path.join(process.cwd(), 'credentials.json');

async function authorize() {
  let client;

  if (fs.existsSync(CREDENTIALS_PATH)) {
    const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
    const { client_id, client_secret, redirect_uris } = credentials.installed || credentials.web;

    client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

    // Check if we have a token
    if (fs.existsSync(TOKEN_PATH)) {
      const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
      client.setCredentials(token);
      return client;
    }

    // Request new token
    console.error('⚠️  Needs authentication. Please follow the instructions...');
    const authUrl = client.generateAuthUrl({
      access_type: 'offline',
      scope: ['https://www.googleapis.com/auth/spreadsheets.readonly'],
    });

    console.error(`📋 Open this URL in your browser:\n${authUrl}\n`);

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stderr,
    });

    return new Promise((resolve) => {
      rl.question('Enter the authorization code: ', (code) => {
        rl.close();

        client.getToken(code, (err, token) => {
          if (err) {
            console.error('❌ Error retrieving token:', err);
            process.exit(1);
          }

          client.setCredentials(token);
          fs.writeFileSync(TOKEN_PATH, JSON.stringify(token));
          resolve(client);
        });
      });
    });
  } else {
    console.error('❌ credentials.json not found');
    console.error('   Get it from: https://developers.google.com/sheets/api/quickstart/nodejs');
    process.exit(1);
  }
}

async function fetchSheetData(auth) {
  console.error('📥 Fetching data from Página1...');

  const sheets = google.sheets({ version: 'v4', auth });

  const response = await sheets.spreadsheets.values.get({
    spreadsheetId: SPREADSHEET_ID,
    range: RANGE,
  });

  const rows = response.data.values || [];
  console.error(`✅ Fetched ${rows.length} rows`);
  return rows;
}

function parseVulnerability(row, index) {
  if (row.length < 14) return null;

  try {
    const vuln = {
      tipo: (row[0] || '').trim(),
      chave: (row[1] || '').trim(),
      resumo: (row[2] || '').trim(),
      responsavel: (row[3] || '').trim(),
      prioridade: (row[4] || '').trim(),
      status: (row[5] || '').trim(),
      categorias: (row[6] || '').trim(),
      criado: (row[7] || '').trim(),
      customfield: (row[8] || '').trim(),
      resolvido: (row[9] || '').trim(),
      the_silence: (row[10] || '').trim(),
      sistema: (row[11] || '').trim(),
      classificacao: (row[12] || 'P3').trim(),
      dias_abertos: parseInt(row[13] || '0') || 0,
    };

    // Skip if no chave
    if (!vuln.chave) return null;

    return vuln;
  } catch (e) {
    console.error(`⚠️  Error parsing row ${index}:`, e.message);
    return null;
  }
}

function generateDataset(rawRows) {
  console.error('📊 Processing data...');

  // Skip header row
  const vulnerabilities = [];
  for (let i = 1; i < rawRows.length; i++) {
    const vuln = parseVulnerability(rawRows[i], i);
    if (vuln) {
      vulnerabilities.push(vuln);
    }
  }

  if (vulnerabilities.length === 0) {
    throw new Error('No vulnerabilities parsed');
  }

  // Calculate statistics
  const total = vulnerabilities.length;
  const backlog = vulnerabilities.filter(v => v.status === 'Backlog').length;
  const concluido = vulnerabilities.filter(v => v.status === 'Concluído').length;
  const em_progresso = vulnerabilities.filter(v => v.status === 'Em Progresso').length;

  const p1 = vulnerabilities.filter(v => v.classificacao === 'P1').length;
  const p2 = vulnerabilities.filter(v => v.classificacao === 'P2').length;
  const p3 = vulnerabilities.filter(v => v.classificacao === 'P3').length;
  const p4 = vulnerabilities.filter(v => v.classificacao === 'P4').length;

  // Get unique responsible parties
  const responsiblesSet = new Set();
  vulnerabilities.forEach(v => {
    if (v.responsavel) responsiblesSet.add(v.responsavel);
  });
  const responsibles = Array.from(responsiblesSet).sort();

  // Get unique categories
  const categoriesSet = new Set();
  vulnerabilities.forEach(v => {
    if (v.categorias) {
      v.categorias.split(';').forEach(cat => {
        const trimmed = cat.trim();
        if (trimmed) categoriesSet.add(trimmed);
      });
    }
  });
  const categories = Array.from(categoriesSet).sort();

  // Build dataset
  const dataset = {
    vulnerabilities,
    summary: {
      total,
      backlog,
      concluido,
      em_progresso,
      p1,
      p2,
      p3,
      p4,
    },
    filters: {
      responsibles,
      categories,
    },
    metadata: {
      updated_at: new Date().toISOString(),
      sheet_id: SPREADSHEET_ID,
      sheet_name: SHEET_NAME,
      source: 'Google Sheets - Página1 (Real Data via API)',
      total_rows_loaded: total,
    },
  };

  return dataset;
}

async function main() {
  try {
    const auth = await authorize();
    const rawRows = await fetchSheetData(auth);
    const dataset = generateDataset(rawRows);

    // Save to file
    fs.writeFileSync('data.json', JSON.stringify(dataset, null, 2));

    // Print summary
    console.error('✅ data.json generated successfully!');
    console.error(`   📊 Total: ${dataset.summary.total.toLocaleString()}`);
    console.error(`   📁 Backlog: ${dataset.summary.backlog.toLocaleString()}`);
    console.error(`   ✓ Concluído: ${dataset.summary.concluido.toLocaleString()}`);
    console.error(`   ⏳ Em Progresso: ${dataset.summary.em_progresso.toLocaleString()}`);
    console.error(`   🔴 P1: ${dataset.summary.p1.toLocaleString()}`);
    console.error(`   🟡 P2: ${dataset.summary.p2.toLocaleString()}`);
    console.error(`   🟠 P3: ${dataset.summary.p3.toLocaleString()}`);
    console.error(`   🟢 P4: ${dataset.summary.p4.toLocaleString()}`);
    console.error(`   👥 Responsibles: ${dataset.filters.responsibles.length}`);
    console.error(`   🏷️  Categories: ${dataset.filters.categories.length}`);
  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

main();
