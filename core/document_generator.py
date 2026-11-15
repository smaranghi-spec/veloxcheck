"""
Generatore Documentale del Ricorso al Prefetto
Produce il testo giuridico formale e la versione HTML stampabile (perfetta per PDF via browser o stampa)
"""

from datetime import date
from core.analyzer import analizza_multa

def genera_ricorso_testo(dati_utente: dict, analisi: dict) -> str:
    """
    Genera il testo legale del ricorso al Prefetto
    """
    prefettura = dati_utente.get("provincia_prefettura", "ROMA").upper()
    nome = dati_utente.get("nome_cognome", "MARIO ROSSI").upper()
    cf = dati_utente.get("codice_fiscale", "RSSMRA80A01H501Z").upper()
    nato_a = dati_utente.get("luogo_nascita", "Roma")
    nato_il = dati_utente.get("data_nascita", "01/01/1980")
    residenza = dati_utente.get("residenza", "Via Roma 1, 00100 Roma (RM)")
    pec = dati_utente.get("pec_email", "mario.rossi@pec.it")
    telefono = dati_utente.get("telefono", "")
    targa = dati_utente.get("targa", "AB123CD").upper()
    
    num_verbale = dati_utente.get("numero_verbale", "12345/2026")
    data_infrazione = dati_utente.get("data_infrazione", "")
    data_notifica = dati_utente.get("data_notifica", "")
    luogo_infrazione = dati_utente.get("luogo_infrazione", "Via Aurelia km 25")
    ente_accertatore = dati_utente.get("ente_accertatore", "Comando Polizia Locale")
    
    dispositivo = analisi["dispositivo"]
    
    # Costruzione motivi
    motivi_testo = []
    num_motivo = 1
    
    if analisi.get("notifica_tardiva"):
        motivi_testo.append(f"""
{num_motivo}. ESTINZIONE DELL'OBBLIGAZIONE PER DECADENZA DEI TERMINI DI NOTIFICAZIONE EX ART. 201 C.D.S.
Il verbale impugnato fa riferimento a un presunto accertamento avvenuto in data {data_infrazione}, mentre la notifica risulta perfezionata in data {data_notifica}, ossia decorsi {analisi['giorni_notifica']} giorni.
L'art. 201, commi 1 e 5 del Codice della Strada fissa in 90 giorni il termine perentorio entro cui la Pubblica Amministrazione ha l'onere di notificare il verbale, a pena di totale estinzione dell'obbligazione di pagare la somma dovuta. Il decorso del termine perentorio consuma integralmente il potere sanzionatorio dell'Amministrazione, rendendo l'atto radicalmente nullo.
""")
        num_motivo += 1
        
    motivi_testo.append(f"""
{num_motivo}. NULLITÀ RADICALE DELL'ACCERTAMENTO PER DIFETTO DI OMOLOGAZIONE TECNICA DEL DISPOSITIVO UTILIZZATO (ORDINANZA CASSAZIONE CIVILE SEZ. II N. 10505 DEL 18/04/2024)
L'art. 142, comma 6, del Codice della Strada subordina la legittimità e l'efficacia probatoria dei rilevatori di velocità alla circostanza che essi siano debitamente «omologati».
Nel caso di specie, il dispositivo impiegato per la rilevazione ({dispositivo['nome']}) risulta privo di formale decreto di omologazione, essendo munito - al più - di mera approvazione dirigenziale ministeriale.
Al riguardo, la Suprema Corte di Cassazione, con la fondamentale Ordinanza n. 10505/2024 (e successive sentenze conformi), ha chiarito in modo inequivocabile che:
- I procedimenti di 'approvazione' e 'omologazione' sono strutturalmente e giuridicamente distinti ex art. 192 Reg. Esec. C.d.S.;
- La sola approvazione del prototipo non soddisfa i requisiti di rigorosa sperimentazione e collaudo metrologico prescritti dalla legge primaria;
- L'assenza di regolare omologazione comporta l'inidoneità dell'apparecchiatura a fungere da fonte di prova legale e determina la nullità insanabile del verbale sanzionatorio.
Né può assumere rilievo alcuna circolare interna o prassi amministrativa di presunta equiparazione, essendo queste gerarchicamente subordinate alla legge ordinaria dello Stato.
""")
    num_motivo += 1

    if not dati_utente.get("taratura_citata", False):
        motivi_testo.append(f"""
{num_motivo}. MANCATA PROVA DELLA TARATURA PERIODICA ANNUALE DELL'APPARECCHIATURA (CORTE COSTITUZIONALE N. 113/2015)
Nel verbale de quo non sono indicati gli estremi del certificato di taratura periodica annuale emesso da un laboratorio accreditato (organismo LAT/ACCREDIA).
La Corte Costituzionale, con la sentenza n. 113/2015, ha dichiarato l'illegittimità costituzionale dell'art. 45 c. 6 C.d.S. nella parte in cui non prevede che tutte le apparecchiature impiegate nell'accertamento dei limiti di velocità debbano essere sottoposte a verifiche periodiche di funzionalità e taratura.
Come costantemente ribadito dalla giurisprudenza di legittimità (Cass. n. 533/2018), a fronte della contestazione dell'automobilista grava interamente sulla Pubblica Amministrazione l'onere probatorio di dimostrare l'avvenuta e valida taratura preventiva dell'apparecchio, non potendosi presumere la conformità del funzionamento in mancanza della prova documentale dell'ultimo controllo annuale.
""")
        num_motivo += 1

    if not dati_utente.get("presenza_cartello", True):
        motivi_testo.append(f"""
{num_motivo}. CARENZA DI PRESEGNALAZIONE E VISIBILITÀ DELLA POSTAZIONE DI CONTROLLO (ART. 142 C. 6-BIS C.D.S. E D.M. MIT N. 282/2017)
L'art. 142, comma 6-bis, del Codice della Strada stabilisce espressamente che le postazioni di controllo sulla rete stradale devono essere preventivamente segnalate e ben visibili mediante l'impiego di cartelli o dispositivi di segnalazione luminosi.
Nel caso in esame, la postazione non risultava adeguatamente presegnalata nel rispetto delle distanze minime di legge (almeno 1.000 metri su strade extraurbane), né posizionata in modo da garantire la tempestiva visibilità agli utenti della strada, configurando violazione del principio di trasparenza e leale cooperazione tra cittadino e P.A.
""")
        num_motivo += 1

    motivi_completi = "\n".join(motivi_testo)

    testo = f"""
ALL'ECCELLENTISSIMO SIGNOR PREFETTO
DELLA PROVINCIA DI {prefettura}
(inoltrato a mezzo PEC / Raccomandata A.R. tramite {ente_accertatore})

OGGETTO: RICORSO AMMINISTRATIVO AI SENSI DEGLI ARTT. 203 E 204 DEL CODICE DELLA STRADA
AVVERSO IL VERBALE DI CONTESTAZIONE N. {num_verbale} ELEVATO IN DATA {data_infrazione}
DA: {ente_accertatore}

* * *

Il/La sottoscritto/a:
Nome e Cognome: {nome}
Codice Fiscale: {cf}
Nato/a a: {nato_a} il {nato_il}
Residente in: {residenza}
Recapito PEC: {pec}
Telefono: {telefono}
in qualità di proprietario / conducente del veicolo targato {targa},

PREMESSO CHE

1. In data {data_notifica}, veniva notificato all'esponente il verbale di contestazione n. {num_verbale}, redatto da {ente_accertatore}, per la presunta violazione dell'art. 142 del Codice della Strada (superamento del limite di velocità);
2. L'accertamento risulta essere stato effettuato in data {data_infrazione} alle ore presunte, in località {luogo_infrazione}, mediante l'utilizzo dell'apparecchiatura denominata '{dispositivo['nome']}' (Matricola: {dati_utente.get('matricola', 'Non specificata')});
3. Il verbale in oggetto risulta viziato da molteplici e insanabili profili di illegittimità formale e sostanziale, tali da renderlo nullo o comunque annullabile, per i seguenti

MOTIVI DI GRAVAME

{motivi_completi}

ISTANZA DI SOSPENSIONE CAUTELARE

Sussistendo evidenti e fondati motivi di illegittimità del verbale impugnato (fumus boni iuris) e ravvisandosi il concreto pericolo di un pregiudizio grave e irreparabile per il ricorrente derivante dall'obbligo di pagamento e dall'eventuale decurtazione dei punti della patente di guida prima della decisione (periculum in mora),
SI CHIEDE
all'Ill.mo Sig. Prefetto di voler disporre, in via cautelare ed immediata, la sospensione dell'esecutività del verbale impugnato ai sensi dell'art. 203, comma 1-bis del Codice della Strada.

PER QUESTI MOTIVI (P.Q.M.)

Il/La sottoscritto/a {nome}, come sopra generalizzato/a, confida nell'accoglimento del presente ricorso e
CHIEDE
che l'Eccellentissimo Signor Prefetto adito, accertati i vizi sopra esposti:
1. IN VIA PRINCIPALE: ANNULLARE il verbale di accertamento n. {num_verbale} emesso da {ente_accertatore}, disponendo l'archiviazione di tutti gli atti del procedimento senza applicazione di sanzione pecuniaria alcuna né decurtazione dei punti della patente di guida;
2. IN VIA SUBORDINATA: Qualora il Prefetto non ritenga di accogliere immediatamente il ricorso allo stato degli atti, si formula espressa richiesta di AUDIZIONE PERSONALE ai sensi dell'art. 203, comma 1-ter C.d.S., con espresso avvertimento che la mancata audizione comporterà la nullità della successiva eventuale ordinanza-ingiunzione.

Si allegano in copia:
1. Copia del verbale impugnato n. {num_verbale};
2. Copia della ricevuta di notificazione / plico raccomandato o ricevuta telematica PEC;
3. Copia di un documento di identità in corso di validità del ricorrente.

Luogo e Data: {nato_a}, {date.today().strftime('%d/%m/%Y')}

Firma del Ricorrente:

________________________________________
({nome})
"""
    return testo


