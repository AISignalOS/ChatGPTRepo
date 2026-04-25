const DEFAULT_API_URL = "http://localhost:8000";

async function getApiUrl() {
  return new Promise(resolve => {
    chrome.storage.local.get(["apiUrl"], result => {
      resolve(result.apiUrl || DEFAULT_API_URL);
    });
  });
}

async function hasBeenSubmitted(url) {
  return new Promise(resolve => {
    chrome.storage.session.get(["submittedUrls"], result => {
      const submitted = result.submittedUrls || [];
      resolve(submitted.includes(url));
    });
  });
}

async function markSubmitted(url) {
  return new Promise(resolve => {
    chrome.storage.session.get(["submittedUrls"], result => {
      const submitted = result.submittedUrls || [];
      submitted.push(url);
      chrome.storage.session.set({ submittedUrls: submitted }, resolve);
    });
  });
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "TOOL_DETECTED") {
    const { payload } = message;

    hasBeenSubmitted(payload.url).then(already => {
      if (already) {
        sendResponse({ status: "duplicate" });
        return;
      }

      markSubmitted(payload.url).then(() => {
        getApiUrl().then(apiUrl => {
          fetch(`${apiUrl}/api/tools`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          })
            .then(r => r.json())
            .then(tool => {
              chrome.storage.local.get(["recentTools"], result => {
                const recent = result.recentTools || [];
                recent.unshift({ name: tool.name, url: tool.url, id: tool.id });
                chrome.storage.local.set({ recentTools: recent.slice(0, 20) });
              });
              sendResponse({ status: "ok", tool });
            })
            .catch(err => {
              console.error("[Research Agent] API error:", err);
              sendResponse({ status: "error", error: err.message });
            });
        });
      });
    });

    return true; // keep channel open for async sendResponse
  }

  if (message.type === "GET_RECENT") {
    chrome.storage.local.get(["recentTools"], result => {
      sendResponse({ tools: result.recentTools || [] });
    });
    return true;
  }
});
