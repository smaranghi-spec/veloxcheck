"""
Test dei moduli core senza necessità di socket di rete
"""
from core.analyzer import analizza_multa, load_dispositivi
from core.document_generator import genera_ricorso_testo, genera_ricorso_html

def test_core():
    # 1. Test database dispositivi
    db = load_dispositivi()
    assert len(db["dispositivi"]) >= 10, "Database dispositivi incompleto"
    print(f"✓ Database dispositivi OK: {len(db['dispositivi'])} modelli censiti")

    # 2. Test caso normale Autovelox 106 non omologato
    multa_sample = {
        "data_infrazione": "2026-10-01",
        "data_notifica": "2026-10-25",
        "modello_dispositivo": "autovelox_106",
        "matricola": "SN-98214",
        "numero_verbale": "28491/2026/PM",
        "ente_accertatore": "Polizia Locale di Roma Capitale",
        "luogo_infrazione": "Via Aurelia km 24+500",
        "limite_velocita": 50,
        "velocita_rilevata": 68,
        "taratura_citata": False,
        "presenza_cartello": True
    }
    analisi = analizza_multa(multa_sample)
    assert analisi["probabilita_successo"] >= 70, "Probabilità attesa non raggiunta"
    assert analisi["numero_vizi"] >= 2, "Vizi non rilevati correttamente"
    print(f"✓ Analisi multa OK: {analisi['probabilita_successo']}% probabilità - {analisi['numero_vizi']} vizi rilevati")

    # 3. Test caso notifica oltre 90 giorni (decadenza assoluta)
    multa_tardiva = dict(multa_sample)
    multa_tardiva["data_infrazione"] = "2026-05-01"
    multa_tardiva["data_notifica"] = "2026-09-15"
    analisi_tardiva = analizza_multa(multa_tardiva)
    assert analisi_tardiva["notifica_tardiva"] is True, "Mancata rilevazione notifica tardiva"
    assert analisi_tardiva["probabilita_successo"] == 99, "Punteggio decadenza non corretto"
    print(f"✓ Rilevazione notifica tardiva (>90gg) OK: {analisi_tardiva['giorni_notifica']} giorni trascorsi")

    # 4. Test generatore documento
    dati_utente = {
        "nome_cognome": "Mario Rossi",
        "codice_fiscale": "RSSMRA80A01H501Z",
        "targa": "AB123CD",
        "residenza": "Via Roma 10, Roma",
        "provincia_prefettura": "ROMA",
        "pec_email": "mario.rossi@pec.it"
    }
    dati_completi = {**multa_sample, **dati_utente}
    testo = genera_ricorso_testo(dati_completi, analisi)
    html = genera_ricorso_html(dati_completi, analisi)

    assert "ALL'ECCELLENTISSIMO SIGNOR PREFETTO" in testo, "Intestazione ricorso assente"
    assert "CASSAZIONE" in testo, "Citazione Cassazione assente"
    assert "MARIO ROSSI" in testo, "Dati ricorrente assenti"
    assert len(html) > 1000, "HTML non valido"
    print(f"✓ Generazione documento ricorso formale OK ({len(testo)} caratteri di testo legale)")
    print("\n=======================================================")
    print(" TUTTI I MODULI CORE DI VELOXCHECK FUNZIONANO AL 100%!")
    print("=======================================================")

if __name__ == "__main__":
    test_core()
