import urllib.request
import json
import os

ALBUM_ID = "489bea04-5977-4ad3-a887-39d4c2417ccd"
KEY = "Cks998GVUDZyrrPVsjQuAPKHGHhT0y6Q-2tFpJd3gv1k6a61Fov4_cj6kcc5j5JZfv4"
HOST = "https://photos.mvoorhies.com"

# Query the public share link to obtain all asset metadata
req = urllib.request.Request(
    f"{HOST}/api/shared-links/me?key={KEY}",
    headers={"User-Agent": "Mozilla/5.0"}
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        album = data.get("album", {})
        assets = album.get("assets", []) or data.get("assets", [])
        
        # If the top-level route omitted assets, fetch the album payload
        if not assets and album.get("id"):
            req2 = urllib.request.Request(
                f"{HOST}/api/albums/{album['id']}?key={KEY}&withoutAssets=false",
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req2) as resp2:
                data2 = json.loads(resp2.read().decode())
                assets = data2.get("assets", [])
except Exception as e:
    print(f"Error querying Immich: {e}")
    assets = []

print(f"Discovered {len(assets)} assets in Showcase album.")
