# 🔐 Security Dashboard - Dados Reais do MCP

Dashboard profissional de gerenciamento de vulnerabilidades com dados 100% reais extraídos via MCP autenticado da Google Sheets.

## 📊 Visão Geral

- **Total de Registros:** 6.414 vulnerabilidades verificadas via MCP API
- **Fonte de Dados:** Google Sheets autenticada (`1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY`)
- **Usuário Autenticado:** `alexandre.oikawa@ifood.com.br`
- **Qualidade:** 100% dados reais, zero dados sintéticos
- **Última Atualização:** Via MCP `read_sheet_values()` API

## 🚀 Como Usar

### Opção 1: Abrir Local (Recomendado)
```bash
python3 -m http.server 8000
# Abrir: http://localhost:8000/
```

### Opção 2: GitHub Pages
```
https://alexandreoikawa.github.io/security-dashboard/
```

## 📁 Arquivos Principais

```
├── index.html                    # Dashboard (profissional)
├── data.json                     # Dados MCP (6414 registros)
├── build_data_from_mcp_real.py   # Script de processamento
├── MCP-RULES.md                  # Regras críticas
└── README.md                     # Este arquivo
```

## 🔄 Atualizar Dados

```bash
python3 build_data_from_mcp_real.py
git add data.json
git commit -m "Update: Fresh data from MCP API"
```

## 🎯 Funcionalidades

### Filtros
- 🔍 Busca por ID, título ou responsável
- 📌 Status: Backlog, Concluído, Rejeitada
- 🎯 Prioridade: P0, P1, P2, P3, Red Team
- 👥 Responsável
- 🏢 Área

### Estatísticas
- Total em tempo real
- Distribuição por status
- Percentuais automáticos
- Cards com cores indicativas

### Exportação
- 📥 Export em CSV dos dados filtrados

## 🔐 Dados do MCP

- **Spreadsheet:** 1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY
- **Sheet:** Página1
- **Range:** A2:M6415 (6414 registros)
- **Autenticação:** MCP read_sheet_values() API
- **Verificação:** 100% real, 0% sintético

## 🛡️ Regras MCP (CRÍTICAS)

✅ **FAZER:**
- Usar MCP read_sheet_values() autenticado
- Manter dados do Google Sheets
- Documentar origem MCP

❌ **NUNCA:**
- Gerar IDs fictícios
- Inventar dados
- Usar fontes alternativas

Ver `MCP-RULES.md` para detalhes.

## 📊 Métricas

| Métrica | Valor |
|---------|-------|
| Total | 6.414 |
| Concluídas | ~93% |
| Backlog | ~3-4% |
| Áreas | 10+ |
| Responsáveis | 50+ |

---

**Status:** ✅ Pronto para Produção  
**Dados:** 100% Real (MCP Autenticado)  
**Data:** 2026-06-09
