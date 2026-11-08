const $ = (id) => document.getElementById(id);
const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
}[char]));

function render(result) {
  const findings = result.findings || [];
  $("total").textContent = findings.length;
  $("high").textContent = findings.filter((item) => ["High", "Critical"].includes(item.severity)).length;
  $("pages").textContent = (result.pages || []).length;
  $("state").textContent = "DONE";
  $("targetLabel").textContent = result.target;
  $("findings").innerHTML = findings.length ? findings.map((item) =>
    "<tr><td><span class='sev " + esc(item.severity) + "'>" + esc(item.severity) +
    "</span></td><td><b>" + esc(item.title) + "</b></td><td>" + esc(item.category) +
    "</td><td>" + esc(item.url) + "<br>" + esc(item.evidence) + "</td><td>" +
    esc(item.remediation) + "</td></tr>"
  ).join("") : "<tr><td colspan='5'>No findings from the enabled checks.</td></tr>";
  $("message").textContent = "Assessment complete. Manually validate findings before remediation.";
}

async function history() {
  try {
    const response = await fetch("/api/history");
    const items = await response.json();
    $("history").innerHTML = items.length ? items.map((item) =>
      "<div>" + esc(item.started_at) + " · <b>" + esc(item.target) + "</b> · " +
      (item.findings || []).length + " findings</div>"
    ).join("") : "No previous scans.";
  } catch (_) {}
}

$("scan").onclick = async () => {
  if (!$("auth").checked) {
    $("message").textContent = "Confirm ownership or explicit authorization first.";
    return;
  }
  if (!$("target").value.trim()) return;
  $("scan").disabled = true;
  $("state").textContent = "RUNNING";
  $("message").textContent = "Running bounded checks…";
  try {
    const response = await fetch("/api/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target: $("target").value, authorized: true })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Scan failed");
    render(data);
    history();
  } catch (error) {
    $("state").textContent = "ERROR";
    $("message").textContent = error.message;
  } finally {
    $("scan").disabled = false;
  }
};
history();
