# LLM API Price Tracker

Live page: https://a692570.github.io/llm-price-chart/

Output price per 1M tokens (USD) for 11 providers, Jan 2025 to Nov 2026, tracked tier by tier (Opus against Opus, Sonnet against Sonnet, Flash against Flash). Every number on the page is computed from the `L` array in `index.html`.

## How the data is built

- `data/sources/*.json` holds the verified per-tier price history for each provider. Every point has a month index, the model, the output price, a VERIFIED or UNVERIFIED status, a source URL and a note.
- `data/build_data.py` turns those files into the `L` array (run from the repo root: `python3 data/build_data.py out.json`). It prints one summary line per lineage for review.
- A month's value is the price in effect on the last day of that month. Nov 2026 is the live pricing page on 18 Nov 2026.
- Standard tier, text output, lowest input-length bracket, non-thinking output where thinking and non-thinking differ. Batch, flex, priority and cached rates are excluded.
- Sources are provider pricing pages and changelogs, launch posts, and archived copies of those pages. Several archived pricing pages are stale or incomplete, so the notes in each JSON file name the snapshot each point rests on.

## What is on the page

- A lineage is one named tier followed across model generations (Claude Sonnet 3.5 to Sonnet 5.5). The board and the three headline numbers use lineages with at least 12 months of history.
- Headline numbers use only points confirmed from a dated source. Tiers whose first or last price is UNVERIFIED stay on the board (dashed ring) and are left out of the counts.
- Lineages under 12 months appear on the history charts only: Claude Fable, OpenAI Sol, Terra and Luna, Gemini 4 Argon, DeepSeek Pro, Meta Muse Spark and Muse Wonder, MiniMax Highspeed and Flash, Kimi K3.
- OpenAI Frontier (GPT-4o, GPT-4.1, GPT-5 to GPT-6.2 Astra) is the model OpenAI called its most capable at each point, so it crosses tiers. It is drawn on the history chart and left out of the board, the counts and the repricing list.

## Tier decisions

- Tier names are each provider's own. No tier is mapped onto another provider's, and no old tier is joined to a new one.
- OpenAI Mini and Nano are followed as their own lines (GPT-4o mini to GPT-5.4 mini, GPT-4.1 nano to GPT-5.4 nano). OpenAI publishes no mapping from them to Terra or Luna, so they are not joined.
- Google Pro is followed through Gemini 2.5 Pro (Sep 2026, the last month it was the Pro line). Gemini 4 Argon, Carbon, Neon and Hydrogen carry no Pro or Flash name, so Argon is its own line and Carbon ($10 intro), Neon ($15) and Hydrogen ($7.50) are not charted (under two months old).
- Gemini 3.x Pro previews ($12) are not charted. No Gemini 3.x Pro reached GA.
- Muse Ember ($0.50, launched 9 Nov 2026) and the GPT-6 Terra gap (no GPT-6 Terra exists) are not charted.

## Price caveats, shown on the page as labels

- Gemini 3.7 Flash and 3.8 Flash and Gemini 4 Argon carry "(intro price)": $3.75 (Flash) and $10 (Argon) until Dec 31 and Nov 30 2026, then $7.50 and $20. Gemini 3.8 Flash is carried into Nov 2026 at its intro price.
- DeepSeek V4 Flash, V4.1 Flash and V4 Pro carry "(peak rate)" from Aug 2026. Peak and off-peak pricing began 16 Aug 2026; the off-peak rate is half. The chart uses the peak rate.
- Meta's Llama 4 Maverick and Scout carry "(host list)". They are Together's list prices. Meta had no first-party paid API until Muse Spark in Jul 2026.
- Dashed segments are prices the research could not confirm from a fetched page: Kimi K2 (first nine months), Qwen Plus and Turbo/Flash (Apr to Jun 2026, inferred from the Jul 2026 snapshot and model IDs), Mistral Small 3.1 (Mar to Apr 2025), xAI Grok Code (Apr 2026), Llama 4 Scout (Apr to May 2026) and MiniMax M3.1 Flash.

## Other notes

- Haiku 5.5 is $0.50 against Haiku 4.5 at $5. Haiku 5.5 uses a newer tokenizer that produces about 30% more tokens for the same text, so cost per document fell less than 90%.
- Qwen figures are the Alibaba Model Studio International (Singapore) page. Qwen3.7-Max at $3.75 on the previous version of this page was not found on any snapshot, so it is dropped.
- Mistral Large 4 at $4.18 (preview, Oct 2026) became $2.10 at GA on 5 Nov 2026. The changelog mentions a launch discount, but no fetched page shows a discounted rate, so which of the two was the list rate is not settled.
- GLM-4.5 launched on 28 Jul 2025 per the changelog; the archived pricing page showing it is dated 5 Aug, so Jul 2025 rests on the changelog date.
- OpenAI GPT-5.6 Sol is $20 on the live page and the changelog calls it promotional; the post-promo price is not published.
- Earlier versions of the page charted one most-capable model per provider. The research corrected several of those values. Anthropic Aug to Oct 2025 was a tier switch from Opus ($75) to Sonnet ($15), Google Jan to Apr 2025 was a Flash price, OpenAI Dec 2025 to Feb 2026 was GPT-5.2 at $14 (not GPT-4.1 at $8), DeepSeek Mar 2025 had no $0.88 rate, and Kimi K2 is $2.50 (not $2.20). The full list is in the `discrepancies` field of each JSON file.

## Sources

developers.openai.com/api/docs/pricing, platform.claude.com/docs/en/about-claude/pricing, ai.google.dev/gemini-api/docs/pricing, api-docs.deepseek.com/quick_start/pricing, docs.x.ai/developers/pricing, dev.meta.ai/docs/pricing-rate-limits, platform.kimi.ai/docs/pricing, docs.mistral.ai, alibabacloud.com/help/en/model-studio/model-pricing, docs.z.ai/guides/overview/pricing, platform.minimax.io/docs/guides/pricing, and archived copies of each.
