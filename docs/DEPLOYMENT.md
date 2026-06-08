# Deployment Guide

## Vercel (Recommended)

### Prerequisites
- GitHub account
- Vercel account (free tier works)

### Steps

1. **Fork the repository**
   ```bash
   # On GitHub, click "Fork" or:
   gh repo fork SolimanAnas/islamic-api
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your forked repo

3. **Configure**
   - Framework Preset: **Other**
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `.`

4. **Deploy**
   - Click "Deploy"
   - Your API is live at `https://your-project.vercel.app`

### Limitations
- 100 GB bandwidth/month (free tier)
- 10 second function timeout (free tier)
- 50 MB max serverless function size

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

## Fly.io

### Steps

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch (creates fly.toml)
fly launch

# Deploy
fly deploy

# Check status
fly status
```

### Free Tier
- 256 MB RAM
- 3 GB storage
- Shared CPU

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
