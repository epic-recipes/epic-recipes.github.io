#!/usr/bin/env python3
"""
Servidor HTTPS local para testing de PWA
Uso: python server_https.py
"""
import http.server
import ssl
import os
import sys
import socket
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()
os.chdir(BASE_DIR)

PORT = 8443
HOST = '127.0.0.1'

class PWAHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Service-Worker-Allowed', '/')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def create_self_signed_cert():
    """Crear certificado autofirmado para localhost"""
    cert_file = BASE_DIR / 'cert.pem'
    key_file = BASE_DIR / 'key.pem'
    
    if cert_file.exists() and key_file.exists():
        print("✓ Certificado existente encontrado")
        return str(cert_file), str(key_file)
    
    print("🔐 Generando certificado autofirmado...")
    
    # Intentar con openssl
    try:
        cmd = f'openssl req -x509 -newkey rsa:2048 -keyout {key_file} -out {cert_file} -days 365 -nodes -subj "/CN=localhost"'
        result = os.system(cmd)
        if result == 0 and cert_file.exists():
            print("✓ Certificado generado exitosamente")
            return str(cert_file), str(key_file)
    except Exception as e:
        print(f"⚠ Error con openssl: {e}")
    
    # Alternativa con cryptography si está disponible
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        from datetime import datetime, timedelta
        
        print("Usando librería cryptography...")
        
        # Generar clave privada
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Crear certificado
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
            critical=False,
        ).sign(private_key, hashes.SHA256(), default_backend())
        
        # Guardar clave privada
        with open(key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Guardar certificado
        with open(cert_file, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        print("✓ Certificado generado con cryptography")
        return str(cert_file), str(key_file)
        
    except ImportError:
        print("⚠ cryptography no instalado")
        pass
    
    print("❌ No se pudo generar certificado autofirmado")
    print("   Instala: pip install cryptography")
    print("   O instala OpenSSL: https://slproweb.com/products/Win32OpenSSL.html")
    sys.exit(1)

def main():
    cert_file, key_file = create_self_signed_cert()
    
    server = http.server.HTTPServer((HOST, PORT), PWAHTTPHandler)
    
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        server.socket = context.wrap_socket(server.socket, server_side=True)
    except Exception as e:
        print(f"❌ Error al cargar certificado: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("🚀 SERVIDOR HTTPS LOCAL PARA TESTING PWA")
    print("=" * 70)
    print(f"")
    print(f"  🌐 URL: https://127.0.0.1:{PORT}")
    print(f"  📁 Directorio: {BASE_DIR}")
    print(f"")
    print(f"  ⚠️  IMPORTANTE:")
    print(f"     1. Acepta el certificado autofirmado en el navegador")
    print(f"     2. El navegador puede mostrar advertencia de seguridad")
    print(f"     3. Haz clic en 'Proceder de todas formas' o similar")
    print(f"")
    print(f"  🧪 TESTING PWA:")
    print(f"     1. Abre https://127.0.0.1:{PORT} en Chrome/Edge")
    print(f"     2. Abre DevTools (F12)")
    print(f"     3. Ejecuta en consola: forceShowInstallBanner()")
    print(f"     4. El banner AMARILLO debería aparecer en la parte superior")
    print(f"")
    print(f"  ⌨️  Para salir: Ctrl+C")
    print("=" * 70 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido correctamente")
        sys.exit(0)

if __name__ == '__main__':
    main()

