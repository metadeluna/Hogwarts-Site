#!/usr/bin/env python3
"""
Servidor HTTP local para Hogwarts RPG
Serve o site na porta 8000 para testes
"""

import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

PORT = 8000
HANDLER = http.server.SimpleHTTPRequestHandler

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Previne cache para desenvolvimento
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # Log mais limpo
        if args[1] == 200:
            print(f"✓ {args[0]}")
        else:
            print(f"✗ {format % args}")

def main():
    # Mudar para o diretório do site
    site_dir = Path(__file__).parent
    os.chdir(site_dir)
    
    print("=" * 70)
    print("🧙‍♂️  HOGWARTS RPG - Servidor Local")
    print("=" * 70)
    print(f"📁 Diretório: {site_dir}")
    print(f"🌐 URL:      http://localhost:{PORT}")
    print(f"📄 Página:   http://localhost:{PORT}/ficha.html")
    print("=" * 70)
    print()
    
    # Verificar se config.public.js tem a chave ANON
    config_file = site_dir / "js" / "config.public.js"
    if config_file.exists():
        with open(config_file, 'r') as f:
            content = f.read()
            if "sua_anon_key_aqui" in content or "eyJ" not in content:
                print("⚠️  AVISO: A SUPABASE_ANON_KEY ainda não foi preenchida em js/config.public.js")
                print("   Você deve adicionar sua chave anon do Supabase antes de testar!")
                print()
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"✅ Servidor iniciado em http://localhost:{PORT}")
            print("   Pressione Ctrl+C para parar")
            print()
            
            # Tentar abrir o navegador automaticamente (opcional)
            try:
                webbrowser.open(f"http://localhost:{PORT}/index.html")
                print("🌐 Abrindo navegador...")
            except:
                pass
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n⛔ Servidor parado.")
        sys.exit(0)
    except OSError as e:
        print(f"\n❌ Erro: {e}")
        if e.errno == 48 or e.errno == 98:  # Port already in use
            print(f"   A porta {PORT} já está em uso. Tente outra porta ou feche o processo.")
        sys.exit(1)

if __name__ == "__main__":
    main()
