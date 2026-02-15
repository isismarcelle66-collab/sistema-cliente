document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("leadForm");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = {
      nome: form.nome.value,
      email: form.email.value,
      whatsapp: form.whatsapp.value
    };

    const response = await fetch("/lead", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      alert("Lead enviado com sucesso!");
      form.reset();
    } else {
      alert("Erro ao enviar");
    }
  });
});
