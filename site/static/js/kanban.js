document.addEventListener("DOMContentLoaded", () => {
    carregarLeads();
});

function carregarLeads() {
    fetch("/api/leads")
        .then(response => response.json())
        .then(leads => {
            limparColunas();
            leads.forEach(renderLead);
        })
        .catch(error => console.error("Erro ao carregar leads:", error));
}

function limparColunas() {
    document.getElementById("novo").innerHTML = "";
    document.getElementById("contato").innerHTML = "";
    document.getElementById("fechado").innerHTML = "";
}

function renderLead(lead) {
    const card = document.createElement("div");
    card.style.border = "1px solid #ccc";
    card.style.padding = "8px";
    card.style.marginBottom = "8px";
    card.style.borderRadius = "4px";

    card.innerHTML = `
        <strong>${lead.nome}</strong><br>
        <small>${lead.email || ""}</small><br>
        <small>${lead.telefone || ""}</small>
    `;

    if (lead.status === "novo") {
        document.getElementById("novo").appendChild(card);
    } 
    else if (lead.status === "contato") {
        document.getElementById("contato").appendChild(card);
    } 
    else if (lead.status === "fechado") {
        document.getElementById("fechado").appendChild(card);
    }
}
