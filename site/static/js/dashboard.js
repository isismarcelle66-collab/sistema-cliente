fetch("/api/metricas")
    .then(res => res.json())
    .then(data => {

        document.getElementById("total").innerText = data.total;
        document.getElementById("novo").innerText = data.novo;
        document.getElementById("contato").innerText = data.contato;
        document.getElementById("fechado").innerText = data.fechado;

        const ctx = document.getElementById("grafico");

        new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Novo", "Contato", "Fechado"],
                datasets: [{
                    label: "Leads",
                    data: [data.novo, data.contato, data.fechado],
                }]
            }
        });
    });
s