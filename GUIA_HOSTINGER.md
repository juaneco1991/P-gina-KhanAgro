# Publicar KhanAgro en Hostinger paso a paso

Hostinger actualmente ejecuta aplicaciones Flask en sus planes **VPS** (no en Web Hosting ni Cloud Hosting). Para este proyecto, elige un VPS Linux, por ejemplo Ubuntu 24.04. La guía oficial de Hostinger usa Flask + Gunicorn + Nginx.

## 1. Crear y preparar el VPS

1. Compra o crea un VPS Linux desde hPanel.
2. Asigna o conecta tu dominio al VPS. En hPanel, entra en **Domains** para modificar la zona DNS; apunta los registros `A` de `@` y `www` a la IP pública de tu VPS.
3. Espera la propagación DNS antes de activar SSL.
4. En hPanel, abre el VPS y copia sus datos de acceso SSH (IP, usuario y contraseña o llave).

## 2. Conectarte desde Windows

Abre PowerShell y reemplaza los valores por los que muestra hPanel:

```powershell
ssh root@IP_DE_TU_VPS
```

La primera vez, acepta la huella de seguridad escribiendo `yes`.

## 3. Instalar el software del servidor

Ya dentro del VPS ejecuta:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx -y
```

## 4. Subir el proyecto

Desde tu computador, en la carpeta de este proyecto, puedes usar `scp`:

```powershell
scp -r app.py wsgi.py requirements.txt templates static root@IP_DE_TU_VPS:/home/root/khanagro
```

> Si la carpeta remota no existe aún, primero entra al servidor y crea `mkdir -p /home/root/khanagro`, luego vuelve a ejecutar el comando. También puedes subir los archivos mediante el administrador de archivos o SFTP.

En el VPS, ve al proyecto y crea su entorno virtual:

```bash
cd /home/root/khanagro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Prueba que Gunicorn pueda iniciar la web:

```bash
./venv/bin/gunicorn --bind 0.0.0.0:8000 wsgi:app
```

Abre temporalmente `http://IP_DE_TU_VPS:8000`. Si funciona, presiona `Ctrl + C` en la terminal.

## 5. Hacer que la web se inicie sola con Gunicorn

Crea el servicio:

```bash
sudo nano /etc/systemd/system/khanagro.service
```

Pega lo siguiente:

```ini
[Unit]
Description=KhanAgro Flask application
After=network.target

[Service]
User=root
WorkingDirectory=/home/root/khanagro
Environment="PATH=/home/root/khanagro/venv/bin"
ExecStart=/home/root/khanagro/venv/bin/gunicorn --workers 3 --bind unix:khanagro.sock -m 007 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Guarda con `Ctrl+O`, confirma y sal con `Ctrl+X`. Activa el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl start khanagro
sudo systemctl enable khanagro
sudo systemctl status khanagro
```

Debe aparecer `active (running)`. Para salir de esa pantalla pulsa `q`.

## 6. Configurar Nginx y el dominio

Crea la configuración:

```bash
sudo nano /etc/nginx/sites-available/khanagro
```

Reemplaza `tudominio.com` por tu dominio real:

```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/root/khanagro/khanagro.sock;
    }
}
```

Actívala y verifica la configuración:

```bash
sudo ln -s /etc/nginx/sites-available/khanagro /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
```

Visita `http://tudominio.com`: ya deberías ver KhanAgro.

## 7. Activar HTTPS (SSL)

Con el DNS ya propagado, instala Certbot y solicita el certificado:

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

Selecciona la opción que redirige automáticamente de HTTP a HTTPS. Verifica luego `https://tudominio.com`.

## Actualizar la página más adelante

1. Sube los archivos modificados a `/home/root/khanagro`.
2. Reinicia la app:

```bash
sudo systemctl restart khanagro
```

3. Si cambiaste la configuración de Nginx, ejecuta además `sudo nginx -t` y `sudo systemctl reload nginx`.

## Si algo falla

```bash
sudo systemctl status khanagro
sudo journalctl -u khanagro -n 50 --no-pager
sudo nginx -t
```

Los dos primeros comandos muestran el error de Flask/Gunicorn; el último detecta problemas de configuración de Nginx.

## Fuentes oficiales

- Hostinger indica que Flask/Python se alojan exclusivamente en VPS: https://support.hostinger.com/en/articles/9791148-is-flask-supported-at-hostinger
- Guía de Hostinger para Flask con Gunicorn y Nginx: https://support.hostinger.com/en/articles/10725412-how-to-install-flask-on-ubuntu-24-04
- Gestión de dominio y hPanel: https://support.hostinger.com/en/articles/1583483-comprehensive-guide-of-hpanel
