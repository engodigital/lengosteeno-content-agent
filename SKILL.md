---
name: lengosteeno-daily-content
description: Agente autonomo di contenuti quotidiani per Lengosteeno (agenzia hostelería/turismo Spagna). Cerca uno spunto/notizia del giorno (settore hostelería/turismo o marketing digitale, alternati), lo commenta col metodo/differenziatore Lengosteeno, genera il formato più adatto (post singolo o carosello IG) e lo carica in GHL come bozza da revisionare — mai pubblicazione automatica. Usare quando l'utente dice "contenuto del giorno Lengosteeno", "genera il post di oggi", o quando la routine schedulata invoca questa skill.
---

# Lengosteeno — Agente Contenuti Quotidiani

Obiettivo: autorità/differenziazione. Non lead gen diretta, non brand awareness generica — mostrare *cosa fa Lengosteeno di diverso* commentando uno spunto reale del giorno.

Canale attuale: solo Instagram (LinkedIn e altri canali arriveranno dopo, con copy adattato — non fare nulla su LinkedIn come piattaforma di destinazione finché non richiesto esplicitamente).

## 0. Precondizione — verificare SEMPRE prima di generare

`mcp__gohighlevel__get_social_accounts` con `locationId: 3fFsxRcRvkat1FpJD7Yw`. Se torna 0 account: **STOP**, non generare nulla, avvisa Marco che deve connettere gli account social in GHL → Marketing → Social Planner → Connect Accounts (serve login suo, non automatizzabile). Non ha senso produrre contenuto senza una destinazione dove appoggiarlo come bozza.

## 1. Fonti — SOLO WebSearch, MAI LinkedIn, MAI scraping diretto

- **Mai LinkedIn** come fonte (deciso esplicitamente da Marco — rischio ToS troppo alto per lo scraping, e niente API gratuita affidabile).
- Per notizie AI/marketing: query tipo `site:x.com OR site:twitter.com <topic> ultime 24-48 ore`, oppure ricerca normale su testate marketing/AI.
- Per notizie hostelería/turismo: ricerca normale su fonti di settore (blog, associazioni di categoria, normative Spagna/Italia turismo).
- Alterna il filone giorno per giorno: un giorno hostelería/turismo, il giorno dopo marketing digitale applicato al settore.
- Filtra per rilevanza reale (una notizia con impatto concreto, non rumore) — criterio dal metodo di riferimento: "una notizia importante o un progetto/caso pratico che il pubblico può usare", non l'ultima cosa uscita solo perché recente.
- **Cita sempre la fonte** (nome + link) — nella caption o nell'ultima slide del carosello. Non commentare mai una notizia senza attribuirla.

## 2. Il differenziatore Lengosteeno — fonte di verità

Prima di scrivere qualsiasi copy, leggere (o rileggere se sono passati giorni):
- `/Users/marcomarengo/Documents/agency-clients/01_Engo Agency/Lengosteeno/05-contenuti/strategia/report_strategico_lengosteeno.md`
- `/Users/marcomarengo/Documents/agency-clients/01_Engo Agency/Lengosteeno/05-contenuti/strategia/piano-comunicazione-lengosteeno.html`

Lo spunto del giorno deve sempre passare per il filtro: "cosa farebbe/direbbe Lengosteeno di diverso su questo, rispetto a un'agenzia qualsiasi del settore". Se il post non supera questo filtro (è genericamente d'accordo con la notizia senza un angolo Lengosteeno), riscriverlo finché non ce l'ha.

## 3. Formato — non è sempre un carosello

Decidere caso per caso cosa comunica meglio:
- **Post singolo** con caption di approfondimento: quando lo spunto è un commento/opinione/reazione breve, non ha bisogno di essere spezzettato in step.
- **Carosello** (5-7 slide, hook/problema/soluzione/dato/CTA): quando c'è uno step-by-step, un confronto, o più punti da sviluppare in sequenza.

Non forzare un carosello ogni giorno solo per uniformità — il formato serve al messaggio, non il contrario.

## 4. Stile visivo — ATTENZIONE, non riusare lo stile personale di Marco

`~/.claude/skills/ig-carousel/references/style-utente.md` è lo stile di **@localseomarco**, l'account PERSONALE di Marco (mascotte pixel art arancione/nero) — non è il brand Lengosteeno. Non generare mai un carosello Lengosteeno con quello stile.

Questa skill usa un riferimento stile separato: `references/style-lengosteeno.md` (dentro questa stessa cartella skill).

- Se non esiste ancora: chiedere a Marco 1-3 screenshot di riferimento — l'impatto estetico che vuole è **Google Italia** su Instagram, con elementi presi anche da **Riccardo Belli** e **Starting Finance**. Vuole sfondi vari, non solo bianco/nero. Una volta ricevuti, scrivere lo spec concreto (palette hex, font, mood, sfondo) in `references/style-lengosteeno.md`, salvare gli screenshot in `references/`, e non richiederli più.
- Il brand base di Lengosteeno (colori navy/logo) è in `/Users/marcomarengo/Documents/agency-clients/01_Engo Agency/Lengosteeno/01-brand-assets/` — lo stile nuovo deve integrare questi colori, non sostituirli del tutto.
- Non generare nessuna immagine finché questo file di stile non è stato scritto e confermato — costa crediti Higgsfield, farlo a caso spreca token e budget.

## 5. Pipeline operativa

1. Verifica precondizione (step 0).
2. Determina argomento del giorno (alternanza hostelería/turismo ↔ marketing digitale).
3. WebSearch: raccogli 3-5 spunti papabili, seleziona il più rilevante.
4. Applica il differenziatore Lengosteeno (step 2) — scrivi l'angolo, non solo un riassunto della notizia.
5. Decide il formato (step 3).
6. Genera il copy (tono/voce da `copy-style` skill + i due documenti di riferimento).
7. Se carosello: genera le immagini con Higgsfield seguendo `references/style-lengosteeno.md` (stessa logica tecnica della skill `ig-carousel`, MA con questo store di stile, non quello personale).
8. Carica su GHL come bozza: `mcp__gohighlevel__create_social_post` con `status: "draft"` (mai `"scheduled"` o `"published"` da questa skill), `accountIds` dagli account trovati allo step 0, `type: "post"` (o `"reel"`/`"story"` solo se richiesto).
9. Fine. Non pubblicare mai. Marco revisiona e pubblica lui da GHL.

## 6. Loop di feedback sui numeri

Quando Marco carica un CSV con i risultati dei post (impressions, like, salvataggi, click, per post), leggerlo e aggiornare `references/feedback-lengosteeno.md` con i pattern osservati (formato/argomento/hook che performano meglio o peggio). Applicare queste regole ai cicli successivi. Non serve chiedere il CSV — se Marco lo fornisce, va processato; se non arriva, si continua con le regole già accumulate.

## Regole ferree

- Mai LinkedIn come fonte.
- Mai pubblicazione automatica — solo bozza.
- Mai lo stile @localseomarco per contenuti Lengosteeno.
- Mai un carosello senza `references/style-lengosteeno.md` confermato.
- Sempre citare la fonte della notizia.
- Se gli account social non sono connessi in GHL, fermarsi e avvisare — non procedere "per vedere come va".
