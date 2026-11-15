"""
Engine di Analisi Giuridica e Verifica Conformità Autovelox
Basato su:
- Cassazione Civile n. 10505/2024 (omologazione vs approvazione)
- Art. 142 c. 6 e Art. 201 Codice della Strada (termini notifica 90gg)
- Sentenza Corte Costituzionale n. 113/2015 (taratura periodica annuale obbligatoria)
- Decreti MIT 305/2025 e 367/2025 (censimento e piattaforma velox.mit.gov.it)
"""

import json
import os
from datetime import datetime, date

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "dispositivi_autovelox.json")

def load_dispositivi():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def analizza_multa(dati: dict) -> dict:
    """
    Analizza i dati del verbale e produce il referto di conformita'
    """
    dispositivi_data = load_dispositivi()
    dispositivi_map = {d["id"]: d for d in dispositivi_data["dispositivi"]}
    
    # Parsing date
    data_infrazione = datetime.strptime(dati["data_infrazione"], "%Y-%m-%d").date()
    data_notifica = datetime.strptime(dati["data_notifica"], "%Y-%m-%d").date()
    oggi = date.today()
    
    # 1. Calcolo giorni notifica (Art. 201 CdS - perentorio 90 giorni)
    giorni_notifica = (data_notifica - data_infrazione).days
    notifica_tardiva = giorni_notifica > 90
    
    # 2. Calcolo termini ricorso (60gg Prefetto, 30gg Giudice di Pace)
    giorni_dalla_notifica = (oggi - data_notifica).days
    giorni_rimasti_prefetto = max(0, 60 - giorni_dalla_notifica)
    giorni_rimasti_giudice_pace = max(0, 30 - giorni_dalla_notifica)
    termini_scaduti = giorni_rimasti_prefetto == 0
    
    # 3. Calcolo tolleranza strumentale (art. 345 Reg. CdS: 5% con minimo 5 km/h)
    limite = float(dati.get("limite_velocita", 50))
    vel_rilevata = float(dati.get("velocita_rilevata", 60))
    riduzione = max(5.0, vel_rilevata * 0.05)
    vel_effettiva = max(0.0, vel_rilevata - riduzione)
    eccesso_netto = round(vel_effettiva - limite, 2)
    
    vizi = []
    punteggio = 0
    
    # Vizio 1: Termini di notifica
    if notifica_tardiva:
        vizi.append({
            "titolo": "Decadenza del potere sanzionatorio per tardiva notifica (Art. 201 C.d.S.)",
            "gravita": "ASSOLUTA",
            "descrizione": f"Il verbale è stato notificato dopo {giorni_notifica} giorni dall'accertamento (limite massimo di legge: 90 giorni). L'obbligazione di pagare la somma è estinta di diritto.",
            "riferimento_legale": "Art. 201, commi 1 e 5 del Codice della Strada."
        })
        punteggio += 45
        
    # Vizio 2: Omologazione vs Approvazione (Cassazione 10505/2024)
    dev_id = dati.get("modello_dispositivo", "altro_dispositivo")
    dispositivo = dispositivi_map.get(dev_id, dispositivi_map["altro_dispositivo"])
    
    if dispositivo["stato_omologazione"] in ["approvato_senza_omologazione", "approvato_sanatoria_discussa", "incerto_onere_prova_pa"]:
        vizi.append({
            "titolo": "Mancata omologazione tecnica dell'apparecchiatura (Ordinanza Cassazione n. 10505/2024)",
            "gravita": "ALTA",
            "descrizione": f"Il dispositivo indicato ({dispositivo['nome']}) risulta privo di formale decreto di omologazione ai sensi dell'art. 142 c. 6 CdS e art. 192 Reg. Esec. CdS, risultando munito unicamente di autorizzazione/approvazione dirigenziale. La Cassazione ha stabilito l'illegittimità dell'accertamento.",
            "riferimento_legale": "Corte di Cassazione Civile, Sez. II, Ordinanza n. 10505 del 18/04/2024 e conformi."
        })
        punteggio += 50
        
    # Vizio 3: Taratura periodica annuale
    taratura_citata = dati.get("taratura_citata", False)
    if not taratura_citata:
        vizi.append({
            "titolo": "Omessa indicazione della verifica periodica di taratura (Corte Cost. n. 113/2015)",
            "gravita": "ALTA",
            "descrizione": "Nel verbale non sono riportati gli estremi del certificato di taratura periodica annuale rilasciato da laboratorio accreditato (ACCREDIA/LAT). L'onere della prova del perfetto funzionamento grava interamente sull'amministrazione.",
            "riferimento_legale": "Corte Costituzionale, Sentenza n. 113 del 18/06/2015 e Cass. Civ. Sez. II n. 533/2018."
        })
        punteggio += 30
    else:
        # Se taratura indicata ma oltre i 365 giorni
        data_taratura_str = dati.get("data_taratura")
        if data_taratura_str:
            try:
                data_taratura = datetime.strptime(data_taratura_str, "%Y-%m-%d").date()
                if (data_infrazione - data_taratura).days > 365:
                    vizi.append({
                        "titolo": "Taratura periodica scaduta alla data dell'accertamento (> 365 giorni)",
                        "gravita": "ALTA",
                        "descrizione": f"La taratura indicata risale a {(data_infrazione - data_taratura).days} giorni prima dell'infrazione, superando il termine massimo di validità annuale.",
                        "riferimento_legale": "Corte Costituzionale n. 113/2015."
                    })
                    punteggio += 30
            except Exception:
                pass
                
    # Vizio 4: Presegnalazione e visibilità
    presenza_cartello = dati.get("presenza_cartello", True)
    if not presenza_cartello:
        vizi.append({
            "titolo": "Carenza di presegnalazione preventiva e visibilità del rilevatore",
            "gravita": "MEDIA",
            "descrizione": "La postazione di controllo non risultava preventivamente segnalata con apposito cartello ad adeguata distanza e chiaramente visibile all'automobilista.",
            "riferimento_legale": "Art. 142 c. 6-bis C.d.S., D.M. MIT n. 282/2017 e Direttiva Maroni."
        })
        punteggio += 15
        
    # Vizio 5: Omessa indicazione matricola
    matricola = str(dati.get("matricola", "")).strip()
    if not matricola or matricola.lower() in ["non indicata", "assente", "non presente"]:
        vizi.append({
            "titolo": "Omessa indicazione del numero di matricola dell'apparecchio nel verbale",
            "gravita": "MEDIA",
            "descrizione": "La mancata indicazione del numero seriale/matricola impedisce la verifica di conformità nella banca dati ministeriale (velox.mit.gov.it), violando il diritto di difesa.",
            "riferimento_legale": "Art. 24 Costituzione e D.M. MIT n. 305/2025."
        })
        punteggio += 15

    # Calcolo percentuale di probabilita' complessiva (cap al 98%)
    probabilita = min(98, max(20, punteggio))
    if notifica_tardiva:
        probabilita = 99
        
    return {
        "dispositivo": dispositivo,
        "giorni_notifica": giorni_notifica,
        "notifica_tardiva": notifica_tardiva,
        "giorni_rimasti_prefetto": giorni_rimasti_prefetto,
        "giorni_rimasti_giudice_pace": giorni_rimasti_giudice_pace,
        "termini_scaduti": termini_scaduti,
        "riduzione_tolleranza": riduzione,
        "velocita_netta": vel_effettiva,
        "eccesso_netto": eccesso_netto,
        "vizi_rilevati": vizi,
        "numero_vizi": len(vizi),
        "probabilita_successo": probabilita,
        "giudizio": "OTTIMO - Elevata probabilità di accoglimento" if probabilita >= 75 else "DISCRETO - Presenti vizi formali" if probabilita >= 50 else "BASSO - Pochi motivi formali"
    }

if __name__ == "__main__":
    # Test rapido
    sample = {
        "data_infrazione": "2026-09-01",
        "data_notifica": "2026-10-15",
        "modello_dispositivo": "autovelox_106",
        "matricola": "SN99281",
        "limite_velocita": 50,
        "velocita_rilevata": 67,
        "taratura_citata": False,
        "presenza_cartello": False
    }
    risultato = analizza_multa(sample)
    print(f"Probabilita' stimata: {risultato['probabilita_successo']}%")
    print(f"Vizi riscontrati: {risultato['numero_vizi']}")
    for v in risultato['vizi_rilevati']:
        print(f" - [{v['gravita']}] {v['titolo']}")
