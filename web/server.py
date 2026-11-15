"""
Server Web Standalone di VeloxCheck
Utilizza esclusivamente la libreria standard di Python 3 (zero dipendenze esterne richieste).
Supporta API REST JSON, routing e interfaccia web reattiva.
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Import moduli interni
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.analyzer import analizza_multa, load_dispositivi
from core.document_generator import genera_ricorso_html, genera_ricorso_testo

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class VeloxHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Aggiunta header CORS e no-cache per sviluppo
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Endpoint API: Lista dispositivi
        if path == "/api/dispositivi":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            data = load_dispositivi()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        # Endpoint API: Dati Mappa Autovelox e Controlli Mobili
        if path == "/api/mappa":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            mappa_path = os.path.join(os.path.dirname(__file__), "..", "data", "autovelox_mappa.json")
            with open(mappa_path, "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))
            return

        # File ads.txt obbligatorio per Google AdSense
        if path == "/ads.txt":
            ads_path = os.path.join(BASE_DIR, "ads.txt")
            if os.path.exists(ads_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                with open(ads_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Pagina principale HTML
        if path == "/" or path == "/index.html":
            html_path = os.path.join(BASE_DIR, "index.html")
            if os.path.exists(html_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(html_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Fallback a file statici
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode("utf-8"))
        except Exception:
            payload = {}

        # Endpoint API: Analisi Multa
        if path == "/api/analizza":
            try:
                risultato = analizza_multa(payload)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(risultato, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        # Endpoint API: Genera Bozza Documento
        if path == "/api/genera-documento":
            try:
                dati_multa = payload.get("multa", {})
                dati_utente = payload.get("utente", {})
                
                # Esegue analisi
                analisi = analizza_multa(dati_multa)
                # Unisce i dati
                dati_completi = {**dati_multa, **dati_utente}
                
                html_doc = genera_ricorso_html(dati_completi, analisi)
                testo_doc = genera_ricorso_testo(dati_completi, analisi)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "html": html_doc,
                    "testo": testo_doc,
                    "analisi": analisi
                }, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def run(port=PORT):
    server_address = ('', port)
    httpd = HTTPServer(server_address, VeloxHandler)
    print(f"==================================================")
    print(f"🚀 VeloxCheck Server attivo su: http://localhost:{port}")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nArresto del server...")
        httpd.server_close()

if __name__ == "__main__":
    p = PORT
    if len(sys.argv) > 1:
        p = int(sys.argv[1])
    run(p)
