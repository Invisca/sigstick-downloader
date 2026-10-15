
import re
import urllib.request
from pathlib import Path
from html import unescape

packs = {
    "Almarts27": "XgR2twwRHeuxPhfpyMkX",
    "Hamster_Doodle_Pt4": "YarEKicOzFAlGdqpnVFU"
}

base = "https://www.sigstick.com/pack/"
headers = {"User-Agent": "Mozilla/5.0"}

for name, pack_id in packs.items():
    folder = Path.home() / "Downloads" / "Hamster_Stickers" / name
    folder.mkdir(parents=True, exist_ok=True)

    request = urllib.request.Request(base + pack_id, headers=headers)
    html = urllib.request.urlopen(request).read().decode("utf-8")
    html = unescape(html).replace("\\/", "/")

    urls = sorted(set(re.findall(
        rf'https?://cdn2\.cdnstep\.com/{pack_id}/[^"\'<>\s]+?\.(?:png|webp|gif)',
        html
    )))

    print(f"{name}: found {len(urls)} images")

    for i, url in enumerate(urls, 1):
        original = url.replace(".thumb128", "")
        extension = url.rsplit(".", 1)[-1]

        for candidate in dict.fromkeys([original, url]):
            try:
                req = urllib.request.Request(candidate, headers=headers)
                data = urllib.request.urlopen(req, timeout=15).read()
                (folder / f"sticker_{i:03d}.{extension}").write_bytes(data)
                break
            except Exception:
                continue

print("Finished! Check Downloads/Hamster_Stickers")
