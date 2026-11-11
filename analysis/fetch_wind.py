"""Fetch daily maximum wind gust (mph) for each SSEN fault-reporting district, 2016-2025,
from the Open-Meteo historical weather API (ERA5 reanalysis). One point per district:
the average position of the primary substations that fault records in that district name.
Writes cache/wind.json = {"days": [...], "gust": {"AREA/DISTRICT": [...]}}. Paced to stay
inside Open-Meteo's free-tier limits; re-running skips districts already fetched."""
import json, os, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cache", "wind.json")
START, END = "2016-01-01", "2025-12-31"
districts = json.load(open(os.path.join(HERE, "districts.json")))
out = json.load(open(OUT)) if os.path.exists(OUT) else {"days": None, "gust": {}}

for d in districts:
    key = f"{d['area']}/{d['d']}"
    if key in out["gust"]:
        continue
    url = ("https://archive-api.open-meteo.com/v1/archive?"
           f"latitude={d['lat']}&longitude={d['lon']}&start_date={START}&end_date={END}"
           "&daily=wind_gusts_10m_max&wind_speed_unit=mph&timezone=Europe%2FLondon")
    for attempt in range(8):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                j = json.load(r)
            break
        except urllib.error.HTTPError as e:
            print(key, "HTTP", e.code, "- waiting", flush=True)
            time.sleep(90 if e.code == 429 else 20)
        except Exception as e:
            print(key, "error", e, flush=True)
            time.sleep(20)
    else:
        raise SystemExit(f"gave up on {key}")
    out["days"] = out["days"] or j["daily"]["time"]
    assert j["daily"]["time"] == out["days"]
    out["gust"][key] = j["daily"]["wind_gusts_10m_max"]
    json.dump(out, open(OUT, "w"), separators=(",", ":"))
    print(key, "ok", len(out["gust"]), "of", len(districts), flush=True)
    time.sleep(12)
print("done")
