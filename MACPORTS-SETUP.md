# MacPorts + Colima Docker Setup for macOS 13

This guide documents the setup for running Docker via Colima + QEMU on macOS 13 Ventura (or older versions where Docker Desktop is unavailable).

## Prerequisites

- macOS 13 Ventura (x86_64)
- Xcode Command Line Tools installed
- Homebrew already present (but failed to build QEMU dependencies due to macOS 13 tier issues)

## Installation Steps

### 1. Install MacPorts

```bash
# Download MacPorts for macOS 13 Ventura
curl -L "https://github.com/macports/macports-base/releases/download/v2.10.4/MacPorts-2.10.4-13-Ventura.pkg" \
  -o /tmp/MacPorts-2.10.4-13-Ventura.pkg

# Install MacPorts (requires admin password)
sudo installer -pkg /tmp/MacPorts-2.10.4-13-Ventura.pkg -target /

# Update MacPorts definitions
sudo /opt/local/bin/port -v selfupdate
```

### 2. Install QEMU via MacPorts

```bash
# Install QEMU and all dependencies
sudo /opt/local/bin/port install qemu
```

**Note**: This installs 90+ dependencies including Python 3.13, glib2, gnutls, mesa, etc. Installation takes ~10-15 minutes.

### 3. Fix Docker Credential Helper

Remove the `credsStore` line from `~/.docker/config.json` if it references `desktop`:

```bash
# Edit ~/.docker/config.json and remove the line:
# "credsStore": "desktop",
```

Or use this command:
```bash
sed -i '' '/"credsStore": "desktop",/d' ~/.docker/config.json
```

### 4. Start Colima with QEMU

```bash
# Start Colima using QEMU backend with network address for host access
colima start --vm-type qemu --cpu 2 --memory 4 --disk 40 --network-address
```

**Options**:
- `--cpu 2`: 2 CPU cores
- `--memory 4`: 4GB RAM
- `--disk 40`: 40GB disk
- `--network-address`: Enables reachable IP for host-to-container networking

### 5. Run Docker Stack

```bash
cd "/Users/apple/API/General Biller(us & ca)"

# Build and start containers
docker compose up -d --build

# Run database migrations (with explicit PYTHONPATH)
docker compose exec web bash -c "cd /app && PYTHONPATH=/app alembic upgrade head"

# Check status
docker compose ps

# View logs
docker compose logs -f web
docker compose logs -f db
docker compose logs -f nginx
```

## Verification

Test the health endpoints:

```bash
# Health check
curl http://localhost/health
# {"environment":"production","status":"ok"}

# Readiness check
curl http://localhost/readiness
# {"ready":true,"status":"all systems operational"}

# Get auth token
TOKEN=$(curl -sS http://localhost/api/v1/auth/token -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id":"admin"}' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# Create a loan
curl -sS http://localhost/api/v1/personal/loans -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "loan_id":"PL001",
    "amount":25000,
    "monthly_payment":500,
    "interest_rate":5.5,
    "due_date":"01/15",
    "lender_name":"Globe Financial"
  }'
```

## Container Architecture

- **web**: Python 3.13 + Flask + Gunicorn on port 8000
- **db**: PostgreSQL 15 on port 5432 (internal)
- **nginx**: Nginx 1.25 reverse proxy on port 80 (→ web:8000)

## Stopping/Starting Services

```bash
# Stop all containers
docker compose down

# Start containers
docker compose up -d

# Restart a specific service
docker compose restart web

# Stop Colima VM
colima stop

# Start Colima VM
colima start
```

## Troubleshooting

### Import errors in Alembic

If you see `ModuleNotFoundError: No module named 'src'`:
```bash
docker compose exec web bash -c "cd /app && PYTHONPATH=/app alembic upgrade head"
```

### Credential helper errors

If you see `exec: "docker-credential-desktop": executable file not found`:
- Remove `"credsStore": "desktop"` from `~/.docker/config.json`

### Colima won't start

- Check VM type: `colima list`
- Delete and recreate: `colima delete default && colima start --vm-type qemu ...`

## Performance Notes

- QEMU is slower than native Docker Desktop or `vz` VM type
- Build times: ~13 minutes for full stack on first build
- Runtime performance: Acceptable for development/testing
- For production: Use a server with native Docker support or macOS 14+ with `vz` driver

## References

- MacPorts: https://www.macports.org
- Colima: https://github.com/abiosoft/colima
- QEMU: https://www.qemu.org
