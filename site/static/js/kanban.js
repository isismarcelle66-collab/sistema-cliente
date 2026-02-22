document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/leads")
    .then(response => response.json())
    .then(leads => {
      leads.forEach(lead => {
        const card = document.createElement("div");
        card.style.border = "1px solid #ccc";
        card.style.padding = "8px";
        card.style.margin = "5px";
        card.style.backgroundColor = "#f9f9f9";

        card.innerHTML = `
          <strong>${lead.nome}</strong><br>
          ${lead.email}<br>
          ${lead.telefone}
        `;

        const coluna = document.getElementById(lead.status);
        if (coluna) {
          coluna.appendChild(card);
        }
      });
    })
    .catch(error => {
      console.error("Erro ao carregar leads:", error);
    });
});