document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("api-url");
  const status = document.getElementById("status");

  chrome.storage.local.get(["apiUrl"], result => {
    input.value = result.apiUrl || "http://localhost:8000";
  });

  document.getElementById("save").addEventListener("click", () => {
    const url = input.value.trim().replace(/\/$/, "");
    chrome.storage.local.set({ apiUrl: url }, () => {
      status.textContent = "Saved!";
      setTimeout(() => { status.textContent = ""; }, 2000);
    });
  });
});
