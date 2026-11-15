# ⚖️ VeloxCheck — Verifica Conformità Autovelox & Ricorsi Prefetto

Piattaforma Micro-SaaS completamente automatizzata per la verifica di conformità delle multe per eccesso di velocità e la generazione istantanea del **Ricorso formale al Prefetto** ai sensi della **Sentenza Cassazione Civile n. 10505/2024**, della **Corte Costituzionale n. 113/2015** e dei **Decreti MIT 305/2025 e 367/2025**.

---

## 🚀 Come Provare Subito l'Applicazione

La Web App è progettata in modalità **Dual-Core**: funziona sia con il server Python, sia in modalità **Standalone nel browser (Client-Side) a costo zero**.

### Metodo 1: Apertura Istantanea nel Browser (Senza installare nulla)
1. Apri la cartella `web/` nel tuo esploratore file:
   `c:\Users\smara\Documents\Progetti Antigravity\Entrata automatica mensile\web\`
2. Fai doppio clic su `index.html` per aprirlo in Google Chrome o Microsoft Edge.
3. L'applicazione è **immediatamente funzionante**:
   - Inserisci una multa di test;
   - Clicca su **Verifica Conformità Istantanea** per vedere il calcolo della probabilità di annullamento (es. 85%) e l'elenco dei vizi riscontrati;
   - Clicca su **Genera e Scarica Ricorso Ufficiale** per vedere il documento legale formale già compilato con tutti gli articoli di legge e pronto per la stampa/PDF!

### Metodo 2: Esecuzione tramite Server Python
Se desideri avviare il backend API locale:
```bash
python web/server.py 8080
```
E collegati dal browser a: `http://localhost:8080`

---

## 📁 Struttura del Progetto

```
Entrata automatica mensile/
├── data/
│   └── dispositivi_autovelox.json   # Database modelli autovelox, decreti e stato omologazione
├── core/
│   ├── analyzer.py                  # Motore di calcolo e rilevazione vizi giuridici
│   └── document_generator.py        # Generatore del testo formale e HTML per la stampa
├── web/
│   ├── index.html                   # Interfaccia grafica completa, reattiva con Tailwind CSS
│   └── server.py                    # Server web standalone in pura libreria standard Python
├── test_core.py                     # Suite di test unitari automatici
└── README.md                        # Documentazione del progetto
```

---

## 💰 Come Funziona la Monetizzazione Automatica

1. **Acquisizione Traffico a Costo Zero (Programmatic SEO)**:
   - Le persone cercano su Google: *"Multa autovelox [Comune]"*, *"Autovelox 106 omologato o approvato"*, *"Ricorso multa prefetto fac simile"*.
   - Atterrano su VeloxCheck ed eseguono il **test gratuito in 30 secondi**.
2. **Conversione d'Impulso (Prezzo: 9,90€ anziché 80€ di un avvocato)**:
   - Il test mostra che il dispositivo non è omologato e che il ricorso ha un'elevata probabilità di successo.
   - L'utente paga 9,90€ tramite Stripe (Apple Pay, Google Pay o Carta).
3. **Erogazione 100% Automatica**:
   - Il software genera istantaneamente il **Ricorso Ufficiale al Prefetto** in formato A4 perfetto per il salvataggio in PDF.
   - Fornisce la guida passo-passo per spedirlo tramite **PEC gratuita** in 2 minuti, risparmiando i 43€ di tasse del Giudice di Pace.
4. **Incasso Diretto**:
   - I soldi arrivano direttamente sul tuo conto Stripe senza alcun intervento manuale da parte tua.

---

## 🌐 Messa Online a Costo Zero (0€/Mese per Sempre)

Puoi pubblicare questa web app online gratuitamente in 2 minuti:
1. **Cloudflare Pages / Vercel / GitHub Pages**:
   - Carica la cartella `web/` su un repository GitHub;
   - Collega il repository a Vercel o Cloudflare Pages;
   - Il sito sarà live con certificato HTTPS gratuito e traffico illimitato senza spendere 1 euro!
