# Grid Labs

A public notebook of experiments on the open data published by Scottish and Southern Electricity Networks (SSEN) Distribution. Companion to [Grid Lens](https://lens.nacharya.com.np/), which shows the data as published.

Each entry asks one question, shows the method, states the result and lists what the result cannot support. Entries marked **Finding** recompute their figures from SSEN's data in the reader's browser each time the page opens.

| Entry | Question | Status |
|---|---|---|
| 01 | Is more generation contracted than the grid supply points can carry? | Finding |
| 02 | Do faults rise with wind, and where do they rise most? | Planned |
| 03 | Does SSEN buy flexibility where it marks the network as constrained? | Planned |
| 04 | Which primaries will run out of headroom before their reinforcement arrives? | Planned |

Static site, no build step. To run locally:

```bash
python3 -m http.server 5179
```

Not affiliated with SSEN. Nothing here is a substitute for a connection application or engineering study.
