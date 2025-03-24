import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

visited_urls = set()
media_extensions = [
    # 📹 Myndbönd
    "mp4", "mov", "webm", "avi", "mkv", "flv", "wmv", "m4v",

    # 🔊 Hljóð
    "mp3", "wav", "ogg", "aac", "flac", "wma", "m4a",

    # 🖼️ Myndir
    "jpg", "jpeg", "png", "gif", "svg", "bmp", "tiff", "webp", "ico",

    # 📄 Skjöl
    "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "rtf", "odt", "ods", "odp",

    # 🗃️ Þjöppuð gögn
    "zip", "rar", "7z", "tar", "gz", "bz2", "xz",

    # ⚙️ Forrit & gögn
    "csv", "json", "xml", "yml", "ini", "log",

    # 🔐 Skjöl með lykilorði eða dulkóðun
    "key", "pem", "crt", "pfx"
]
headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_url_with_fallback(raw_url, headers=None):
    if not raw_url.startswith("http"):
        url_https = "https://" + raw_url
        url_http = "http://" + raw_url
    else:
        url_https = raw_url
        url_http = raw_url.replace("https://", "http://")

    try:
        print(f"🔍 Prófa: {url_https}")
        response = requests.get(url_https, headers=headers, timeout=10)
        response.raise_for_status()
        return url_https, response
    except Exception as e:
        print(f"⚠️  HTTPS virkaði ekki: {e}")

    try:
        print(f"🔍 Prófa: {url_http}")
        response = requests.get(url_http, headers=headers, timeout=10)
        response.raise_for_status()
        return url_http, response
    except Exception as e:
        print(f"❌ HTTP virkaði ekki heldur: {e}")
        return None, None

def crawl_and_download(url, base_folder, domain):
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        print(f"\n🌐 Skoða: {url}")
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ Gat ekki sótt {url}: {e}")
        return

    soup = BeautifulSoup(res.text, "html.parser")

    for tag in soup.find_all(["a", "source", "img", "video", "audio", "iframe", "embed"]):
        for attr in ["href", "src"]:
            if tag.has_attr(attr):
                link = tag[attr]
                full_url = urljoin(url, link)
                ext = full_url.lower().split("?")[0].split(".")[-1]

                if ext in media_extensions:
                    filename = os.path.basename(full_url.split("?")[0])
                    save_path = os.path.join(base_folder, filename)

                    try:
                        print(f"⬇ Sæki {filename}...")
                        with requests.get(full_url, stream=True, headers=headers, timeout=15) as r:
                            r.raise_for_status()
                            with open(save_path, "wb") as f:
                                for chunk in r.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                        print(f"✅ Vistað: {save_path}")
                    except Exception as e:
                        print(f"⚠ Gat ekki sótt {full_url}: {e}")

    # Leitum að fleiri tenglum á sömu síðu og köllum aftur á fallið
    for link_tag in soup.find_all("a", href=True):
        next_url = urljoin(url, link_tag['href'])
        if domain in next_url and next_url not in visited_urls:
            crawl_and_download(next_url, base_folder, domain)

# === Aðal keyrsla ===
if __name__ == "__main__":
    raw_url = input("📥 Sláðu inn vefslóð: ").strip()
    url, response = fetch_url_with_fallback(raw_url, headers)

    if not response:
        print("🚫 Ekki tókst að nálgast síðuna.")
    else:
        parsed = urlparse(url)
        domain = parsed.netloc
        safe_name = parsed.path.strip("/").replace("/", "_") or "niðurhal"
        folder_name = f"niðurhal_{domain}_{safe_name}"
        os.makedirs(folder_name, exist_ok=True)

        crawl_and_download(url, folder_name, domain)

        print(f"\n🎉 Lokið! Gögn vistuð í möppunni: {folder_name}")
