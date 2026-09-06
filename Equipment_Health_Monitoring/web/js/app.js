/**
 * Multi-Sensor Fusion Control Center - Simplicity-First ES6 Controller.
 * Direct 3-Step Flow: INPUT -> PROCESS -> OUTPUT
 */

document.addEventListener("DOMContentLoaded", () => {
    initControls();
    fetchAnalysis();
});

function initControls() {
    const btnAnalyze = document.getElementById("btnAnalyze");
    if (btnAnalyze) {
        btnAnalyze.addEventListener("click", runAnalysis);
    }

    const presets = document.querySelectorAll(".btn-preset");
    presets.forEach(btn => {
        btn.addEventListener("click", async () => {
            const mode = btn.getAttribute("data-mode");
            try {
                const res = await fetch(`/api/preset?mode=${mode}`);
                const data = await res.json();
                populateInputs(data.inputs);
                renderOutputs(data);
            } catch (err) {
                console.error("Preset load error:", err);
            }
        });
    });
}

function populateInputs(inputs) {
    if (!inputs) return;
    for (const [key, val] of Object.entries(inputs)) {
        const el = document.getElementById(`in_${key}`);
        if (el) {
            el.value = parseFloat(val).toFixed(1);
        }
    }
}

function getFormInputs() {
    return {
        temperature: parseFloat(document.getElementById("in_temperature").value || 42.5),
        vibration: parseFloat(document.getElementById("in_vibration").value || 1.8),
        pressure: parseFloat(document.getElementById("in_pressure").value || 4.1),
        humidity: parseFloat(document.getElementById("in_humidity").value || 45.0),
        current: parseFloat(document.getElementById("in_current").value || 12.4),
        voltage: parseFloat(document.getElementById("in_voltage").value || 401.2),
        rpm: parseFloat(document.getElementById("in_rpm").value || 1480.0)
    };
}

async function runAnalysis() {
    const inputs = getFormInputs();
    try {
        const res = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(inputs)
        });
        const data = await res.json();
        renderOutputs(data);
    } catch (err) {
        console.error("Analysis execution error:", err);
    }
}

async function fetchAnalysis() {
    try {
        const res = await fetch("/api/status");
        const data = await res.json();
        if (data.inputs) {
            populateInputs(data.inputs);
        } else if (data.telemetry) {
            populateInputs(data.telemetry);
        }
        renderOutputs(data);
    } catch (err) {
        console.error("Initial fetch error:", err);
    }
}

function renderOutputs(data) {
    if (!data) return;

    // SECTION 2: PROCESS MATRIX
    const tbody = document.getElementById("processTbody");
    if (tbody && data.inputs) {
        let html = "";
        for (const [key, val] of Object.entries(data.inputs)) {
            const risk = data.normalized_risks ? (data.normalized_risks[key] || 0.0) : 0.0;
            const weight = data.weights ? (data.weights[key] || 0.1) : 0.1;
            const contrib = data.contributions ? (data.contributions[key] || 0.0) : 0.0;

            html += `
                <tr>
                    <td style="font-weight: 600;">${key.toUpperCase()}</td>
                    <td class="mono">${val.toFixed(1)}</td>
                    <td class="mono">${risk.toFixed(3)}</td>
                    <td class="mono">${weight.toFixed(2)}</td>
                    <td class="mono">${contrib.toFixed(1)}%</td>
                </tr>
            `;
        }
        tbody.innerHTML = html;
    }

    // SECTION 3: OUTPUT
    // 1. Equipment Health Score
    const score = data.health_score !== undefined ? data.health_score : 95.0;
    document.getElementById("outScore").textContent = `${score.toFixed(1)} / 100`;

    // 2. Equipment Status
    const status = data.health_status || "Healthy";
    const statusEl = document.getElementById("outStatus");
    statusEl.textContent = status.toUpperCase();
    statusEl.className = `status-badge ${getBadgeClass(status)}`;

    // 3. Main Problem Detected
    document.getElementById("outProblem").textContent = data.main_problem || "None (All parameters nominal)";

    // 4. Affected Sensors
    document.getElementById("outAffected").textContent = data.affected_sensors || "None";

    // 5. Maintenance Recommendation
    document.getElementById("outRecommendation").textContent = data.recommendation || "No immediate maintenance required.";
    document.getElementById("outReason").textContent = data.reason || "All parameters operating within nominal safe bounds.";
    document.getElementById("outTimeframe").textContent = data.timeframe || "Routine cycle";
    document.getElementById("outPriority").textContent = data.priority || "LOW";
    document.getElementById("outPriority").style.color = getStatusColor(status);
}

function getBadgeClass(status) {
    switch (status ? status.toUpperCase() : "") {
        case "HEALTHY": return "badge-healthy";
        case "NORMAL": return "badge-normal";
        case "WARNING": return "badge-warning";
        case "CRITICAL": return "badge-critical";
        default: return "badge-normal";
    }
}

function getStatusColor(status) {
    switch (status ? status.toUpperCase() : "") {
        case "HEALTHY": return "#059669";
        case "NORMAL": return "#2563EB";
        case "WARNING": return "#D97706";
        case "CRITICAL": return "#DC2626";
        default: return "#64748B";
    }
}
