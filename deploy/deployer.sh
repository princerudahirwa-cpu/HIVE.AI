#!/bin/bash
# ===================================================
# HIVE.AI — Deploiement sur VPS Hostinger
# Reine Nu v0.2.0 | 20 Skills Souverains
# Swarmly SAS · 2026
#
# Usage : sudo bash deploy/deployer.sh
# Prerequis : Ubuntu 22/24, acces root, DNS pointe
# ===================================================

set -e

HIVE_DIR="/opt/hive"
LOG_DIR="/var/log/hive"
HIVE_USER="hive"
DOMAIN="hive-ai.tech"

echo ""
echo "  ==================================================="
echo "  HIVE.AI — Deploiement de la Reine Nu"
echo "  Polyvalente et digne. Jamais etroitement specialisee."
echo "  ==================================================="
echo ""

# Verifier root
if [ "$EUID" -ne 0 ]; then
    echo "  ERREUR : Executer avec sudo"
    exit 1
fi

# ===================================================
# ETAPE 1 : Paquets systeme
# ===================================================
echo "  [1/9] Installation des paquets systeme..."
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip nginx certbot python3-certbot-nginx > /dev/null
echo "  OK — Python3, Nginx, Certbot installes"

# ===================================================
# ETAPE 2 : Utilisateur hive
# ===================================================
echo "  [2/9] Creation de l'utilisateur hive..."
if id "$HIVE_USER" &>/dev/null; then
    echo "  OK — Utilisateur '$HIVE_USER' existe deja"
else
    useradd --system --no-create-home --shell /bin/false "$HIVE_USER"
    echo "  OK — Utilisateur '$HIVE_USER' cree"
fi

# ===================================================
# ETAPE 3 : Repertoires
# ===================================================
echo "  [3/9] Creation des repertoires..."
mkdir -p "$HIVE_DIR"
mkdir -p "$LOG_DIR"
chown "$HIVE_USER":"$HIVE_USER" "$LOG_DIR"
echo "  OK — $HIVE_DIR et $LOG_DIR prets"

# ===================================================
# ETAPE 4 : Copie du code
# ===================================================
echo "  [4/9] Copie du code source..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Copier tous les fichiers Python + HTML + JSON + configs
cp "$SCRIPT_DIR"/*.py "$HIVE_DIR/"
cp "$SCRIPT_DIR"/*.html "$HIVE_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR"/*.json "$HIVE_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR"/requirements.txt "$HIVE_DIR/"

# Permissions
chown -R "$HIVE_USER":"$HIVE_USER" "$HIVE_DIR"
echo "  OK — Code copie dans $HIVE_DIR"

# ===================================================
# ETAPE 5 : Environnement Python
# ===================================================
echo "  [5/9] Creation du venv Python..."
python3 -m venv "$HIVE_DIR/venv"
"$HIVE_DIR/venv/bin/pip" install --upgrade pip -q
"$HIVE_DIR/venv/bin/pip" install -r "$HIVE_DIR/requirements.txt" -q
echo "  OK — venv pret, dependances installees"

# ===================================================
# ETAPE 6 : Configuration .env
# ===================================================
echo "  [6/9] Configuration .env..."
if [ ! -f "$HIVE_DIR/.env" ]; then
    SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    cat > "$HIVE_DIR/.env" << EOF
# HIVE.AI — Variables d'environnement (production)
HIVE_PORT=5000
HIVE_HOST=0.0.0.0
HIVE_DEBUG=false
HIVE_WORKERS=2
HIVE_DOMAIN=$DOMAIN
SECRET_KEY=$SECRET
EOF
    chown "$HIVE_USER":"$HIVE_USER" "$HIVE_DIR/.env"
    chmod 600 "$HIVE_DIR/.env"
    echo "  OK — .env cree avec SECRET_KEY genere"
else
    echo "  OK — .env existe deja (preserve)"
fi

# ===================================================
# ETAPE 7 : Service systemd
# ===================================================
echo "  [7/9] Installation du service systemd..."
cp "$SCRIPT_DIR/deploy/hive.service" /etc/systemd/system/hive.service
systemctl daemon-reload
systemctl enable hive
systemctl start hive
echo "  OK — Service hive demarre"

# Attendre que Gunicorn soit pret
sleep 2
if systemctl is-active --quiet hive; then
    echo "  OK — Gunicorn repond"
else
    echo "  ATTENTION — Le service a demarre mais verifier : sudo journalctl -u hive -n 20"
fi

# ===================================================
# ETAPE 8 : Nginx + HTTPS
# ===================================================
echo "  [8/9] Configuration Nginx..."

# Supprimer le site par defaut si present
rm -f /etc/nginx/sites-enabled/default

# Installer la config Nginx (sans SSL d'abord pour certbot)
cat > /etc/nginx/sites-available/hive << 'NGINX_TEMP'
server {
    listen 80;
    listen [::]:80;
    server_name hive-ai.tech www.hive-ai.tech;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX_TEMP

ln -sf /etc/nginx/sites-available/hive /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
echo "  OK — Nginx configure (HTTP)"

echo "  [9/9] Obtention du certificat HTTPS..."
certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive --agree-tos --email admin@"$DOMAIN" --redirect
echo "  OK — HTTPS actif"

# Remplacer par la config complete avec headers de securite
cp "$SCRIPT_DIR/deploy/nginx-hive.conf" /etc/nginx/sites-available/hive
nginx -t && systemctl reload nginx
echo "  OK — Config Nginx finale avec headers de securite"

# ===================================================
# VERIFICATION
# ===================================================
echo ""
echo "  ==================================================="
echo "  VERIFICATION"
echo "  ==================================================="

# Test local
RESPONSE=$(curl -s http://127.0.0.1:5000/api/status 2>/dev/null || echo "ERREUR")
if echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"  Reine Nu v{d['version']} — {d['reine']['skills']} skills\")" 2>/dev/null; then
    echo "  Gunicorn : OK"
else
    echo "  Gunicorn : VERIFIER — sudo journalctl -u hive -n 20"
fi

# Test HTTPS
HTTPS_RESPONSE=$(curl -s "https://$DOMAIN/api/status" 2>/dev/null || echo "ERREUR")
if echo "$HTTPS_RESPONSE" | python3 -c "import sys,json; json.load(sys.stdin); print('  HTTPS    : OK')" 2>/dev/null; then
    true
else
    echo "  HTTPS    : VERIFIER — curl https://$DOMAIN/api/status"
fi

echo ""
echo "  ==================================================="
echo "  Deploiement termine."
echo ""
echo "  Bureau     : https://$DOMAIN"
echo "  API Status : https://$DOMAIN/api/status"
echo "  API Reine  : https://$DOMAIN/api/reine/etat"
echo "  API Skills : https://$DOMAIN/api/reine/skills"
echo ""
echo "  Commandes utiles :"
echo "    sudo systemctl status hive"
echo "    sudo systemctl restart hive"
echo "    sudo journalctl -u hive -f"
echo "    sudo tail -f /var/log/hive/error.log"
echo ""
echo "  La Reine est deployee."
echo "  On est tous le HIVE."
echo "  ==================================================="
echo ""
