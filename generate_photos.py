import os
import json
import urllib.request
import urllib.error
from pathlib import Path

# Parse .env directly without third-party libraries
env_path = Path(".env")
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

IMMICH_URL = os.getenv("IMMICH_INSTANCE_URL", "https://photos.mvoorhies.com").rstrip("/")
API_KEY = os.getenv("IMMICH_API_KEY")
ALBUM_ID = os.getenv("IMMICH_ALBUM_ID")

def fetch_album_photos():
    if not API_KEY or not ALBUM_ID:
        print("[WARN] Missing IMMICH_API_KEY or IMMICH_ALBUM_ID in environment.")
        return []

    url = f"{IMMICH_URL}/api/albums/{ALBUM_ID}"
    req = urllib.request.Request(url, headers={
        "x-api-key": API_KEY,
        "Accept": "application/json"
    })

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Failed to fetch album: HTTP {e.code} - {e.reason}")
        return []
    except Exception as e:
        print(f"[ERROR] Unexpected request failure: {e}")
        return []

    assets = data.get("assets", [])
    photos = []

    for item in assets:
        asset_id = item.get("id")
        desc = item.get("description", "") or ""
        tags = [t.strip("#") for t in desc.split() if t.startswith("#")]
        clean_desc = " ".join([w for w in desc.split() if not w.startswith("#")]).strip()

        # Extract EXIF telemetry safely
        exif = item.get("exifInfo") or {}
        make = exif.get("make") or ""
        model = exif.get("model") or ""
        camera = f"{make} {model}".strip() if (make or model) else "Standard Optics"
        lens = exif.get("lensModel") or ""
        focal_length = f"{exif.get('focalLength')}mm" if exif.get("focalLength") else ""
        f_number = f"f/{exif.get('fNumber')}" if exif.get("fNumber") else ""
        exposure_time = exif.get("exposureTime") or ""
        iso = f"ISO {exif.get('iso')}" if exif.get("iso") else ""
        date_taken = exif.get("dateTimeOriginal") or item.get("fileCreatedAt") or ""

        photos.append({
            "id": asset_id,
            "title": clean_desc if clean_desc else "Field Capture",
            "tags": tags if tags else ["landscape"],
            "url": f"{IMMICH_URL}/api/assets/{asset_id}/thumbnail?size=preview",
            "fullUrl": f"{IMMICH_URL}/api/assets/{asset_id}/original",
            "exif": {
                "camera": camera,
                "lens": lens,
                "focalLength": focal_length,
                "aperture": f_number,
                "shutter": exposure_time,
                "iso": iso,
                "date": date_taken[:10] if date_taken else ""
            }
        })

    return photos

if __name__ == "__main__":
    photos_data = fetch_album_photos()
    out_path = "src/data/photos.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(photos_data, f, indent=2)
    print(f"[SUCCESS] Exported {len(photos_data)} photos with EXIF telemetry to {out_path}")
