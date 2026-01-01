// ==========================
// Variáveis globais
// ==========================
let clientes = [];
let paginaAtual = 1;
const itensPorPagina = 10;

// ==========================
// Função para carregar clientes do servidor
// ==========================
async function carregarClientes() {
    const res = await fetch('/api/export'); // vamos criar endpoint JSON separado se quiser melhor performance
    const text = await res.text();
    // converter CSV em array de objetos
    const linhas = text.trim().split('\n');
    const headers = linhas.shift().split(',');
    clientes = linhas.map(linha => {
        const valores = linha.split(',');
        let obj = {};
        headers.forEach((h, i) => obj[h] = valores[i]);
        return obj;
    });
    renderizarTabela();
}

// ==========================
// Renderizar tabela com paginação
// ==========================
function renderizarTabela() {
    const tbody = document.getElementById('clientesTable');
    tbody.innerHTML = '';

    // Filtros
    const filtroTexto = document.getElementById('buscaClientes').value.toLowerCase();
    const dataInicio = document.getElementById('dataInicio').value;
    const dataFim = document.getElementById('dataFim').value;

    let filtrados = clientes.filter(c => {
        let ok = true;

        // filtro por texto
        if(filtroTexto){
            ok = Object.values(c).some(v => v.toLowerCase().includes(filtroTexto));
        }

        // filtro por datas
        if(ok && dataInicio){
            ok = new Date(c.Data) >= new Date(dataInicio);
        }
        if(ok && dataFim){
            ok = ok && new Date(c.Data) <= new Date(dataFim);
        }

        return ok;
    });

    // paginação
    const totalPaginas = Math.ceil(filtrados.length / itensPorPagina);
    const inicio = (paginaAtual-1) * itensPorPagina;
    const fim = inicio + itensPorPagina;
    const paginaClientes = filtrados.slice(inicio, fim);

    paginaClientes.forEach(c => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${c.Nome}</td>
            <td>${c.Email}</td>
            <td>${c.Telefone}</td>
            <td>${c.Data}</td>
        `;
        tbody.appendChild(tr);
    });

    document.getElementById('pageInfo').innerText = `Página ${paginaAtual} de ${totalPaginas || 1}`;
}

// ==========================
// Eventos
// ==========================
document.getElementById('buscaClientes').addEventListener('input', () => {
    paginaAtual = 1;
    renderizarTabela();
});

document.getElementById('filtrarData').addEventListener('click', () => {
    paginaAtual = 1;
    renderizarTabela();
});

document.getElementById('limparFiltro').addEventListener('click', () => {
    document.getElementById('buscaClientes').value = '';
    document.getElementById('dataInicio').value = '';
    document.getElementById('dataFim').value = '';
    paginaAtual = 1;
    renderizarTabela();
});

document.getElementById('prevPage').addEventListener('click', () => {
    if(paginaAtual > 1) {
        paginaAtual--;
        renderizarTabela();
    }
});

document.getElementById('nextPage').addEventListener('click', () => {
    const totalPaginas = Math.ceil(clientes.length / itensPorPagina);
    if(paginaAtual < totalPaginas) {
        paginaAtual++;
        renderizarTabela();
    }
});

// ==========================
// Inicialização
// ==========================
carregarClientes();
