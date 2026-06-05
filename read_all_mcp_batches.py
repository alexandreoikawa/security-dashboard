#!/usr/bin/env python3
"""Read all 7 batches from Página1 via MCP API"""

# Este script será executado com as ferramentas do sistema
# que têm acesso ao MCP (mcp__google_workspace__read_sheet_values)

SHEET_ID = "1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY"
SHEET_NAME = "Página1"

batches = [
    {"name": "batch_1", "range": "A1:N1000"},     # header + 999 data
    {"name": "batch_2", "range": "A1001:N2000"},  # 999 data
    {"name": "batch_3", "range": "A2001:N3000"},  # 999 data
    {"name": "batch_4", "range": "A3001:N4000"},  # 999 data
    {"name": "batch_5", "range": "A4001:N5000"},  # 999 data
    {"name": "batch_6", "range": "A5001:N6000"},  # 999 data
    {"name": "batch_7", "range": "A6001:N6349"},  # 349 data
]

print("Para sincronizar dados REAIS:")
print()
print("Preciso executar 7 chamadas MCP em paralelo:")
for batch in batches:
    print(f"  mcp__google_workspace__read_sheet_values(")
    print(f"    spreadsheet_id='{SHEET_ID}',")
    print(f"    range_name='{SHEET_NAME}!{batch['range']}'")
    print(f"  )")
print()
print("Estas chamadas retornarão:")
print("  • Batch 1: 1000 rows (header + 999 data)")
print("  • Batches 2-6: 1000 rows cada")
print("  • Batch 7: 350 rows")
print("  • TOTAL: 6349 rows (header + 6348 data)")
