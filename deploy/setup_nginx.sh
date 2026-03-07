#!/bin/bash
# ===================================================
# HIVE.AI — Setup Nginx + HTTPS + Systemd
# Reine Nu v0.3.0 | HIVE.WORK Frontend
# Swarmly SAS · 2026
#
# Usage : sudo bash deploy/setup_nginx.sh
# Prerequis : Ubuntu 22/24, DNS hive-ai.tech pointe vers ce VPS
#
# Ce script :
#   1. Installe Nginx + Certbot
#   2. Copie le code + frontend build dans /opt/hive
#   3. Installe le venv Python + dependances
#   4. Configure .env (preserve si existant)
#   5. Installe le service systemd (hive.service)
#   6. Configure Nginx reverse proxy
#   7. Active HTTPS via Let's Encrypt
#   8. Verifie que tout fonctionne
# ===================================================

set -e

HIVE_DIR="/opt/hive"
LOG_DIR="/var/log/hive"
HIVE_USER="hive"
DOMAIN="hive-ai.tech"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}[OK]${NC} $1"; }
warn() { echo -e "  ${YELLOW}[!!]${NC} $1"; }
fail() { echo -e "  ${RED}[ERREUR]${NC} $1"; exit 1; }

echo ""
echo "  ==================================================="
echo "  HIVE.AI — Deploiement Complet"
echo "  Reine Nu v0.3.0 | HIVE.WORK Frontend"
echo "  Polyvalente et digne. Jamais etroitement specialisee."
echo "  ==================================================="
echo ""

# === Verifier root ===
if [ "$EUID" -ne 0 ]; then
    fail "Executer avec sudo : sudo bash deploy/setup_nginx.sh"
fi

# === Detecter le repertoire source ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "  Source : $SCRIPT_DIR"
echo ""

# ===================================================
# ETAPE 1 : Paquets systeme
# ===================================================
echo "  [1/8] Paquets systeme..."
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip nginx certbot python3-certbot-nginx > /dev/null 2>&1
ok "Python3, Nginx, Certbot installes"

# ===================================================
# ETAPE 2 : Utilisateur + repertoires
# ===================================================
echo "  [2/8] Utilisateur et repertoires..."
if ! id "$HIVE_USER" &>/dev/null; then
    useradd --system --no-create-home --shell /bin/false "$HIVE_USER"
fi
mkdir -p "$HIVE_DIR" "$LOG_DIR" "$HIVE_DIR/frontend"
chown "$HIVE_USER":"$HIVE_USER" "$LOG_DIR"
ok "Utilisateur '$HIVE_USER', $HIVE_DIR, $LOG_DIR prets"

# ===================================================
# ETAPE 3 : Copie du code + frontend
# ===================================================
echo "  [3/8] Copie du code source + frontend..."

