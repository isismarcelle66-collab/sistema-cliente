document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/leads")
    .then(res => res.json())
    .then(leads => {
      leads.forEach(lead => {
        criarCard(lead);
      });
    });

  function criarCard(lead) {
    const card = document.createElement("div");
    card.classList.add("card");
    card.draggable = true;
    card.dataset.id = lead.id;

    card.innerHTML = `
      <strong>${lead.nome}</strong><br>
      ${lead.email}
    `;

    card.addEventListener("dragstart", dragStart);

    const coluna = document.getElementById(lead.status);
    if (coluna) coluna.appendChild(card);
  }

  function dragStart(e) {
    e.dataTransfer.setData("id", e.target.dataset.id);
  }

  document.querySelectorAll(".coluna").forEach(coluna => {
    coluna.addEventListener("dragover", e => e.preventDefault());

    coluna.addEventListener("drop", function (e) {
      e.preventDefault();

      const id = e.dataTransfer.getData("id");
      const card = document.querySelector(`[data-id='${id}']`);

      this.appendChild(card);

      fetch(`/api/leads/${id}?status=${this.id}`, {
        method: "PUT"
      });
    });
  });
});