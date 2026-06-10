
const fs = require('fs');
const { google } = require('googleapis');
const { auth } = require('google-auth-library');

const SHEET_ID = '1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY';

async function getAuthClient() {
  try {
    const authClient = await auth.getClient({
      scopes: ['https://www.googleapis.com/auth/spreadsheets.readonly']
    });
    return authClient;
  } catch (err) {
    console.error('Auth failed:', err.message);
    return null;
  }
}

async function fetchChunk(authClient, range) {
  try {
    const sheets = google.sheets({ version: 'v4', auth: authClient });
    const response = await sheets.spreadsheets.values.get({
      spreadsheetId: SHEET_ID,
      range: range,
    });
    return response.data.values || [];
  } catch (err) {
    console.error(`Error fetching ${range}:`, err.message);
    return [];
  }
}

async function main() {
  const authClient = await getAuthClient();
  if (!authClient) {
    console.error('Failed to authenticate');
    process.exit(1);
  }

  const allRecords = [];
  const ranges = [
    'Página1!A2:M101',
    'Página1!A102:M201',
    'Página1!A202:M301',
    'Página1!A302:M401',
    'Página1!A402:M501',
    'Página1!A502:M601',
    'Página1!A602:M701',
    'Página1!A702:M801',
    'Página1!A802:M901',
    'Página1!A902:M1001',
  ];

  for (const range of ranges) {
    console.log(`Fetching ${range}...`);
    const rows = await fetchChunk(authClient, range);
    allRecords.push(...rows);
    console.log(`  Got ${rows.length} rows`);
  }

  console.log(`\nTotal real records: ${allRecords.length}`);
  fs.writeFileSync('all_1000_real_records.json', JSON.stringify(allRecords, null, 2));
}

main();
