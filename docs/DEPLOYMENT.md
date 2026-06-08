# Deployment Guide

## Fly.io (Recommended)

### Prerequisites
- GitHub account
- Fly.io account ([fly.io](https://fly.io) — free tier works)

### CLI Deploy

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch (uses existing fly.toml)
fly launch

# Deploy
fly deploy
```

### Dashboard Deploy

1. Go to [fly.io/apps](https://fly.io/apps)
2. Click **Create App**
3. Import `SolimanAnas/islamic-api`
4. **Branch:** `main`
5. **Region:** Choose closest to your users (e.g., `ams` for Europe, `iad` for US East)
6. **VM:** Shared CPU, 512MB RAM
7. Click **Deploy**

### Configuration

The `fly.toml` is pre-configured:

```toml
app = "islamic-api"
primary_region = "ams"

[build]

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1

[[vm]]
  memory = "512mb"
  cpu_kind = "shared"
  cpus = 1
```

### Cost
- **Free allowance:** 3 shared-cpu-1x VMs, 256MB RAM, 160GB bandwidth/month
- **Your usage:** 1 VM, 512MB RAM → ~$0-2/month (within free allowance)
- **Always-on:** `min_machines_running = 1` ensures no cold starts

### Custom Domain

```bash
fly certs add yourdomain.com
fly ips allocate-v4
```

### Useful Commands

```bash
fly status          # Check app status
fly logs            # View live logs
fly restart         # Restart the app
fly ssh console     # SSH into the VM
fly deploy          # Redeploy after changes
```

---

## Railway

### Steps

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add Python environment
railway add --plugin python

# Deploy
railway up

# Get the URL
railway open
```

### Cost
- $5/month for always-on (no sleep)
- 500 hours/month included

---

## Render

### Steps

1. Go to [render.com](https://render.com)
2. Click **New Web Service**
3. Connect your GitHub repo
4. Configure:
   - **Name:** `islamic-api`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click **Deploy**

### Cost
- **Free tier:** 750 hours/month, sleeps after 15min inactivity
- **Starter ($7/month):** Always-on, no sleep

---

## Docker (Self-hosted)

### Build and run

```bash
# Build
docker build -t islamic-api .

# Run
docker run -d -p 8000:8000 --name islamic-api islamic-api

# Check logs
docker logs islamic-api
```

### With docker-compose

```bash
docker-compose up --build -d
```

---

## DigitalOcean VPS

### Steps

1. Create a $6/month droplet (Ubuntu 22.04)
2. SSH into the server
3. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```
4. Clone and deploy:
   ```bash
   git clone https://github.com/SolimanAnas/islamic-api.git
   cd islamic-api
   docker-compose up -d
   ```

### Add Nginx reverse proxy (optional)

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `DEBUG` | `false` | Enable debug mode |
| `CORS_ORIGINS` | `["*"]` | Allowed origins |
| `RATE_LIMIT` | `100` | Requests per window |
| `RATE_LIMIT_WINDOW` | `60` | Window in seconds |

---

## Performance Tips

1. **Data is loaded into memory at startup** — first request is instant
2. **Search is in-memory** — fast for <100k items
3. **Tafsir uses SQLite** — query on demand, not loaded into memory
4. **Add caching headers** — for CDN caching of static data
5. **Use pagination** — don't return all results at once

---

## Monitoring

### Health check

```bash
curl https://your-api.com/health
# {"status": "ok", "version": "1.0.0"}
```

### API info

```bash
curl https://your-api.com/v1
# Returns endpoint list and dataset statistics
```
