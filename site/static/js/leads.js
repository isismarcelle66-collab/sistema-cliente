const API = "http://127.0.0.1:8000/api/leads";

async function carregar() {
  const r = await fetch(API);
  const data = await r.json();
  const lista = document.getElementById("lista");
  lista.innerHTML = "";

  data.forEach(l => {
    lista.innerHTML += `
      <tr>
        <td>${l.nome}</td>
        <td>${l.email}</td>
        <td>${l.telefone}</td>
        <td>${l.status}</td>
      </tr>
    `;
  });
}

document.getElementById("formLead").onsubmit = async e => {
  e.preventDefault();

  await fetch(API, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      nome: nome.value,
      email: email.value,
      telefone: telefone.value
    })
  });

  carregar();
};

carregar();
