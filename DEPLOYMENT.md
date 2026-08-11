# 🚀 ShoeStore Production Deployment Guide

This guide provides step-by-step instructions for deploying the **ShoeStore** full-stack e-commerce web application to cloud platforms (Render, Railway, Heroku), Docker, or an Ubuntu VPS.

---

## 📋 Pre-Deployment Checklist

- [x] Production WSGI server (`gunicorn`) installed in `requirements.txt`.
- [x] Platform startup script (`Procfile`) defined (`web: gunicorn run:app`).
- [x] Python version runtime specified (`runtime.txt` -> `python-3.11.9`).
- [x] Database migration repository generated (`migrations/`).
- [x] Dockerfile & Docker Compose defined (`Dockerfile`, `docker-compose.yml`).
- [x] Environment configuration template ready (`.env.example`).
- [x] Automated test suite passing (`12 passed in 3.67s`).

---

## Option 1: Deploy to Render.com (Recommended Free/Easy Cloud Hosting)

1. **Push Code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for production"
   git remote add origin https://github.com/your-username/shoe-store.git
   git push -u origin main
   ```

2. **Create New Web Service on Render**:
   - Log into [Render Dashboard](https://dashboard.render.com/).
   - Click **New +** &rarr; **Web Service**.
   - Connect your GitHub repository `shoe-store`.

3. **Configure Settings**:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt && python seed.py`
   - **Start Command**: `gunicorn run:app`

4. **Environment Variables**:
   Add the following under **Environment**:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: `your-secure-random-key-here`
   - `DATABASE_URL`: (Connect a Render PostgreSQL database if desired)

5. **Deploy**: Render will automatically build the container and issue a live SSL `https://shoestore.onrender.com` URL!

---

## Option 2: Deploy using Docker Compose (Self-Hosted / VPS)

Run the entire full-stack application with a PostgreSQL database with a single command:

```bash
docker-compose up -d --build
```

- **Web Container**: Listening on port `5000`.
- **PostgreSQL Database**: Listening on port `5432`.
- Automatic database seeding and table creation on first run.

---

## Option 3: Deploy to Railway.app

1. Install Railway CLI or connect via Web GUI.
2. Run:
   ```bash
   railway up
   ```
3. Add a PostgreSQL plugin inside Railway Dashboard and link the `DATABASE_URL` variable.

---

## Option 4: Deploy to Heroku

1. Login via Heroku CLI:
   ```bash
   heroku login
   heroku create shoestore-app
   heroku addons:create heroku-postgresql:mini
   ```
2. Set Environment Variables:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=$(openssl rand -hex 32)
   ```
3. Push to Deploy:
   ```bash
   git push heroku main
   heroku run python seed.py
   ```

---

## Option 5: Manual Ubuntu VPS Setup (NGINX + Gunicorn + Systemd)

1. **Install Dependencies**:
   ```bash
   sudo apt update && sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y
   ```

2. **Clone & Setup Environment**:
   ```bash
   cd /var/www
   git clone https://github.com/your-username/shoe-store.git
   cd shoe-store
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python seed.py
   ```

3. **Create Systemd Service (`/etc/systemd/system/shoestore.service`)**:
   ```ini
   [Unit]
   Description=Gunicorn instance to serve ShoeStore
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/shoe-store
   Environment="PATH=/var/www/shoe-store/venv/bin"
   Environment="FLASK_ENV=production"
   ExecStart=/var/www/shoe-store/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 run:app

   [Install]
   WantedBy=multi-user.target
   ```

4. **Start Service & NGINX Proxy**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start shoestore
   sudo systemctl enable shoestore
   sudo systemctl restart nginx
   ```

---

## ⚡ Quick Deployment Command

To verify production build locally with Gunicorn before deploying:

```bash
gunicorn --bind 0.0.0.0:5000 run:app
```
