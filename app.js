async function loadState() {
  const state = await fetch("data/state.json?cache=" + Date.now()).then(r => r.json());
  renderLeaderboard(state.leaderboard || []);
  renderMatches(state.matches || []);
  renderEvents(state.events || []);
  renderInsights(state.insights || {}, state.last_updated);
}

function renderLeaderboard(rows) {
  const el = document.getElementById("leaderboard");
  el.innerHTML = rows.map(row => `
    <div class="leader-row">
      <div class="rank">${row.rank}</div>
      <div>
        <strong>${row.name}</strong>
        <small>${(row.teams || []).join(" · ")}</small>
      </div>
      <div class="points">${row.points}</div>
    </div>
  `).join("") || "<p>No players yet. Edit data/players.json.</p>";
}

function renderMatches(matches) {
  const el = document.getElementById("matches");
  el.innerHTML = matches.slice(-8).reverse().map(m => `
    <div class="match-row">
      <strong>${m.team1}</strong> ${m.score1}-${m.score2} <strong>${m.team2}</strong>
      <small>${m.status || ""} ${m.stage ? "· " + m.stage : ""}</small>
    </div>
  `).join("") || "<p>No finished matches loaded yet.</p>";
}

function renderEvents(events) {
  const el = document.getElementById("events");
  el.innerHTML = events.slice(-12).reverse().map(e => `<div class="event">${e.text}</div>`).join("") || "<p>No events yet.</p>";
}

function renderInsights(insights, lastUpdated) {
  const el = document.getElementById("insights");
  el.innerHTML = `
    <p><strong>Leader:</strong> ${insights.leader || "TBC"}</p>
    <p><strong>Wooden spoon:</strong> ${insights.wooden_spoon || "TBC"}</p>
    <p><strong>Top scoring teams:</strong> ${(insights.top_scoring_teams || []).join(", ") || "TBC"}</p>
    <p><strong>Last updated:</strong> ${lastUpdated ? new Date(lastUpdated).toLocaleString() : "Never"}</p>
  `;
}

loadState();
setInterval(loadState, 300000);
