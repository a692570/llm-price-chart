# LLM Flagship API Price Tracker

Live page: https://a692570.github.io/llm-price-chart/

Flagship output price per 1M tokens (USD, standard tier) for 11 providers, Jan 2025 to Nov 2026. All figures on the page are computed from the arrays in `index.html`.

## Data notes

These live here, not on the page.

- Each line tracks one provider's most capable API model at the time. Prices checked 18 Nov 2026 against provider pricing pages.
- A month's value is the price in effect that month.
- DeepSeek plots off-peak rates. Peak is Mon to Fri 01:00 to 04:00 and 06:00 to 10:00 UTC, at 2x ($3.96).
- Meta's values before Oct 2026 are representative host list rates (Together, DeepInfra). Meta ran no first-party API until Muse Wonder on the Meta Model API.
- xAI's 2025 rates (Grok 2 $10, Grok 3 and 4 $15) come from xAI's published 2025 rate card.
- Kimi K2 uses Moonshot's 0711 list rate. K2.5 interim pricing in early 2026 is not tracked. The K2 series closed to new users Oct 31.
- Qwen3.7-Max is shown at its 50% promo rate ($3.75; list $7.50). The May 2026 price ($2.40) has no model name in the source data.
- Gemini 4 Argon's $10 is an intro rate that steps to $20 on Dec 1.
- Anthropic's line follows the Fable tier from Jun 2026, when it became Anthropic's most capable model. GLM-5.3 (Aug 2026) kept GLM-5.2's $4.40.
- Not charted: GPT-6 Luna ($0.50), GPT-5.6 Terra ($12), Sonnet 5.5 ($10), Gemini 3.x Flash promo ($3.75). GPT-5.6 Sol ($30) sits between GPT-5.5 and GPT-6 at an unchanged price.
- "First charted price" is each provider's first non-empty month: Jan 2025 for most, Apr 2025 for Meta, Jul 2025 for GLM and Kimi. The 188x to 33x spread uses the 8 providers with a Jan 2025 price.

## Sources (verified 18 Nov 2026)

developers.openai.com/api/docs/pricing, platform.claude.com/docs/en/about-claude/pricing, ai.google.dev/gemini-api/docs/pricing, api-docs.deepseek.com/quick_start/pricing, docs.x.ai/developers/pricing, dev.meta.ai/docs/pricing-rate-limits, platform.kimi.ai/docs/pricing/chat, platform.minimax.io/docs/pricing/overview, docs.z.ai/guides/overview/pricing, alibabacloud.com Model Studio pricing, mistral.ai/pricing/api.
