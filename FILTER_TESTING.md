# Teste de Filtros - Dashboard de Segurança

## Instruções de Teste

1. Abra `index.html` em um navegador
2. Aguarde o carregamento completo dos dados (verifique o console para mensagens de sucesso)
3. Teste cada filtro conforme os cenários abaixo

---

## Cenários de Teste

### 1️⃣ Teste de Carregamento Inicial
- **Esperado**: 
  - Dashboard carrega com 6,348 vulnerabilidades
  - KPI cards mostram: Total, P1, Backlog, Resolvido
  - Tabela populada com primeiros registros
- **Verifique**:
  - Console mostra: `✅ Dados carregados: 6348 vulnerabilidades`
  - Display mostra: "Mostrando 6,348 de 6,348"

### 2️⃣ Filtro de Busca (Search)
- **Campo**: "🔍 Buscar"
- **Teste**:
  - Digite "SEC-735527" → deve mostrar 1 resultado
  - Digite "P1" → deve mostrar resultados que contêm P1 na chave/resumo
  - Digite "SQL Injection" → deve mostrar vulnerabilidades com SQL Injection
  - Limpe e teste "Backlog" → deve mostrar ocorrências no texto
- **Esperado**: Filtro em tempo real, atualizando enquanto digita

### 3️⃣ Filtro de Status
- **Campo**: "Status"
- **Teste cada opção**:
  - Todos os Status → 6,348 resultados
  - Backlog → 3,768 resultados
  - Em Progresso → 1,264 resultados  
  - Resolvido → 1,316 resultados
- **Esperado**: Contagem precisa em cada seleção

### 4️⃣ Filtro de Prioridade
- **Campo**: "Prioridade"
- **Teste cada opção**:
  - Todas as Prioridades → 6,348 resultados
  - P1 - Crítica → 760 resultados
  - P2 - Alta → 1,642 resultados
  - P3 - Média → 3,153 resultados
  - P4 - Baixa → 793 resultados
- **Esperado**: Contagem precisa e badges coloridas corretas

### 5️⃣ Filtro de Responsável
- **Campo**: "Responsável"
- **Teste cada opção**:
  - Todos os Responsáveis → 6,348 resultados
  - Beatriz De Matos Campos → 1,586 resultados
  - Fabiano Vieira De Souza → 1,604 resultados
  - Felipe Dos Santos Ramas → 1,552 resultados
  - Gabriel Angelo Oberstein Branco → 1,606 resultados
- **Esperado**: Dropdown preenchido dinamicamente com valores reais

### 6️⃣ Filtro de Categoria
- **Campo**: "Categoria"
- **Teste alguns valores**:
  - Todas as Categorias → 6,348 resultados
  - app-sec → múltiplos resultados
  - snyk → múltiplos resultados
  - sca → múltiplos resultados
- **Esperado**: 11 categorias únicas disponíveis
- **Nota**: Popup mostra primeiros 25 caracteres de categorias

### 7️⃣ Filtros Combinados
- **Teste combinações**:
  - Status: Backlog + Prioridade: P1 → 449 resultados esperados
  - Responsável: Fabiano + Status: Resolvido → múltiplos resultados
  - Status: Em Progresso + Prioridade: P2 → múltiplos resultados
  - Busca: "SQL" + Status: Backlog + Prioridade: P1 → resultado refinado
- **Esperado**: Todos os filtros trabalham juntos sem conflitos

### 8️⃣ Botão Limpar Filtros
- **Ação**: Após aplicar alguns filtros, clique "↺ Limpar Filtros"
- **Esperado**:
  - Todos os campos de filtro voltam ao valor vazio
  - Tabela mostra novamente todos os 6,348 registros
  - Display mostra "Mostrando 6,348 de 6,348"

### 9️⃣ Exportar CSV
- **Ação**: 
  - Aplique alguns filtros (ex: Status = Backlog)
  - Clique "📥 Exportar CSV"
- **Esperado**:
  - Download inicia com nome: `vulnerabilities-YYYY-MM-DD.csv`
  - Arquivo contém apenas linhas filtradas (3,768 para Backlog)
  - Headers corretos: Chave, Tipo, Resumo, Status, Prioridade, etc.

### 🔟 Performance
- **Teste**: Aplicar/remover filtros rapidamente
- **Esperado**:
  - Resposta rápida (< 1 segundo)
  - Console mostra tempo de execução (ex: "123.45ms")
  - Nenhum "travamento" da interface

---

## Verificações no Console

Abra o DevTools (F12) e observe o console para:

```
✅ Dados carregados: 6348 vulnerabilidades
📊 Resumo: {total: 6348, backlog: 3768, ...}
🔄 Populando opções de filtros...
✅ Populated responsible filter: 4 items
✅ Populated category filter: 11 items
📝 Filtro alterado: status-filter
✅ Filtros aplicados: 3768/6348 resultados (45.23ms)
```

---

## Valores Esperados - Referência Rápida

| Campo | Total | Backlog | Resolvido | Em Progresso | P1 | P2 | P3 | P4 |
|-------|-------|---------|-----------|--------------|----|----|----|----|
| **Valores** | 6,348 | 3,768 | 1,316 | 1,264 | 760 | 1,642 | 3,153 | 793 |

### Responsáveis
- Beatriz De Matos Campos: 1,586
- Fabiano Vieira De Souza: 1,604
- Felipe Dos Santos Ramas: 1,552
- Gabriel Angelo Oberstein Branco: 1,606

### Categorias (11 total)
- app-sec
- automatic-creation
- devsecops-block-job-2
- layer:tech-corp
- layer:people-tech
- priority:P1, P2, P3, P4
- sca, sast, snyk, snyk_code
- tsv2

---

## Troubleshooting

### Problema: Filtros não respondem
- **Solução**: Abra DevTools (F12), verifique console para erros
- **Verificar**: Se dados foram carregados corretamente

### Problema: Dados vazios
- **Solução**: Verifique se `data.json` existe no mesmo diretório que `index.html`
- **Verificar**: Network tab para ver se data.json foi baixado

### Problema: Números não batem
- **Solução**: Limpe cache do navegador (Ctrl+Shift+Del)
- **Verificar**: Se não há filtros aplicados

### Problema: Exportar CSV não funciona
- **Solução**: Verifique se há registros a exportar
- **Verificar**: Se popups bloqueados estão ativados

---

## Status: ✅ Pronto para Teste

Todos os filtros foram:
- ✓ Corrigidos para corresponder aos dados reais
- ✓ Otimizados para 6,348 registros
- ✓ Testados com lógica de filtro validada
- ✓ Implementados com feedback em tempo real

**Data da última atualização**: 2026-06-05
