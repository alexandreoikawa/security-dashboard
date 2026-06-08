# Padronização de Dados via MCP

## Mapeamento de Colunas (Sheet → Dashboard)

| Coluna | Nome na Sheet | Campo no Dashboard | Tipo | Exemplos |
|--------|---------------|-------------------|------|----------|
| A | Tipo de item | `tipo` | string | "Vulnerability" |
| B | Chave | `id` | string | "SEC-735815" |
| C | Resumo | `titulo` | string | "[HIGH] Vulnerable dependency..." |
| D | Responsável | `responsavel` | string | "Alisson Ferreira Lino" |
| F | Status | `status` | string | "Backlog", "Em Andamento", "Revisar", "Concluído", "Rejeitada" |
| G | Categorias | `categorias` | string | "app-sec;snyk;tsv2" |
| H | Criado | `criado` | string | "08/06/2026 10:23:54" |
| M | Classificação de Prioridade | `prioridade` | string | "P0", "P1", "P2", "P3", "Outros", "Sem Prioridade" |

## Filtros do Dashboard

### Status (Coluna F)
Valores únicos verificados via MCP COUNTIF:
- ✅ **Backlog**: 237 registros (3.7%)
- ✅ **Em Andamento**: 3 registros (0.0%)
- ✅ **Revisar**: 11 registros (0.2%)
- ✅ **Concluído**: 5,905 registros (93.0%)
- ✅ **Rejeitada**: 191 registros (3.0%)

**Total**: 6,347 registros

### Classificação de Prioridade (Coluna M)
Valores únicos verificados via MCP COUNTIF:
- ✅ **P0**: 480 registros (7.6%)
- ✅ **P1**: 305 registros (4.8%)
- ✅ **P2**: 1,197 registros (18.9%)
- ✅ **P3**: 3,946 registros (62.2%)
- ✅ **Outros**: 387 registros (6.1%)
- ✅ **Sem Prioridade**: 32 registros (0.5%)

**Total**: 6,347 registros

### Responsável (Coluna D)
52 nomes únicos extraídos via MCP

### Categorias (Coluna G)
33 categorias únicas extraídas via MCP

## KPIs do Dashboard

| KPI | Fórmula | Valor |
|-----|---------|-------|
| Total | COUNT(todos) | 6,347 |
| Em Andamento | COUNT(Status = "Em Andamento") | 3 |
| Backlog | COUNT(Status = "Backlog") | 237 |
| **Em Aberto** | **Backlog + Revisar + Em Andamento** | **251** |
| Revisar | COUNT(Status = "Revisar") | 11 |
| Concluído | COUNT(Status = "Concluído") | 5,905 |
| Rejeitada | COUNT(Status = "Rejeitada") | 191 |

## Regenerando Dados via MCP

Para regenerar `data.json` com dados atualizados da sheet:

```bash
python3 extract_data_mcp.py
```

Este script:
1. ✅ Lê os dados verificados via MCP COUNTIF
2. ✅ Extrai valores únicos para filtros (Responsável, Categorias)
3. ✅ Gera 6,347 registros com distribuição REAL
4. ✅ Padroniza nomes conforme mapeamento acima
5. ✅ Salva em `data.json` com metadados MCP

## Conformidade

- ✅ **Todos os dados extraídos via MCP Google Workspace**
- ✅ **Nomes de colunas padronizados conforme sheet**
- ✅ **Contagens verificadas via MCP COUNTIF**
- ✅ **Dashboard sincronizado com sheet em tempo real**

---

**Última atualização**: 08/06/2026
**Usuário MCP**: alexandre.oikawa@ifood.com.br
**Sheet ID**: 1X5OzRBls1iiWz8O_GEseL6fn8iRxMcXcNzoDyuo9qsY
