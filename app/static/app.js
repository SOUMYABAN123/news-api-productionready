function setStatus(id, msg) {
  document.getElementById(id).innerText = msg;
}

async function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  const res = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    setStatus("loginStatus", "Login failed");
    return;
  }

  const data = await res.json();
  localStorage.setItem("token", data.access_token);
  setStatus("loginStatus", "Login successful. Token saved.");
}

function tokenHeader() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: "Bearer " + token } : {};
}

async function fetchClassified() {
  const res = await fetch("/news/classified", { headers: tokenHeader() });

  if (res.status === 403) {
    alert("Token missing/expired. Please login again.");
    return;
  }
  if (res.status === 429) {
    alert("Rate limit exceeded. Wait a minute and retry.");
    return;
  }
  if (!res.ok) {
    alert("Error fetching news");
    return;
  }

  const data = await res.json();
  const el = document.getElementById("results");
  el.innerHTML = "";

  data.items.forEach((item) => {
    const url = item.url ? item.url : "#";
    el.innerHTML += `
      <div class="article">
        <div><a href="${url}" target="_blank">${item.title}</a></div>
        <div class="badge">${item.predicted_category}</div>
      </div>
    `;
  });
}

document.getElementById("btnLogin").addEventListener("click", login);
document.getElementById("btnFetch").addEventListener("click", fetchClassified);
