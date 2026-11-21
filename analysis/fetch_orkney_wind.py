"""Fetch hourly wind speed at 100 m (m/s) for Orkney, 2016-2025, from the Open-Meteo historical weather API
(ERA5 reanalysis), for entry 06. One point on Orkney Mainland. Times are UTC, which matches the ANM data:
each of its years has exactly 48 half-hours a day, with no daylight saving gaps or repeats.
Writes cache/orkney-wind.json = {"lat": .., "lon": .., "time": [...], "ws100": [...]}."""
import json, os, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cache", "orkney-wind.json")
LAT, LON = 59.0, -3.05          # central Orkney Mainland
START, END = "2016-01-01", "2025-12-31"

url = ("https://archive-api.open-meteo.com/v1/archive?"
       f"latitude={LAT}&longitude={LON}&start_date={START}&end_date={END}"
       "&hourly=wind_speed_100m&wind_speed_unit=ms&timezone=GMT")
for attempt in range(8):
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            j = json.load(r)
        break
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, "- waiting", flush=True)
        time.sleep(90 if e.code == 429 else 20)
    except Exception as e:
        print("error", e, flush=True)
        time.sleep(20)
else:
    raise SystemExit("gave up")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({"lat": LAT, "lon": LON, "time": j["hourly"]["time"], "ws100": j["hourly"]["wind_speed_100m"]}, open(OUT, "w"), separators=(",", ":"))
print("done", len(j["hourly"]["time"]), "hours", flush=True)
