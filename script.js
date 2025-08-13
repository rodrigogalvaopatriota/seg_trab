// Usuários permitidos
const USERS = {
    "admin": "1234",
    "usuario": "senha123"
};

// Login
function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (USERS[username] && USERS[username] === password) {
        localStorage.setItem("user", username);
        window.location.href = "dashboard.html";
    } else {
        document.getElementById("error").innerText = "Usuário ou senha inválidos.";
    }
}

// Logout
function logout() {
    localStorage.removeItem("user");
    window.location.href = "index.html";
}

// Proteger dashboard
if (window.location.pathname.includes("dashboard.html")) {
    const user = localStorage.getItem("user");
    if (!user) {
        window.location.href = "index.html";
    } else {
        fetch("data.csv")
            .then(response => response.text())
            .then(data => {
                const rows = data.split("\n").slice(1); // Ignora header
                const counts = {};

                rows.forEach(row => {
                    const cols = row.split(",");
                    const dia = cols[0]; // Supondo coluna dia na posição 0
                    const name = cols[1]; // Supondo first_name_telegram na posição 1
                    if (!counts[dia]) counts[dia] = 0;
                    counts[dia]++;
                });

                const labels = Object.keys(counts).sort();
                const values = labels.map(d => counts[d]);

                const ctx = document.getElementById('myChart').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Quantidade de usuários por dia',
                            data: values,
                            borderColor: 'blue',
                            fill: false
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            x: { title: { display: true, text: 'Dia' } },
                            y: { title: { display: true, text: 'Quantidade' } }
                        }
                    }
                });
            });
    }
}
