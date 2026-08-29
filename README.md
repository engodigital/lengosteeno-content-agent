# Lengosteeno — Agente Contenuti Quotidiani

Repo di supporto per la routine cloud che genera il contenuto Instagram
quotidiano di Lengosteeno (autorità/differenziazione nel settore
hostelería/turismo). La routine clona questo repo ad ogni esecuzione.

## Contenuto

- `scraper/fetch_news.py` — scraping deterministico via RSS (nessun AI
  coinvolto in questo step). Legge `scraper/feeds.json`, ritorna JSON con
  gli articoli delle ultime N ore. Testato e funzionante con feed reali:
  Hosteltur, Preferente, Search Engine Land, Marketing AI Institute,
  Social Media Today.
- Metodo e differenziatore Lengosteeno: **non in questo repo** (repo
  pubblico, quei documenti sono riservati). Vivono su Google Drive,
  letti dalla routine via connettore Drive — link in `SKILL.md`.
- `SKILL.md` — la pipeline completa passo-passo (stessa skill installata
  in locale su `~/.claude/skills/lengosteeno-daily-content/`).

## Cosa manca ancora (non fatto in questa sessione)

- `reference/style-lengosteeno.md` — stile visivo carosello (Google
  Italia + Riccardo Belli + Starting Finance) — da creare quando Marco
  manda gli screenshot di riferimento. Finché manca, niente immagini.
- Verifica reale che GHL accetti un post in bozza via `curl` con la API
  key (non ancora testato end-to-end).
- La routine cloud vera e propria (da creare via /schedule).

## Backlog editoriale

Vive in Google Sheets, non in questo repo (accesso umano diretto):
https://docs.google.com/spreadsheets/d/1LlQB57S4dABziofiuKF-uy5rwid1TNLboWJGlkWBjPw

## Segreti — MAI in questo repo

`GHL_API_KEY` e `GHL_LOCATION_ID` vengono passati alla routine come
variabili d'ambiente/secret, mai committati qui.
