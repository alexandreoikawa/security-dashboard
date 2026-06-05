# 🔧 Guia de Troubleshooting - Filtro de Status

## O Problema

O filtro de status não está funcionando como esperado.

---

## Como Diagnosticar

### Passo 1: Abra o Console do Navegador

1. Pressione **F12** ou **Ctrl+Shift+I** (Windows/Linux) ou **Cmd+Option+I** (Mac)
2. Vá para a aba **Console**
3. Você deve ver mensagens como:

```
🚀 Inicializando dashboard...
📥 Buscando dados do arquivo data.json...
✅ Dados carregados: 6348 vulnerabilidades
📊 Resumo: {total: 6348, backlog: 3768, resolved: 1316, in_progress: 1264}
🔄 Populando opções de filtros...
✅ Populated responsible filter: 4 items
✅ Populated category filter: 11 items
✓ Event listener configurado para: search-vuln
✓ Event listener configurado para: status-filter
✓ Event listener configurado para: priority-filter
✓ Event listener configurado para: responsible-filter
✓ Event listener configurado para: category-filter
✅ Dashboard carregado com filtros ativos!
```

**Se não vir estas mensagens, o problema é no carregamento inicial.**

---

### Passo 2: Teste o Filtro de Status

1. No dashboard, localize o dropdown **Status**
2. Selecione **"Backlog"**
3. **Observe o Console** - você deve ver:

```
📝 Filtro alterado: status-filter = "Backlog"
🔍 Filter values: {search: "", status: "Backlog", priority: "", responsible: "", category: ""}
   Status comparison: vuln.status="Backlog" vs filter="Backlog" => true
   Status comparison: vuln.status="Backlog" vs filter="Backlog" => true
   Status comparison: vuln.status="Backlog" vs filter="Backlog" => true
✅ Filtro aplicado: 3768/6348 resultados
   Status: "Backlog" = 3768 registros
```

---

## Diagnóstico Rápido

### Se vir: `Filter values: {... status: "" ...}`
- **Problema**: O valor do select não está sendo capturado
- **Solução**: Verifique se o elemento `status-filter` existe no HTML
- **Teste**: No console, digite: `document.getElementById('status-filter')`

### Se vir: `Status comparison: ... => false`
- **Problema**: Os valores não correspondem
- **Solução**: Verifique se há espaços em branco extras
- **Teste**: No console, digite:
  ```javascript
  const el = document.getElementById('status-filter');
  console.log('Valor:', '"' + el.value + '"');
  ```

### Se não vir mensagens de filtro
- **Problema**: O event listener não está registrado
- **Solução**: A página pode não ter carregado completamente
- **Teste**: Aguarde 3 segundos e clique novamente no dropdown

### Se vir: `Filtro aplicado: 0/6348`
- **Problema**: Nenhum registro corresponde ao filtro
- **Solução**: Verifique se o nome do status é exato
- **Teste**: No console, verifique os valores únicos:
  ```javascript
  const statuses = [...new Set(allVulnerabilities.map(v => v.status))];
  console.log('Status únicos:', statuses);
  ```
  **Esperado**: `["Backlog", "Em Progresso", "Resolvido"]`

---

## Checklist de Verificação

- [ ] Dados carregados com sucesso (mensagem ✅ no console)
- [ ] Event listeners registrados (5 event listeners configurados)
- [ ] Select element existe no DOM
- [ ] Valores do select correspondem aos dados:
  - `"Backlog"` = 3,768 registros
  - `"Em Progresso"` = 1,264 registros
  - `"Resolvido"` = 1,316 registros
- [ ] Console mostra log quando seleciona um status
- [ ] Tabela muda quando seleciona um status

---

## Teste Isolado

Se quiser testar o filtro de forma isolada:

1. Abra **test_filter_debug.html** no navegador
2. Clique em **"📊 Mostrar Todos os Status"**
3. Selecione um status no dropdown
4. Clique em **"🔍 Testar Filtro"**
5. Verifique os números exatos

---

## Valores Esperados - Referência

```
Status: "Backlog" = 3,768 registros
Status: "Em Progresso" = 1,264 registros
Status: "Resolvido" = 1,316 registros
Total: 6,348 registros
```

---

## Se Nada Funcionar

### Opção 1: Limpar Cache
- Pressione **Ctrl+Shift+Del** (Windows) ou **Cmd+Shift+Delete** (Mac)
- Selecione "Cached images and files"
- Clique "Clear Now"
- Recarregue a página (**F5** ou **Cmd+R**)

### Opção 2: Testar em Navegador Diferente
- Tente em Firefox, Chrome, Safari
- Cada navegador pode comportar-se diferente

### Opção 3: Verificar Arquivo data.json
```javascript
// No console, digite:
fetch('./data.json').then(r => r.json()).then(d => {
  const statuses = [...new Set(d.vulnerabilities.map(v => v.status))];
  console.log('Status no arquivo:', statuses);
  statuses.forEach(s => {
    const count = d.vulnerabilities.filter(v => v.status === s).length;
    console.log(`  "${s}": ${count}`);
  });
});
```

---

## Relatório para Debug

Se o filtro ainda não funcionar, copie e compartilhe do console:

1. Abra DevTools (F12)
2. Vá para **Console**
3. Selecione um status
4. Copie todas as mensagens de log
5. Procure por mensagens que indicam o problema

**Exemplo de log completo esperado:**
```
🚀 Inicializando dashboard...
✅ Dados carregados: 6348 vulnerabilidades
✓ Event listener configurado para: status-filter
📝 Filtro alterado: status-filter = "Backlog"
🔍 Filter values: {...status: "Backlog"...}
   Status comparison: vuln.status="Backlog" vs filter="Backlog" => true
✅ Filtro aplicado: 3768/6348 resultados
```

---

## Status: 🔍 Investigando

Este guia ajudará a identificar exatamente onde o filtro de status está falhando.
Compartilhe as mensagens do console para diagnóstico mais rápido.
