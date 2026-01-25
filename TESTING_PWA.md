# Testing PWA con Servidor HTTPS Local

## ⚠️ ¿Por qué necesito HTTPS?

PWA (Progressive Web Apps) **solo funciona con HTTPS**. En desarrollo local HTTP no permite:
- Evento `beforeinstallprompt`
- Service Workers
- Instalación como app

## 🚀 Iniciar Servidor HTTPS

### Opción 1: Python (Recomendado)

```bash
python server_https.py
```

Esto:
1. Genera un certificado autofirmado (si no existe)
2. Inicia servidor en `https://127.0.0.1:8443`
3. Muestra instrucciones en pantalla

### Opción 2: Node.js (si tienes Node instalado)

```bash
npm install -g http-server
http-server -S
```

### Opción 3: Python sin script

```bash
python -m http.server 8000
```

(Nota: Este NO es HTTPS, solo HTTP)

## 🧪 Testear el Banner PWA

1. **Abre el servidor:**
   ```bash
   python server_https.py
   ```

2. **En el navegador:**
   - Ve a: `https://127.0.0.1:8443`
   - El navegador mostrará advertencia de seguridad
   - Haz clic en "Proceder de todas formas" o similar

3. **En la consola (F12):**
   ```javascript
   forceShowInstallBanner()
   ```

4. **Resultado esperado:**
   - Aparece un banner AMARILLO en la parte superior
   - Tiene botón "Instalar" verde
   - Tiene botón "X" para cerrar (blanco)

## 🔐 Certificado Autofirmado

El script genera automáticamente un certificado autofirmado:
- **Archivo:** `cert.pem` y `key.pem`
- **Válido por:** 365 días
- **Para localhost:** 127.0.0.1

El navegador mostrará advertencia porque no es firmado por autoridad certificada, pero es **seguro para testing local**.

## 📋 Requisitos

### Para Python (Opción 1)
- Python 3.6+
- Opcional: `pip install cryptography` (para mejor generación de certs)

### Para Node.js (Opción 2)
- Node.js instalado
- `npm install -g http-server`

## ❓ Troubleshooting

### "No se puede generar certificado"
```bash
pip install cryptography
```

### "Puerto 8443 ya en uso"
Cambia el puerto en `server_https.py`:
```python
PORT = 9443  # o cualquier otro
```

### "Conexión rechazada"
- Verifica que el servidor está corriendo
- Comprueba la URL: `https://127.0.0.1:8443`
- Acepta el certificado autofirmado en el navegador

## 🎯 Flujo Completo de Testing

1. Terminal:
   ```bash
   cd e:\epic-recipes.github.io
   python server_https.py
   ```

2. Navegador (Chrome/Edge):
   ```
   https://127.0.0.1:8443
   ```

3. Consola del navegador (F12):
   ```javascript
   forceShowInstallBanner()
   ```

4. Deberías ver el banner amarillo ✓

## 📝 Notas

- El certificado se genera una sola vez
- No necesitas regenerarlo cada vez
- El servidor es seguro para testing local
- En producción usa certificados válidos (Let's Encrypt, etc.)

## 🔗 Referencias

- [MDN - Service Workers](https://developer.mozilla.org/es/docs/Web/API/Service_Worker_API)
- [Google - PWA](https://web.dev/progressive-web-apps/)
- [PWA Requirements](https://web.dev/install-criteria/)
