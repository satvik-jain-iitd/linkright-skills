# ref_03 — Portfolio HTML Template

## Architecture

```
portfolio/
├── index.html          ← intro + 3 featured case studies + contact
├── about.html          ← professional narrative (not a resume)
└── cases/
    ├── <slug>.html     ← each full case study
    └── ...
```

---

## index.html Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Name] — Product Manager</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #FAFAFA;
      color: #1A1A1A;
      line-height: 1.6;
      max-width: 760px;
      margin: 0 auto;
      padding: 48px 24px;
    }
    .name { font-size: 28px; font-weight: 700; letter-spacing: -0.5px; }
    .tagline { color: #555; margin-top: 6px; font-size: 15px; }
    .contact { margin-top: 12px; font-size: 13px; color: #666; }
    .contact a { color: #0066CC; text-decoration: none; }
    .divider { border: none; border-top: 1px solid #E5E5E5; margin: 40px 0; }
    .section-label { font-size: 11px; font-weight: 600; letter-spacing: 1.5px;
                     text-transform: uppercase; color: #888; margin-bottom: 20px; }
    .case-card {
      padding: 24px;
      background: #FFF;
      border: 1px solid #E5E5E5;
      border-radius: 6px;
      margin-bottom: 16px;
      transition: border-color 0.15s;
    }
    .case-card:hover { border-color: #0066CC; }
    .case-card a { text-decoration: none; color: inherit; }
    .case-title { font-size: 17px; font-weight: 600; margin-bottom: 6px; }
    .case-meta { font-size: 12px; color: #888; margin-bottom: 10px; }
    .case-summary { font-size: 14px; color: #444; line-height: 1.55; }
    .case-metric {
      display: inline-block;
      margin-top: 12px;
      font-size: 13px;
      font-weight: 600;
      color: #0066CC;
    }
    footer { margin-top: 60px; font-size: 12px; color: #AAA; }
  </style>
</head>
<body>

  <h1 class="name">[Name]</h1>
  <p class="tagline">[1-sentence professional descriptor — e.g., "Product Manager specializing in growth and 0→1 products"]</p>
  <p class="contact">
    <a href="mailto:[email]">[email]</a> ·
    <a href="https://linkedin.com/in/[handle]">LinkedIn</a> ·
    <a href="about.html">About</a>
  </p>

  <hr class="divider">

  <p class="section-label">Selected Work</p>

  <!-- Case Card 1 -->
  <div class="case-card">
    <a href="cases/[slug-1].html">
      <p class="case-meta">[Company] · [Role] · [Year]</p>
      <p class="case-title">[Case Study Title]</p>
      <p class="case-summary">[2-3 sentence summary of the problem and approach]</p>
      <span class="case-metric">[Key metric outcome — e.g., "↑ 30-day retention from 28% → 41%"]</span>
    </a>
  </div>

  <!-- Case Card 2 -->
  <div class="case-card">
    <a href="cases/[slug-2].html">
      <p class="case-meta">[Company] · [Role] · [Year]</p>
      <p class="case-title">[Case Study Title]</p>
      <p class="case-summary">[2-3 sentence summary]</p>
      <span class="case-metric">[Key metric]</span>
    </a>
  </div>

  <!-- Case Card 3 -->
  <div class="case-card">
    <a href="cases/[slug-3].html">
      <p class="case-meta">[Company] · [Role] · [Year]</p>
      <p class="case-title">[Case Study Title]</p>
      <p class="case-summary">[2-3 sentence summary]</p>
      <span class="case-metric">[Key metric]</span>
    </a>
  </div>

  <footer>
    Last updated [Month Year]
  </footer>

</body>
</html>
```

---

## Case Study Page Template (cases/[slug].html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Case Title] — [Name]</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #FAFAFA;
      color: #1A1A1A;
      line-height: 1.7;
      max-width: 680px;
      margin: 0 auto;
      padding: 48px 24px;
    }
    .back { font-size: 13px; color: #0066CC; text-decoration: none;
            display: inline-block; margin-bottom: 32px; }
    .back:hover { text-decoration: underline; }
    .case-label { font-size: 11px; font-weight: 600; letter-spacing: 1.5px;
                  text-transform: uppercase; color: #888; margin-bottom: 8px; }
    h1 { font-size: 26px; font-weight: 700; letter-spacing: -0.5px;
         line-height: 1.25; margin-bottom: 12px; }
    .meta { font-size: 13px; color: #888; margin-bottom: 8px; }
    .tldr {
      background: #F0F4FF;
      border-left: 3px solid #0066CC;
      padding: 14px 18px;
      margin: 28px 0;
      font-size: 14px;
      color: #333;
    }
    .tldr strong { display: block; font-size: 11px; letter-spacing: 1px;
                   text-transform: uppercase; color: #0066CC; margin-bottom: 6px; }
    .divider { border: none; border-top: 1px solid #E5E5E5; margin: 36px 0; }
    h2 { font-size: 13px; font-weight: 700; letter-spacing: 1.5px;
         text-transform: uppercase; color: #888; margin-bottom: 12px; }
    p { font-size: 15px; color: #2A2A2A; margin-bottom: 16px; }
    ul { padding-left: 20px; margin-bottom: 16px; }
    li { font-size: 15px; color: #2A2A2A; margin-bottom: 6px; }
    .metric-block {
      background: #FFF;
      border: 1px solid #E5E5E5;
      border-radius: 6px;
      padding: 20px;
      margin: 24px 0;
    }
    .metric-block .metric-row {
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      padding: 6px 0;
      border-bottom: 1px solid #F0F0F0;
    }
    .metric-block .metric-row:last-child { border-bottom: none; }
    .metric-label { color: #666; }
    .metric-value { font-weight: 600; color: #0066CC; }
    .learning-box {
      background: #FFF8EE;
      border-left: 3px solid #F5A623;
      padding: 14px 18px;
      margin: 28px 0;
      font-size: 14px;
      color: #4A3000;
    }
    .learning-box strong { display: block; font-size: 11px; letter-spacing: 1px;
                           text-transform: uppercase; color: #B87010; margin-bottom: 6px; }
    footer { margin-top: 60px; font-size: 12px; color: #AAA; }
    footer a { color: #0066CC; text-decoration: none; }
  </style>
</head>
<body>

  <a href="../index.html" class="back">← Back to work</a>

  <p class="case-label">Case Study</p>
  <h1>[Case Study Title]</h1>
  <p class="meta">[Company] · [Role] · [Timeframe]</p>

  <!-- TL;DR for quick scanners -->
  <div class="tldr">
    <strong>TL;DR</strong>
    [2-3 sentence summary: problem → what you did → key outcome]
  </div>

  <hr class="divider">

  <h2>1. Context</h2>
  <p>[Context paragraph(s)]</p>

  <hr class="divider">

  <h2>2. Problem</h2>
  <p>[Problem paragraph(s) with evidence]</p>

  <hr class="divider">

  <h2>3. Constraints</h2>
  <p>[Constraints paragraph(s)]</p>

  <hr class="divider">

  <h2>4. Approach</h2>
  <p>[Approach paragraph(s) — show reasoning, alternatives considered]</p>

  <hr class="divider">

  <h2>5. Execution</h2>
  <p>[Execution paragraph(s)]</p>

  <hr class="divider">

  <h2>6. Outcome</h2>

  <!-- Metrics block for visual impact -->
  <div class="metric-block">
    <div class="metric-row">
      <span class="metric-label">[Metric name]</span>
      <span class="metric-value">[before] → [after]</span>
    </div>
    <div class="metric-row">
      <span class="metric-label">[Metric name 2]</span>
      <span class="metric-value">[value]</span>
    </div>
  </div>

  <p>[Outcome context paragraph — scope, confidence, caveats]</p>

  <hr class="divider">

  <h2>7. What I Learned</h2>

  <div class="learning-box">
    <strong>Learning</strong>
    [One honest, specific learning]
  </div>

  <footer>
    <a href="../index.html">← All work</a> · [Name] · [Year]
  </footer>

</body>
</html>
```

---

## Design Principles

- No heavy JS frameworks — pure HTML + inline CSS
- Mobile-first: max-width 680-760px, 24px side padding
- Information hierarchy: recruiter should get the story in 10 seconds (TL;DR + metric block)
- No personal photos unless user provides one
- Color: neutral base (#FAFAFA, #FFF, #1A1A1A) + one accent (#0066CC for links/metrics)
- Section 7 gets its own distinct box (amber) — signals it's the honest learning section

## File Naming

Case study slugs: lowercase, hyphenated, company-and-topic format
- Example: `stripe-onboarding-redesign.html`
- Example: `figma-growth-experiment.html`
- Example: `notion-platform-migration.html`
