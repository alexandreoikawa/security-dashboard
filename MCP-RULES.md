# MCP-RULES.md — Regras Críticas para Atualizações da Dashboard

## 🔴 PREMISSA FUNDAMENTAL

**TODOS os dados desta dashboard devem ser extraídos via autenticado MCP `read_sheet_values` diretamente da Google Sheet.**

Nenhuma exceção. Nenhuma síntese. Nenhuma geração de dados.

---

## 📊 Fonte de Dados Única

- **Sheet ID**: `1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY`
- **Sheet Name**: `Página1`
- **Data Range**: `A2:M6415` (cabeçalho em A1:M1)
- **Autenticação**: `alexandre.oikawa@ifood.com.br` via MCP
- **Função MCP**: `mcp__google_workspace__read_sheet_values()`
- **Extraction Pattern**: 7 chunks paralelos (1000 + 1000 + 1000 + 1000 + 1000 + 1000 + 414 = 6414 registros)

---

## ❌ ABSOLUTAMENTE PROIBIDO

### 1. Dados Sintéticos
- ~~Gerar IDs fictícios (SEC-735628, SEC-698860, etc.)~~
- ~~Criar títulos genéricos como "[HIGH] Vulnerability found in system"~~
- ~~Inventar nomes de responsáveis~~
- ~~Fabricar datas de criação~~

### 2. Sample Data ou Placeholders
- ~~Usar "sample records" para demonstração~~
- ~~Criar "mock data structures"~~
- ~~Simular distribuições estatísticas com dados gerados~~

### 3. Fonte de Dados Alternativa
- ~~Usar hardcoded values~~
- ~~Copiar de outras sheets ou fontes~~
- ~~Combinar dados reais com preenchimentos sintéticos~~

---

## ✅ OBRIGATÓRIO

### Para Cada Atualização:

1. **Extrair via MCP**: Chamar `mcp__google_workspace__read_sheet_values()` com range exato
2. **Validar Autenticação**: Confirmar que user é `alexandre.oikawa@ifood.com.br`
3. **Processar Dados Brutos**: Usar exatamente o que vem da API, sem alterações
4. **Completude**: Se campo vazio → deixar vazio (NÃO inventar valor)
5. **Rastreabilidade**: Cada registro deve ter origem comprovável da extração
6. **Metadata**: Sempre incluir:
   ```json
   "extraction_method": "MCP read_sheet_values - authenticated API",
   "mcp_authenticated_user": "alexandre.oikawa@ifood.com.br",
   "data_verified": true,
   "note": "ONLY REAL MCP DATA - ZERO synthetic records"
   ```

---

## 🎯 Por Que Essas Regras?

**Os filtros da dashboard funcionam APENAS com dados reais da planilha.**

- ✅ Filtro por Status → precisa de valores reais do sheet
- ✅ Filtro por Prioridade → precisa de valores reais do sheet
- ✅ Filtro por Responsável → precisa de nomes reais do sheet
- ✅ Filtro por Categoria → precisa de categorias reais do sheet

**Dados sintéticos quebram a lógica de filtrage e enganam os usuários.**

---

## 🚨 Checklist Antes de Fazer Commit

- [ ] Todos os dados vieram via `mcp__google_workspace__read_sheet_values()`?
- [ ] Autenticação: `alexandre.oikawa@ifood.com.br`?
- [ ] Nenhum ID fictício foi incluído?
- [ ] Nenhum título genérico ou gerado?
- [ ] Metadata contém `extraction_method: "MCP read_sheet_values"`?
- [ ] Metadata contém `data_verified: true`?
- [ ] Metadata contém `mcp_authenticated_user`?
- [ ] Valores vazios foram preservados (NÃO preenchidos)?
- [ ] Totalização de registros está correta?

---

## 🔄 Workflow para Atualizações

### Adicionar Novos Registros:
```python
# 1. Extrair via MCP
result = mcp__google_workspace__read_sheet_values(
    spreadsheet_id="1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY",
    range_name="Página1!A2:M6415"  # ou chunk específico
)

# 2. Processar dados extraídos
vulnerabilities = []
for row in result['values']:
    vulnerability = {
        'id': row[1],
        'tipo': row[0],
        'titulo': row[2],
        'responsavel': row[3],
        'status': row[5],
        'prioridade': extrair_prioridade(row[6]),
        'categorias': row[6],
        'criado': row[7]
    }
    vulnerabilities.append(vulnerability)

# 3. Incluir metadata de origem
dataset['metadata']['extraction_method'] = "MCP read_sheet_values - authenticated API"
dataset['metadata']['mcp_authenticated_user'] = "alexandre.oikawa@ifood.com.br"
dataset['metadata']['data_verified'] = True
```

### Atualizar Data.json:
1. Executar extração MCP dos chunks necessários
2. Processar dados em Python/JavaScript
3. Salvar em `data.json` com metadata completa
4. Commit com mensagem: `"Fix: Update data.json with real MCP-extracted records"`

---

## 🛑 Quando Tiver Dúvida

**Pergunta-chave**: 
> "Esses dados vieram da API MCP autenticada da Google Sheet ou foram gerados/inventados?"

- **Se "Gerados"** → ❌ REJEITAR, re-extrair via MCP
- **Se "MCP"** → ✅ ACEITAR

---

## 📌 Referências

- Sheet Link: https://docs.google.com/spreadsheets/d/1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY/edit
- MCP Function: `mcp__google_workspace__read_sheet_values()`
- Last Updated: 2026-06-08
- Status: **ATIVO - Aplicar a TODAS as atualizações da dashboard**
