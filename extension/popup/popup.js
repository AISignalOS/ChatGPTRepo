document.addEventListener("DOMContentLoaded", () => {
  chrome.runtime.sendMessage({ type: "GET_RECENT" }, ({ tools }) => {
    const list = document.getElementById("tool-list");
    if (!tools || !tools.length) return;

    list.innerHTML = "";
    tools.forEach(t => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = t.url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.textContent = t.name;
      li.appendChild(a);
      list.appendChild(li);
    });
  });

  document.getElementById("open-directory").addEventListener("click", () => {
    chrome.storage.local.get(["apiUrl"], result => {
      const base = (result.apiUrl || "http://localhost:8000").replace(":8000", ":5173");
      chrome.tabs.create({ url: base });
    });
  });

  document.getElementById("open-options").addEventListener("click", e => {
    e.preventDefault();
    chrome.runtime.openOptionsPage();
  });
});
