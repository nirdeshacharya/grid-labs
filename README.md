# Grid Labs

A public notebook of experiments on the open data published by Scottish and Southern Electricity Networks (SSEN) Distribution. Companion to [Grid Lens](https://nirdeshacharya.github.io/grid-lens/), which shows the data as published.

Each entry asks one question, shows the method, states the result and lists what the result cannot support. Entry 01 recomputes its figures from SSEN's data in the reader's browser each time the page opens. Entries 02 and 04 are dated snapshots; the scripts that produced them are in `analysis/`.

| Entry | Question | Status |
|---|---|---|
| 01 | Is more generation contracted than the grid supply points can carry? | Finding |
| 02 | At what wind speed do faults take off, and which places are most sensitive? | Finding (snapshot) |
| 04 | Where could home electrification use up substation headroom before upgrades arrive? | Finding (snapshot, adjustable) |

Static site, no build step. To run locally:

```bash
python3 -m http.server 5179
```

Not affiliated with SSEN. Nothing here is a substitute for a connection application or engineering study.
