async function refreshStats() {
  try {
    const res = await fetch("/api/stats", { headers: { "Accept": "application/json" } });
    if (res.status === 401) {
      console.warn("Dashboard API: not authenticated.");
      return;
    }
    if (!res.ok) throw new Error("HTTP " + res.status);
    const d = await res.json();
    const map = {
      "stat-models": d.models, "stat-versions": d.versions,
      "stat-experiments": d.experiments, "stat-deployments": d.deployments,
      "stat-datasets": d.datasets, "stat-alerts": d.open_alerts,
      "stat-incidents": d.open_incidents, "stat-recent": d.recent_deployments,
      "stat-time": d.server_time,
    };
    for (const id in map) {
      const el = document.getElementById(id);
      if (el) el.textContent = map[id];
    }
  } catch (err) {
    console.error("Dashboard refresh failed:", err);
  }
}
document.addEventListener("DOMContentLoaded", () => {
  refreshStats();
  setInterval(refreshStats, 10000);
});