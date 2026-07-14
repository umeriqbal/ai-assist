import { apiGet } from "./api.js";

async function checkBackendHealth() {
  const statusEl = document.getElementById("backend-status");
  const detailsEl = document.getElementById("health-details");

  try {
    const health = await apiGet("/health");

    statusEl.textContent = "Backend: reachable";
    statusEl.classList.remove("status-pending");
    statusEl.classList.add("status-ok");

    for (const [key, value] of Object.entries(health)) {
      const dt = document.createElement("dt");
      dt.textContent = key;

      const dd = document.createElement("dd");
      dd.textContent = value;

      detailsEl.append(dt, dd);
    }
  } catch (error) {
    statusEl.textContent = "Backend: unreachable";
    statusEl.classList.remove("status-pending");
    statusEl.classList.add("status-error");

    const dt = document.createElement("dt");
    dt.textContent = "error";

    const dd = document.createElement("dd");
    dd.textContent = error.message;

    detailsEl.append(dt, dd);
  }
}

checkBackendHealth();
