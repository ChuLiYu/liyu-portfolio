# Hero visual spec: "Transaction log" card

Status: approved by the site owner for implementation (2026-11-11). Author: Claude (spec). Implementer: Codex.

## Goal

Give the home page one memorable first impression that also proves the owner's core selling point:
backend systems that stay correct when something fails, from banking transactions to AI agents.

Audience: recruiters (6–10 second scan) and engineering managers, including conservative financial
institutions. Tone must be **calm, controlled and evidence-based**, not alarming or flashy.

## Positioning copy (use exactly)

| Element | English (`website/index.html`) | zh-TW (`website/index-zh.html`) |
|---|---|---|
| Eyebrow | keep current | keep current |
| H1 | keep current name | keep current name |
| Headline (`.headline`) | `Every transaction accounted for. <strong>Every AI action bounded.</strong>` | `每筆交易都對得上，<strong>每個 AI 動作都有邊界。</strong>` |
| Sub line (new `p.lead`, under headline) | `Java / Spring Boot backend engineer with three years in internet banking, now building AI tools with the same controls.` | `三年網路銀行 Java／Spring Boot 後端經驗，用同樣的控管標準打造 AI 工具。` |

Do not change `<head>` metadata.

## Layout

- Desktop (> 860px): hero becomes two columns. Left column: avatar (shrink to 96px, placed above the eyebrow, not beside it), eyebrow, H1, headline, lead, CTA buttons. Right column (~420px): the transaction log card. Vertically centred.
- ≤ 860px: single column; card goes after the CTA buttons, full width.
- The existing four `.facts` tiles stay below the hero, unchanged.
- Add a static **controls strip** directly below `.facts` (see below). No marquee, no scrolling animation.
- No horizontal overflow at 375px width.

## Transaction log card

A dark panel styled like a monitoring/audit log (monospace for log lines, `ui-monospace, SFMono-Regular, Menlo, monospace`). Uses existing CSS variables. **No red anywhere.** Colours: neutral text for events, `--amber` for pending/retry states, `--green` for the final settled line.

Structure:

1. Header row: small label `Recovery log` (zh: `復原紀錄`) and three tab buttons:
   `Bank debit` / `AI agent write` / `Node failure` (zh: `銀行扣款` / `AI 寫入` / `節點故障`).
2. Body: 3–4 log lines for the selected scenario, each with a short state tag on the right.
3. Footer: one small muted line with the source, linking where noted.

Scenarios (keep wording; zh translations below):

| # | Lines (state tag in brackets) | Footer |
|---|---|---|
| 1 Bank debit | `debit request → core banking` [SENT] · `response timed out` [PENDING] · `retry with same request ID` [RETRY] · `✓ settled once` [SETTLED] | `Illustrative pattern from internet-banking work` (no link) |
| 2 AI agent write | `Claude: mark task "Pay rent" done` [REQUEST] · `task changed since it was read` [CONFLICT] · `✓ write rejected, nothing overwritten` [SAFE] | `Google Tasks MCP` → https://github.com/ChuLiYu/google-tasks-mcp |
| 3 Node failure | `leader node-1 stops responding` [DOWN] · `node-2 elected leader` [ELECTION] · `✓ committed jobs intact` [COMMITTED] | `Raft-Recovery` → https://github.com/ChuLiYu/raft-recovery |

zh-TW lines:
1. `扣款請求 → 核心系統` · `回應逾時` · `以相同請求 ID 重試` · `✓ 只扣款一次`；footer `依網路銀行工作經驗示意`
2. `Claude：將「繳房租」標為完成` · `任務在讀取後已被修改` · `✓ 拒絕寫入，未覆蓋任何資料`
3. `leader node-1 無回應` · `node-2 當選 leader` · `✓ 已提交的工作完整保留`

State tags stay in English in both languages (they read as log codes). DOWN/CONFLICT/PENDING/RETRY/ELECTION use amber; final line and its tag use green; SENT/REQUEST neutral.

Behaviour:

- On load, lines of scenario 1 appear one by one (~600 ms apart, simple fade/slide 4px). After the last line, hold ~2.5 s, then advance to scenario 2, then 3. **Play the cycle once**, then stop on scenario 3. No infinite loop.
- Clicking a tab stops autoplay and shows that scenario (animate its lines once).
- `prefers-reduced-motion: reduce`: no animation, no autoplay; show scenario 1 fully; tabs still work.
- Pause autoplay while the tab is hidden (`visibilitychange`) — optional but preferred.
- Without JavaScript: scenario 1 is fully visible in the HTML; tabs may be hidden via a `.js` class on `<html>` set by the script.
- Accessibility: tabs are `<button>` with `aria-pressed` (or a proper tablist with `aria-selected`); log body is not `aria-live` (avoid announcing animation). Each scenario's text must be present in the DOM or rendered from a data structure in the script — either is fine, but keep translations in the HTML (e.g. `<template>` or `data-` blocks) so the script is language-neutral.

## Controls strip

A single row of 4 small items, muted, separated by thin dividers, wrapping on mobile:

- EN: `Idempotent retries` · `Checkpoint in the same transaction` · `AI read-only by default` · `Majority-commit writes`
- zh: `冪等重試` · `checkpoint 與資料同一交易` · `AI 預設唯讀` · `多數節點 commit 才寫入`

Each item has a small green check. No links, no animation.

## Constraints

- Static site, no build step, no new dependencies, no external requests. Vanilla JS in `website/assets/js/hero.js`, loaded with `defer` from both pages.
- CSS goes in `website/assets/css/site.css`; reuse existing variables and classes where possible.
- Keep everything else on both pages unchanged.
- Both pages must stay in sync structurally.

## Acceptance

1. Both pages render the new headline, lead, card and strip; no console errors.
2. Autoplay runs through the three scenarios once, then stops; tab clicks work; reduced-motion shows a static card.
3. No horizontal overflow at 375px; card readable at 375px and 1280px.
4. No red colour used in the card; no infinite animations on the page.
5. HTML remains valid (tags balanced); no changes to `<head>` metadata.

## Out of scope

Interactive Raft demo, marquee, new sections, copy changes elsewhere.