def genera_ricorso_html(dati_utente: dict, analisi: dict) -> str:
    """
    Genera il documento impaginato in HTML pronto per la stampa o PDF vettoriale
    """
    testo_formattato = genera_ricorso_testo(dati_utente, analisi)
    
    # Conversione in paragrafi HTML puliti
    righe = testo_formattato.strip().split("\n")
    html_lines = []
    for r in righe:
        r_strip = r.strip()
        if not r_strip:
            html_lines.append("<br/>")
        elif r_strip.startswith("ALL'ECCELLENTISSIMO") or r_strip.startswith("DELLA PROVINCIA"):
            html_lines.append(f"<h3 style='margin: 2px 0; text-align: center; font-weight: bold;'>{r_strip}</h3>")
        elif r_strip.startswith("OGGETTO:") or r_strip.startswith("PREMESSO CHE") or r_strip.startswith("MOTIVI DI GRAVAME") or r_strip.startswith("ISTANZA DI SOSPENSIONE") or r_strip.startswith("PER QUESTI MOTIVI"):
            html_lines.append(f"<h4 style='margin-top: 18px; margin-bottom: 6px; font-weight: bold; text-decoration: underline;'>{r_strip}</h4>")
        elif r_strip.startswith("1. ") or r_strip.startswith("2. ") or r_strip.startswith("3. ") or r_strip.startswith("4. ") or r_strip.startswith("5. "):
            html_lines.append(f"<h5 style='margin-top: 14px; margin-bottom: 4px; font-weight: bold;'>{r_strip}</h5>")
        elif r_strip == "* * *":
            html_lines.append("<hr style='border: 0; border-top: 1px solid #ccc; margin: 15px 0;'/>")
        else:
            html_lines.append(f"<p style='margin: 4px 0; text-align: justify; line-height: 1.5;'>{r_strip}</p>")
            
    corpo = "\n".join(html_lines)
    
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<title>Ricorso al Prefetto - Verbale {dati_utente.get('numero_verbale', '')}</title>
<style>
  @page {{
    size: A4;
    margin: 20mm;
  }}
  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 11pt;
    color: #111;
    background: #fff;
    margin: 0;
    padding: 20px;
  }}
  .no-print {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 12px 20px;
    margin-bottom: 25px;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: system-ui, sans-serif;
  }}
  .btn-print {{
    background: #0284c7;
    color: white;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    border: none;
  }}
  @media print {{
    .no-print {{
      display: none !important;
    }}
    body {{
      padding: 0;
    }}
  }}
</style>
</head>
<body>
<div class="no-print">
  <div>
    <strong>Documento Ufficiale Generato da VeloxCheck</strong> &bull; Conforme alle sentenze della Cassazione Civile 2024
  </div>
  <div>
    <button class="btn-print" onclick="window.print()">Stampa / Salva in PDF</button>
  </div>
</div>
<div class="documento">
  {corpo}
</div>
</body>
</html>
"""
    return html
