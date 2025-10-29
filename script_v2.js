// Link to new CSV file in the repo
const csvUrl = "https://raw.githubusercontent.com/rawankhalife/webscraping-automation/main/bitcoin_hourly_data_v2.csv";

async function fetchCsvData() {
  try {
    const response = await fetch(csvUrl);
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }

    const csvText = await response.text();
    const rows = csvText.trim().split("\n").map(row => row.split(","));
    createTable(rows);

  } catch (error) {
    console.error("Error fetching CSV data:", error);
    document.getElementById("data-container").innerHTML = "<p>Failed to load data.</p>";
  }
}

function createTable(rows) {
  const container = document.getElementById("data-container");
  const table = document.createElement("table");
  const header = document.createElement("tr");

  rows[0].forEach(col => {
    const th = document.createElement("th");
    th.textContent = col;
    header.appendChild(th);
  });
  table.appendChild(header);

  rows.slice(1).forEach(row => {
    const tr = document.createElement("tr");
    row.forEach(cell => {
      const td = document.createElement("td");
      td.textContent = cell;
      tr.appendChild(td);
    });
    table.appendChild(tr);
  });

  container.appendChild(table);
}

fetchCsvData();
