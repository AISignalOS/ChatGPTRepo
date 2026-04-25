(function () {
  if (window.__researchAgentRan) return;
  window.__researchAgentRan = true;

  const SIGNALS = {
    keywords: [
      "ai-powered", "powered by ai", "artificial intelligence",
      "machine learning", "llm", "large language model",
      "gpt", "claude", "generative ai", "neural network",
      "natural language", "ai assistant", "ai tool", "ai platform"
    ],
    pricingIndicators: [
      "per month", "/month", "per seat", "free tier", "free plan",
      "pricing", "upgrade to pro", "enterprise plan", "contact sales",
      "free forever", "billed annually", "per user"
    ],
    structuralSelectors: [
      "[class*='pricing']", "[id*='pricing']",
      "[class*='feature']", "[class*='plan']",
      "[class*='hero']", "[class*='cta']",
      "table", "section"
    ]
  };

  function scorePageAsAITool() {
    const bodyText = document.body.innerText.toLowerCase();
    let score = 0;

    SIGNALS.keywords.forEach(kw => {
      if (bodyText.includes(kw)) score += 2;
    });
    SIGNALS.pricingIndicators.forEach(kw => {
      if (bodyText.includes(kw)) score += 1;
    });
    SIGNALS.structuralSelectors.forEach(sel => {
      if (document.querySelector(sel)) score += 1;
    });

    return score;
  }

  function extractPageData() {
    const metaDesc = document.querySelector('meta[name="description"]')?.content || "";
    const ogTitle = document.querySelector('meta[property="og:title"]')?.content || "";
    const h1 = document.querySelector("h1")?.innerText || "";

    const mainContent =
      document.querySelector("main, article, [role='main'], .hero, .landing") ||
      document.body;

    const rawContent = mainContent.innerText.slice(0, 10000);

    return {
      name: ogTitle || h1 || document.title,
      url: window.location.href,
      description: metaDesc,
      raw_content: rawContent
    };
  }

  const THRESHOLD = 4;

  if (scorePageAsAITool() >= THRESHOLD) {
    const data = extractPageData();
    chrome.runtime.sendMessage({ type: "TOOL_DETECTED", payload: data });
  }
})();
