import urllib.request
import time
import subprocess
import sys
import json

def test_full_flow():
    # Avvia server in background
    proc = subprocess.Popen([sys.executable, 'web/server.py', '8080'])
    time.sleep(1.5)

    try:
        # 1. Test GET /api/dispositivi
        req = urllib.request.urlopen('http://localhost:8080/api/dispositivi')
        dispositivi = json.loads(req.read().decode('utf-8'))
        print(f"Dispositivi caricati con successo: {len(dispositivi['dispositivi'])} modelli censiti")

        # 2. Test POST /api/analizza
        sample = {
            'data_infrazione': '2026-09-01',
            'data_notifica': '2026-10-10',
            'modello_dispositivo': 'autovelox_106',
            'matricola': 'SN99281',
            'limite_velocita': 50,
            'velocita_rilevata': 68,
            'taratura_citata': False,
            'presenza_cartello': False
        }
        req2 = urllib.request.Request(
            'http://localhost:8080/api/analizza',
            data=json.dumps(sample).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        res2 = urllib.request.urlopen(req2)
        analisi = json.loads(res2.read().decode('utf-8'))
        print(f"Analisi completata: Probabilita' di annullamento {analisi['probabilita_successo']}%, Vizi rilevati: {analisi['numero_vizi']}")

        # 3. Test POST /api/genera-documento
        sample_doc = {
            'multa': sample,
            'utente': {
                'nome_cognome': 'Mario Rossi',
                'codice_fiscale': 'RSSMRA80A01H501Z',
                'targa': 'AB123CD',
                'residenza': 'Via Roma 1, Roma',
                'provincia_prefettura': 'ROMA',
                'pec_email': 'mario.rossi@pec.it'
            }
        }
        req3 = urllib.request.Request(
            'http://localhost:8080/api/genera-documento',
            data=json.dumps(sample_doc).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        res3 = urllib.request.urlopen(req3)
        doc_res = json.loads(res3.read().decode('utf-8'))
        print(f"Generazione documento ricorso completata: {len(doc_res['html'])} caratteri HTML generati")
        print("\n>>> TUTTI I TEST HANNO AVUTO ESITO POSITIVO AL 100%! <<<")

    finally:
        proc.terminate()

if __name__ == "__main__":
    test_full_flow()
