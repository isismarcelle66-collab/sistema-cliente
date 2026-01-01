document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // FORMULÁRIO AJAX (LEADS)
    // =========================
    const form = document.getElementById("leadForm");
    const resultado = document.getElementById("formResultado");

    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            resultado.innerHTML = "";
            resultado.className = "";

            const formData = new FormData(form);

            try {
                const response = await fetch("/lead", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) throw new Error(`Erro na requisição: ${response.status}`);
                resultado.className = "success";
                resultado.innerHTML = "Lead enviado com sucesso!";
                form.reset();
            } catch (error) {
                resultado.className = "error";
                resultado.innerHTML = `Ocorreu um erro: ${error.message}`;
            }
        });
    }

    // =========================
    // DASHBOARD METRICS E GRÁFICOS
    // =========================
    let chartTotais, chartPorDia;

    async function carregarMetricasTotais() {
        try {
            const response = await fetch('/api/metricas');
            const data = await response.json();
            const chartData = [data.clientes_unicos, data.clientes_recompra, data.total_pedidos];

            if (chartTotais) {
                chartTotais.data.datasets[0].data = chartData;
                chartTotais.update();
            } else {
                const ctx = document.getElementById('clientesChart');
                if (!ctx) return;
                chartTotais = new Chart(ctx.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: ['Clientes Únicos', 'Clientes Recompra', 'Total de Pedidos'],
                        datasets: [{
                            label: 'Quantidade',
                            data: chartData,
                            backgroundColor: [
                                'rgba(75, 192, 192, 0.6)',
                                'rgba(153, 102, 255, 0.6)',
                                'rgba(255, 159, 64, 0.6)'
                            ],
                            borderColor: [
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: { responsive: true, scales: { y: { beginAtZero: true, precision: 0 } } }
                });
            }
        } catch (err) {
            console.error("Erro ao carregar métricas:", err);
        }
    }

    async function carregarMetricasPorDia() {
        try {
            const response = await fetch('/api/clientes_por_dia');
            const data = await response.json();
            const dias = data.dias;
            const contagens = data.contagens;

            if (chartPorDia) {
                chartPorDia.data.labels = dias;
                chartPorDia.data.datasets[0].data = contagens;
                chartPorDia.update();
            } else {
                const ctx = document.getElementById('clientesDiaChart');
                if (!ctx) return;
                chartPorDia = new Chart(ctx.getContext('2d'), {
                    type: 'line',
                    data: {
                        labels: dias,
                        datasets: [{
                            label: 'Clientes por Dia',
                            data: contagens,
                            fill: false,
                            borderColor: 'rgba(54, 162, 235, 1)',
                            backgroundColor: 'rgba(54, 162, 235, 0.4)',
                            tension: 0.1
                        }]
                    },
                    options: { responsive: true, scales: { y: { beginAtZero: true, precision: 0 } } }
                });
            }
        } catch (err) {
            console.error("Erro ao carregar métricas por dia:", err);
        }
    }

    // Primeira chamada e atualização a cada 5 segundos
    carregarMetricasTotais();
    carregarMetricasPorDia();
    setInterval(() => {
        carregarMetricasTotais();
        carregarMetricasPorDia();
    }, 5000);
});