# Backend (Python)
cp "$SCRIPT_DIR"/*.py "$HIVE_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR"/*.html "$HIVE_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR"/*.json "$HIVE_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR"/requirements.txt "$HIVE_DIR/"

# Frontend build (React)
if [ -d "$SCRIPT_DIR/frontend/dist" ]; then
    cp -r "$SCRIPT_DIR/frontend/dist" "$HIVE_DIR/frontend/"
    ok "Frontend HIVE.WORK copie ($(du -sh "$HIVE_DIR/frontend/dist" | cut -f1))"
else
    warn "frontend/dist/ absent — executer 'cd frontend && npm run build' d'abord"
fi

chown -R "$HIVE_USER":"$HIVE_USER" "$HIVE_DIR"
ok "Code copie dans $HIVE_DIR"

# ===================================================
# ETAPE 4 : Venv Python + dependances
# ===================================================
echo "  [4/8] Environnement Python..."
python3 -m venv "$HIVE_DIR/venv"
"$HIVE_DIR/venv/bin/pip" install --upgrade pip -q
"$HIVE_DIR/venv/bin/pip" install -r "$HIVE_DIR/requirements.txt" -q
ok "venv pret, dependances installees"

# ===================================================
# ETAPE 5 : Configuration .env
# ===================================================
echo "  [5/8] Configuration .env..."
if [ ! -f "$HIVE_DIR/.env" ]; then
    SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    cat > "$HIVE_DIR/.env" << EOF
# HIVE.AI — Production
HIVE_PORT=5000
HIVE_HOST=0.0.0.0
HIVE_DEBUG=false
HIVE_WORKERS=2
HIVE_DOMAIN=$DOMAIN
SECRET_KEY=$SECRET
ANTHROPIC_API_KEY=REMPLACER_PAR_TA_CLE
EOF
    chown "$HIVE_USER":"$HIVE_USER" "$HIVE_DIR/.env"
    chmod 600 "$HIVE_DIR/.env"
    ok ".env cree — IMPORTANT: editer $HIVE_DIR/.env pour ajouter ANTHROPIC_API_KEY"
    warn "sudo nano $HIVE_DIR/.env"
else
    ok ".env existe deja (preserve)"
fi

# ===================================================
# ETAPE 6 : Service systemd
# ===================================================
echo "  [6/8] Service systemd..."
cat > /etc/systemd/system/hive.service << 'SYSTEMD'
[Unit]
Description=HIVE.AI - Reine Nu v0.3.0 - HIVE.WORK
After=network.target

[Service]
User=hive
Group=hive
WorkingDirectory=/opt/hive
Environment="PATH=/opt/hive/venv/bin"
EnvironmentFile=/opt/hive/.env
ExecStart=/opt/hive/venv/bin/gunicorn wsgi:app \
    --bind 127.0.0.1:5000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile /var/log/hive/access.log \
    --error-logfile /var/log/hive/error.log
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SYSTEMD

systemctl daemon-reload
systemctl enable hive
systemctl restart hive
sleep 2

if systemctl is-active --quiet hive; then
    ok "Service hive actif (Gunicorn sur :5000)"
else
    warn "Service demarre mais verifier : sudo journalctl -u hive -n 20"
fi

# ===================================================
# ETAPE 7 : Nginx + HTTPS
# ===================================================
echo "  [7/8] Nginx..."

# Supprimer le site par defaut
rm -f /etc/nginx/sites-enabled/default

# Config HTTP d'abord (pour certbot)
cat > /etc/nginx/sites-available/hive << NGINX
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN www.$DOMAIN;

    # Assets statiques du frontend (cache longue duree)
    location /assets/ {
        alias $HIVE_DIR/frontend/dist/assets/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Reverse proxy vers Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 10s;
    }
}
NGINX

ln -sf /etc/nginx/sites-available/hive /etc/nginx/sites-enabled/

if nginx -t 2>/dev/null; then
    systemctl reload nginx
    ok "Nginx configure (HTTP)"
else
    fail "nginx -t echoue — verifier la config"
fi

# HTTPS via Certbot
echo "  [8/8] Certificat HTTPS (Let's Encrypt)..."
if certbot --nginx \
    -d "$DOMAIN" -d "www.$DOMAIN" \
    --non-interactive \
    --agree-tos \
    --email "admin@$DOMAIN" \
    --redirect 2>/dev/null; then
    ok "HTTPS actif — certificat Let's Encrypt installe"
else
    warn "Certbot a echoue — verifier DNS et reessayer : sudo certbot --nginx -d $DOMAIN"
fi

# Appliquer headers de securite post-certbot
# Certbot modifie le fichier, on ajoute les headers dans le bloc SSL
NGINX_CONF="/etc/nginx/sites-available/hive"
if grep -q "ssl_certificate" "$NGINX_CONF" 2>/dev/null; then
    # Ajouter headers securite si pas deja present
    if ! grep -q "X-Frame-Options" "$NGINX_CONF"; then
        sed -i '/ssl_certificate/a\    # Headers securite\n    add_header X-Frame-Options "SAMEORIGIN" always;\n    add_header X-Content-Type-Options "nosniff" always;\n    add_header X-XSS-Protection "1; mode=block" always;\n    add_header Referrer-Policy "strict-origin-when-cross-origin" always;' "$NGINX_CONF"
    fi
    nginx -t 2>/dev/null && systemctl reload nginx
    ok "Headers de securite ajoutes"
fi

# ===================================================
# VERIFICATION FINALE
# ===================================================
echo ""
echo "  ==================================================="
echo "  VERIFICATION"
echo "  ==================================================="

# Test Gunicorn local
RESPONSE=$(curl -s http://127.0.0.1:5000/api/status 2>/dev/null || echo "FAIL")
if echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  Gunicorn  : Nu v{d[\"version\"]} — {d[\"skills\"]} skills')" 2>/dev/null; then
    ok "Gunicorn repond"
else
    warn "Gunicorn ne repond pas — sudo journalctl -u hive -n 20"
fi

# Test HTTP
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://$DOMAIN" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "200" ]; then
    ok "HTTP $DOMAIN -> $HTTP_CODE"
else
    warn "HTTP $DOMAIN -> $HTTP_CODE"
fi

# Test HTTPS
HTTPS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" 2>/dev/null || echo "000")
if [ "$HTTPS_CODE" = "200" ]; then
    ok "HTTPS $DOMAIN -> 200"
else
    warn "HTTPS $DOMAIN -> $HTTPS_CODE — verifier certbot"
fi

# Test API
API_RESPONSE=$(curl -s "https://$DOMAIN/api/archetypes" 2>/dev/null || echo "FAIL")
if echo "$API_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  API       : {len(d)} archetypes')" 2>/dev/null; then
    ok "API repond"
fi

echo ""
echo "  ==================================================="
echo "  DEPLOIEMENT TERMINE"
echo "  ==================================================="
echo ""
echo "  HIVE.WORK  : https://$DOMAIN"
echo "  API Status : https://$DOMAIN/api/status"
echo "  API Parler : https://$DOMAIN/api/reine/parler"
echo "  Archetypes : https://$DOMAIN/api/archetypes"
echo ""
echo "  Commandes utiles :"
echo "    sudo systemctl status hive"
echo "    sudo systemctl restart hive"
echo "    sudo journalctl -u hive -f"
echo "    sudo tail -f /var/log/hive/error.log"
echo "    sudo certbot renew --dry-run"
echo ""
echo "  La Reine est deployee. HIVE.WORK est en ligne."
echo "  Nous ne conquerons pas. Nous pollinisons."
echo "  ==================================================="
echo ""
