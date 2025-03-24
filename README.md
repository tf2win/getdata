📄 README.md (fyrir niðurhalsforrit)

# 📥 Vefskrár Niðurhalsforrit

Python-forrit sem sækir sjálfkrafa myndbönd, myndir, hljóðskrár og skjöl af vefsíðu — og leitar líka dýpra í undirsíður á sama léni.

## 🎯 Hvað forritið gerir

- Tekur inn vefslóð (t.d. `www.dæmi.is`)
- Prófar sjálfkrafa bæði `https://` og `http://`
- Skannar síðuna eftir skrám með endingum eins og:
  - 📹 Myndbönd: `.mp4`, `.mkv`, `.webm` o.fl.
  - 🔊 Hljóð: `.mp3`, `.wav`, `.ogg` o.fl.
  - 🖼️ Myndir: `.jpg`, `.png`, `.svg` o.fl.
  - 📄 Skjöl: `.pdf`, `.docx`, `.zip` o.fl.
- Fer **dýpra** í undirsíður á sama léninu (recursive scanning)
- Býr til möppu og vistar allar skrár snyrtilega

## ⚙️ Uppsetning

1. Gakktu úr skugga um að þú sért með Python 3.x
2. Settu upp nauðsynlegar pakkar:

```bash
pip install requests beautifulsoup4

    Vistaðu kóðann sem sækja_vefskrár.py

🚀 Keyrsla

python sækja_vefskrár.py

Skráir inn slóð (t.d. www.rafkall.is) og forritið sækir allar tengdar skrár og vistar í möppu sem heitir t.d.:

niðurhal_rafkall.is_skjalasida

🔐 Ef vefurinn krefst innskráningar

Þú getur bætt við vefköku (cookie) ef vefurinn krefst innskráningar:

headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": "session_id=..."  # Fáðu úr vafranum þínum (Dev Tools > Application > Cookies)
}

📌 Takmarkanir

    Forritið virkar ekki á síður sem hlaða gögn með JavaScript (SPA) — nema með aðstoð eins og selenium

    Ekki ætlað til niðurhals frá vefum með höfundarréttarvarið efni án leyfis

👨‍💻 Höfundur

Skrifað með aðstoð ChatGPT í samvinnu við notanda 😄
