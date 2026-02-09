# Exercices Docker — Du Simple au Très Avancé

---

## Niveau 1 : Débutant

### Exercice 1.1 — Premiers pas avec Docker

```
Tâches :
1. Vérifie que Docker est installé (docker version, docker info).
2. Télécharge l'image "hello-world" et lance-la.
3. Liste les images locales.
4. Liste les conteneurs (en cours et arrêtés).
5. Supprime le conteneur et l'image.
```

<details>
<summary>Solution</summary>

```bash
docker version
docker info

docker run hello-world

docker images
# REPOSITORY    TAG       IMAGE ID       SIZE
# hello-world   latest    abc123         13.3kB

docker ps -a
# CONTAINER ID  IMAGE         STATUS                   NAMES
# xyz789        hello-world   Exited (0) 5 seconds ago dreamy_tesla

docker rm xyz789          # supprimer le conteneur
docker rmi hello-world    # supprimer l'image
```
</details>

---

### Exercice 1.2 — Lancer un conteneur interactif

```
Tâches :
1. Lance un conteneur Ubuntu en mode interactif (-it).
2. Dans le conteneur : installe curl, fais une requête HTTP.
3. Quitte le conteneur. Que se passe-t-il avec curl au prochain démarrage ?
4. Redémarre le conteneur arrêté et rattache-toi.
5. Explique la différence entre docker run, docker start, docker exec.
```

<details>
<summary>Solution</summary>

```bash
docker run -it --name mon-ubuntu ubuntu:22.04 bash

# Dans le conteneur :
apt update && apt install -y curl
curl https://httpbin.org/get
exit

# curl sera PERDU si on fait un nouveau "docker run"
# mais CONSERVÉ si on redémarre le même conteneur :
docker start mon-ubuntu
docker exec -it mon-ubuntu bash
which curl  # → /usr/bin/curl (toujours là)
```

**Différences :**
- `docker run` : crée un NOUVEAU conteneur à partir d'une image
- `docker start` : redémarre un conteneur EXISTANT arrêté
- `docker exec` : exécute une commande dans un conteneur EN COURS d'exécution
</details>

---

### Exercice 1.3 — Volumes et persistance

```
Tâches :
1. Lance un conteneur avec un bind mount (-v) qui lie un dossier local.
2. Crée un fichier dans le conteneur, vérifie qu'il apparaît localement.
3. Modifie le fichier localement, vérifie que le changement est visible
   dans le conteneur.
4. Crée un named volume avec docker volume create.
5. Lance 2 conteneurs qui partagent le même volume.
6. Explique la différence entre bind mount et named volume.
```

<details>
<summary>Solution</summary>

```bash
# Bind mount
mkdir ~/docker-data
docker run -it -v ~/docker-data:/data ubuntu bash
# Dans le conteneur :
echo "from container" > /data/test.txt
exit
cat ~/docker-data/test.txt  # → "from container"

# Named volume
docker volume create shared-data
docker run -d --name writer -v shared-data:/data ubuntu bash -c "echo hello > /data/msg.txt && sleep 3600"
docker run -it --name reader -v shared-data:/data ubuntu cat /data/msg.txt
# → "hello"

docker volume ls
docker volume inspect shared-data
```

**Différences :**
- **Bind mount** : chemin absolu sur l'hôte, tu contrôles où les données vivent
- **Named volume** : géré par Docker dans /var/lib/docker/volumes/, portable, recommandé pour la production
</details>

---

### Exercice 1.4 — Port mapping et networking basique

```
Tâches :
1. Lance un conteneur nginx et mappe le port 80 vers le port 8080 local.
2. Accède à nginx depuis ton navigateur ou curl.
3. Lance un 2ème nginx sur un port différent.
4. Inspecte les réseaux Docker par défaut.
5. Arrête et supprime tous les conteneurs.
```

<details>
<summary>Solution</summary>

```bash
docker run -d --name web1 -p 8080:80 nginx
docker run -d --name web2 -p 8081:80 nginx

curl http://localhost:8080   # → page nginx
curl http://localhost:8081   # → page nginx

docker network ls
docker network inspect bridge

# Nettoyage
docker stop web1 web2
docker rm web1 web2

# Ou en une commande :
docker rm -f web1 web2
```
</details>

---

## Niveau 2 : Intermédiaire

### Exercice 2.1 — Écrire un Dockerfile

```
Contexte : Crée une application Flask simple conteneurisée.

Tâches :
1. Crée une app Flask minimale (app.py + requirements.txt).
2. Écris un Dockerfile qui :
   - Part de python:3.11-slim
   - Copie les fichiers
   - Installe les dépendances
   - Expose le port 5000
   - Lance l'application
3. Build l'image et lance le conteneur.
4. Teste avec curl.
```

<details>
<summary>Solution</summary>

```python
# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return {"message": "Hello from Docker!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

```
# requirements.txt
flask==3.0.0
```

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

```bash
docker build -t flask-app .
docker run -d -p 5000:5000 --name my-flask flask-app
curl http://localhost:5000
# {"message": "Hello from Docker!"}
```
</details>

---

### Exercice 2.2 — Multi-stage build

```
Contexte : Tu as une application React. Le build prend 1.5GB mais
le résultat est juste du HTML/CSS/JS statique.

Tâches :
1. Écris un Dockerfile multi-stage :
   - Stage 1 (builder) : installe les dépendances, build le projet
   - Stage 2 (runtime) : copie seulement les fichiers buildés dans nginx
2. Compare la taille de l'image avec et sans multi-stage.
```

<details>
<summary>Solution</summary>

```dockerfile
# Stage 1 : Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2 : Runtime
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```bash
# Comparaison
docker build -t react-app-multi .
docker images | grep react-app
# react-app-multi    latest    ...    ~25MB    (multi-stage)
# react-app-single   latest    ...    ~1.5GB   (sans multi-stage)
```

**Pourquoi multi-stage :**
- Image finale beaucoup plus petite
- Pas d'outils de build (node, npm) dans l'image de production
- Surface d'attaque réduite
</details>

---

### Exercice 2.3 — Docker Compose

```
Contexte : Tu as une application web + base de données + cache Redis.

Tâches :
1. Écris un docker-compose.yml avec 3 services :
   - web (Flask/Django/Express)
   - db (PostgreSQL)
   - cache (Redis)
2. Configure les variables d'environnement.
3. Configure un healthcheck pour la base de données.
4. Configure un volume nommé pour la persistance de la DB.
5. Lance, arrête, et relance la stack complète.
```

<details>
<summary>Solution</summary>

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    volumes:
      - .:/app  # bind mount pour le développement
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

```bash
docker compose up -d        # démarrer en arrière-plan
docker compose ps            # voir le statut
docker compose logs -f web   # suivre les logs du web
docker compose down          # arrêter et supprimer
docker compose down -v       # + supprimer les volumes
docker compose up -d --build # rebuild + restart
```
</details>

---

### Exercice 2.4 — Réseaux Docker

```
Tâches :
1. Crée un réseau bridge custom "app-net".
2. Lance 2 conteneurs sur ce réseau.
3. Vérifie qu'ils peuvent se ping par nom de conteneur (DNS intégré).
4. Lance un 3ème conteneur sur le réseau par défaut.
5. Vérifie qu'il ne peut PAS communiquer avec les 2 premiers.
6. Connecte le 3ème conteneur au réseau app-net (sans le recréer).
```

<details>
<summary>Solution</summary>

```bash
docker network create app-net

docker run -d --name api --network app-net nginx
docker run -d --name worker --network app-net alpine sleep 3600

# Test DNS et connectivity
docker exec worker ping -c 2 api
# PING api (172.18.0.2): 64 bytes from 172.18.0.2

# Conteneur isolé
docker run -d --name outsider alpine sleep 3600
docker exec outsider ping -c 2 api
# ping: bad address 'api' → pas de résolution DNS

# Connecter au réseau
docker network connect app-net outsider
docker exec outsider ping -c 2 api
# Fonctionne maintenant !

docker network inspect app-net
docker network disconnect app-net outsider
```
</details>

---

### Exercice 2.5 — Optimisation du Dockerfile

```
Tâches :
Prends ce Dockerfile inefficace et optimise-le :
```

```dockerfile
# AVANT (inefficace)
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y curl
CMD ["python", "app.py"]
```

```
Optimisations à faire :
1. Utiliser une image slim/alpine.
2. Optimiser l'ordre des couches pour le cache.
3. Minimiser le nombre de layers RUN.
4. Ajouter un .dockerignore.
5. Ne pas tourner en root.
6. Utiliser --no-cache-dir pour pip.
```

<details>
<summary>Solution</summary>

```dockerfile
# APRÈS (optimisé)
FROM python:3.11-slim

# Installer les dépendances système en une seule couche
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root
RUN useradd --create-home appuser
WORKDIR /home/appuser/app

# Copier et installer les dépendances Python en premier (cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source (change le plus souvent → dernière couche)
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
```

```
# .dockerignore
.git
.gitignore
__pycache__
*.pyc
.env
.venv
venv/
node_modules/
Dockerfile
docker-compose.yml
.dockerignore
README.md
tests/
```

**Principes :**
- Ce qui change le MOINS souvent → en HAUT du Dockerfile
- Ce qui change le PLUS souvent → en BAS
- Chaque instruction crée une couche cachée
</details>

---

## Niveau 3 : Avancé

### Exercice 3.1 — Docker dans un pipeline CI/CD

```
Tâches :
1. Écris un Dockerfile qui lance les tests pendant le build
   et échoue si les tests échouent.
2. Crée un docker-compose.test.yml pour les tests d'intégration.
3. Implémente le pattern "build → test → push" avec des tags
   basés sur le git commit hash.
4. Configure un registry privé local et pousse/tire des images.
```

<details>
<summary>Solution</summary>

```dockerfile
# Dockerfile avec tests intégrés
FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Stage de test (échoue si les tests échouent)
FROM base AS test
RUN pip install --no-cache-dir pytest
RUN pytest tests/ -v --tb=short

# Stage de production (n'est atteint que si les tests passent)
FROM base AS production
USER nobody
CMD ["python", "app.py"]
```

```yaml
# docker-compose.test.yml
services:
  test:
    build:
      context: .
      target: test
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://test:test@db:5432/testdb

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: testdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 2s
      timeout: 5s
      retries: 10
```

```bash
# Pipeline CI
#!/bin/bash
set -e

GIT_SHA=$(git rev-parse --short HEAD)
IMAGE="registry.example.com/myapp"

# Build et test
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
echo "Tests passed!"

# Tag et push
docker build -t $IMAGE:$GIT_SHA -t $IMAGE:latest --target production .
docker push $IMAGE:$GIT_SHA
docker push $IMAGE:latest

# Registry privé local
docker run -d -p 5000:5000 --name registry registry:2
docker tag myapp localhost:5000/myapp:latest
docker push localhost:5000/myapp:latest
docker pull localhost:5000/myapp:latest
```
</details>

---

### Exercice 3.2 — Sécurité des conteneurs

```
Tâches :
1. Scanne une image Docker pour les vulnérabilités (trivy ou docker scout).
2. Crée un conteneur avec des capabilities Linux réduites.
3. Lance un conteneur en read-only filesystem.
4. Configure un seccomp profile.
5. Implémente un utilisateur non-root et vérifie.
6. Analyse une image : combien de couches ? Quels fichiers sont sensibles ?
```

<details>
<summary>Solution</summary>

```bash
# 1. Scanner les vulnérabilités
docker scout cves myapp:latest
# ou avec trivy :
trivy image myapp:latest

# 2. Capabilities réduites
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
# Supprime TOUTES les capabilities puis ajoute seulement ce qui est nécessaire

# 3. Read-only filesystem
docker run --read-only --tmpfs /tmp --tmpfs /var/run myapp
# Le conteneur ne peut rien écrire sauf dans /tmp et /var/run

# 4. Seccomp profile
docker run --security-opt seccomp=./seccomp-profile.json myapp

# 5. Non-root (dans Dockerfile)
# FROM python:3.11-slim
# RUN useradd -r -s /bin/false appuser
# USER appuser

# Vérifier :
docker exec myapp whoami
# → appuser (pas root)

docker exec myapp id
# uid=1000(appuser) gid=1000(appuser)

# 6. Analyser les couches
docker history myapp:latest
docker inspect myapp:latest

# Outil dive pour explorer les couches interactivement :
dive myapp:latest
```

```json
// seccomp-profile.json (exemple restrictif)
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": ["read", "write", "open", "close", "stat", "fstat",
                "mmap", "mprotect", "munmap", "brk", "exit_group",
                "access", "getpid", "socket", "connect", "sendto",
                "recvfrom", "bind", "listen", "accept"],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```
</details>

---

### Exercice 3.3 — Healthchecks et restart policies

```
Tâches :
1. Ajoute un HEALTHCHECK dans le Dockerfile.
2. Configure les restart policies (no, on-failure, always, unless-stopped).
3. Simule un crash d'application et vérifie le restart automatique.
4. Configure un healthcheck dans docker-compose avec interval, timeout, retries.
5. Utilise depends_on avec condition: service_healthy.
```

<details>
<summary>Solution</summary>

```dockerfile
# Dans le Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
```

```bash
# Restart policies
docker run -d --restart=no myapp           # pas de restart (défaut)
docker run -d --restart=on-failure:5 myapp # restart max 5 fois si exit != 0
docker run -d --restart=always myapp       # restart toujours
docker run -d --restart=unless-stopped myapp # comme always mais pas après docker stop

# Vérifier le health status
docker ps
# CONTAINER ID  STATUS
# abc123        Up 2 min (healthy)

docker inspect --format='{{.State.Health.Status}}' myapp
# healthy

# Voir les logs de healthcheck
docker inspect --format='{{json .State.Health}}' myapp | python -m json.tool
```

```yaml
# docker-compose.yml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped

  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s
    restart: unless-stopped
```
</details>

---

### Exercice 3.4 — Docker logging et monitoring

```
Tâches :
1. Configure les différents logging drivers (json-file, syslog, fluentd).
2. Limite la taille des logs (log rotation).
3. Collecte les métriques Docker avec Prometheus + cAdvisor.
4. Crée un dashboard Grafana pour monitorer tes conteneurs.
```

<details>
<summary>Solution</summary>

```bash
# Logging drivers
docker run -d --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  myapp

# Configuration globale dans /etc/docker/daemon.json
cat > /etc/docker/daemon.json << 'EOF'
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "5"
  }
}
EOF
```

```yaml
# docker-compose monitoring stack
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin

volumes:
  prometheus-data:
  grafana-data:
```

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
  - job_name: 'docker'
    static_configs:
      - targets: ['host.docker.internal:9323']
```
</details>

---

### Exercice 3.5 — Build context et cache avancé

```
Tâches :
1. Utilise BuildKit et explique ses avantages.
2. Utilise le cache mount pour pip/npm (--mount=type=cache).
3. Utilise le secret mount pour ne pas exposer de secrets dans les layers.
4. Implémente un build avec un cache externe (registry cache).
5. Analyse l'impact du .dockerignore sur la taille du build context.
```

<details>
<summary>Solution</summary>

```dockerfile
# syntax=docker/dockerfile:1

# Activer BuildKit
# export DOCKER_BUILDKIT=1

FROM python:3.11-slim

WORKDIR /app

# Cache mount pour pip (persiste entre builds)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Secret mount (jamais stocké dans une layer)
RUN --mount=type=secret,id=aws_creds,target=/root/.aws/credentials \
    aws s3 cp s3://bucket/config.json /app/config.json

COPY . .
CMD ["python", "app.py"]
```

```bash
# Build avec secret
docker build --secret id=aws_creds,src=~/.aws/credentials .

# Cache externe (registry)
docker build \
  --cache-from=registry.example.com/myapp:cache \
  --cache-to=type=registry,ref=registry.example.com/myapp:cache \
  -t myapp .

# Build avec cache inline (stocké dans l'image)
docker build --build-arg BUILDKIT_INLINE_CACHE=1 -t myapp .
docker push myapp  # le cache est inclus dans l'image

# Analyser le build context
# Avant .dockerignore :
docker build . 2>&1 | head -1
# Sending build context to Docker daemon  250MB

# Après .dockerignore avec .git, node_modules, venv exclus :
# Sending build context to Docker daemon  2.5MB
```
</details>

---

## Niveau 4 : Très Avancé

### Exercice 4.1 — Container orchestration sans Kubernetes

```
Tâches :
1. Utilise Docker Swarm :
   - Initialise un swarm
   - Déploie un service avec 3 réplicas
   - Fais un rolling update
   - Configure le load balancing ingress
2. Implémente un blue-green deployment avec Docker Compose.
3. Configure un reverse proxy (Traefik) avec auto-discovery des conteneurs.
```

<details>
<summary>Solution</summary>

```bash
# Docker Swarm
docker swarm init

# Déployer un service
docker service create \
  --name web \
  --replicas 3 \
  --publish 80:5000 \
  --update-delay 10s \
  --update-parallelism 1 \
  --rollback-on-failure \
  myapp:v1

# Rolling update
docker service update --image myapp:v2 web

# Rollback
docker service rollback web

# Voir le statut
docker service ls
docker service ps web
```

```yaml
# Blue-Green avec Compose
# docker-compose.yml
services:
  blue:
    image: myapp:v1
    deploy:
      replicas: 3

  green:
    image: myapp:v2
    deploy:
      replicas: 0  # en standby

  proxy:
    image: traefik:v3.0
    ports:
      - "80:80"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
```

```yaml
# Traefik avec auto-discovery
services:
  traefik:
    image: traefik:v3.0
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedByDefault=false"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
      - "8080:8080"  # dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  api:
    image: myapp
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.localhost`)"
      - "traefik.http.services.api.loadbalancer.server.port=5000"
    deploy:
      replicas: 3
```
</details>

---

### Exercice 4.2 — Docker et les namespaces Linux

```
Contexte : Comprendre ce que Docker fait sous le capot.

Tâches :
1. Crée un conteneur "à la main" avec les namespaces Linux :
   - PID namespace (isoler les processus)
   - NET namespace (isoler le réseau)
   - MNT namespace (isoler le filesystem)
   - UTS namespace (isoler le hostname)
2. Utilise nsenter pour entrer dans les namespaces d'un conteneur existant.
3. Compare les cgroups d'un conteneur avec et sans limites de ressources.
4. Explique le rôle d'overlay2 (ou le storage driver utilisé).
```

<details>
<summary>Solution</summary>

```bash
# 1. Créer un "conteneur" manuellement avec unshare
sudo unshare --pid --fork --mount-proc --net --uts bash

# Dans ce "conteneur" :
hostname container-manual
ps aux        # Seulement 2 processus (bash + ps)
ip addr       # Pas d'interface réseau (sauf lo)
mount         # Mountpoints isolés

# 2. nsenter dans un conteneur Docker
CONTAINER_PID=$(docker inspect --format '{{.State.Pid}}' mycontainer)
sudo nsenter --target $CONTAINER_PID --mount --uts --ipc --net --pid bash
# Tu es maintenant "dans" le conteneur au niveau kernel

# 3. Cgroups
# Sans limites :
docker run -d --name unlimited myapp
cat /sys/fs/cgroup/docker/<container-id>/memory.max
# → max (pas de limite)

# Avec limites :
docker run -d --name limited -m 256m --cpus=0.5 myapp
cat /sys/fs/cgroup/docker/<container-id>/memory.max
# → 268435456 (256 MB)
cat /sys/fs/cgroup/docker/<container-id>/cpu.max
# → 50000 100000 (50% d'un CPU)

# Voir les cgroups d'un conteneur
docker stats limited --no-stream

# 4. Storage driver
docker info | grep "Storage Driver"
# → overlay2

# Structure overlay2 :
ls /var/lib/docker/overlay2/<layer-id>/
# diff/     → les fichiers de cette couche
# merged/   → la vue unifiée (union mount)
# work/     → dossier de travail pour OverlayFS
# lower     → référence aux couches inférieures
```

**Architecture d'un conteneur Docker :**
```
┌─────────────────────────────┐
│  Processus applicatif       │
├─────────────────────────────┤
│  Namespaces (PID, NET, MNT, │
│  UTS, IPC, USER)            │
├─────────────────────────────┤
│  Cgroups (CPU, RAM, IO,     │
│  network bandwidth)         │
├─────────────────────────────┤
│  Union Filesystem (OverlayFS)│
│  image layers (read-only)   │
│  + container layer (r/w)    │
├─────────────────────────────┤
│  Kernel Linux (partagé)     │
└─────────────────────────────┘
```
</details>

---

### Exercice 4.3 — Images distroless et scratch

```
Tâches :
1. Crée une image basée sur "scratch" (zéro OS) pour un binaire Go.
2. Crée une image basée sur distroless pour une app Python.
3. Compare les tailles et surfaces d'attaque.
4. Gère le problème : pas de shell pour debug.
   Comment debugger un conteneur distroless ?
```

<details>
<summary>Solution</summary>

```go
// main.go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello from scratch!")
    })
    http.ListenAndServe(":8080", nil)
}
```

```dockerfile
# Dockerfile.scratch — Image FROM scratch (0 bytes de base)
FROM golang:1.22 AS builder
WORKDIR /app
COPY main.go .
# CGO_ENABLED=0 pour un binaire statique
RUN CGO_ENABLED=0 GOOS=linux go build -o server main.go

FROM scratch
COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 8080
ENTRYPOINT ["/server"]
```

```dockerfile
# Dockerfile.distroless — Pour Python
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt
COPY . .

FROM gcr.io/distroless/python3-debian12
WORKDIR /app
COPY --from=builder /app .
ENV PYTHONPATH=/app/deps
CMD ["app.py"]
```

```bash
# Comparaison de tailles
docker images
# scratch-app       latest    ~8MB
# distroless-app    latest    ~50MB
# python-slim-app   latest    ~200MB
# python-app        latest    ~1GB

# Debugger un conteneur distroless :

# Option 1 : image debug
FROM gcr.io/distroless/python3-debian12:debug
# Inclut busybox → un shell minimal

# Option 2 : ephemeral container (K8s)
kubectl debug -it myapp --image=busybox --target=myapp

# Option 3 : copier un binaire statique dans le conteneur
docker cp /usr/bin/busybox mycontainer:/busybox
docker exec mycontainer /busybox sh

# Option 4 : nsenter depuis l'hôte
PID=$(docker inspect --format '{{.State.Pid}}' mycontainer)
sudo nsenter -t $PID -m -u -i -n -p bash
```
</details>

---

### Exercice 4.4 — Docker et le réseau en profondeur

```
Tâches :
1. Crée un réseau macvlan (chaque conteneur a sa propre MAC/IP sur le LAN).
2. Crée un réseau ipvlan L2 et L3.
3. Implémente un réseau overlay multi-host (sans Swarm, avec consul/etcd).
4. Debug un problème réseau Docker :
   - Inspecte les iptables rules créées par Docker
   - Utilise tcpdump dans un conteneur
   - Trace le parcours d'un paquet de l'extérieur vers un conteneur
```

<details>
<summary>Solution</summary>

```bash
# 1. Macvlan
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  macvlan-net

docker run -d --network macvlan-net --ip=192.168.1.100 nginx
# Ce conteneur a sa propre adresse MAC et IP sur le réseau physique

# 2. IPvlan L2
docker network create -d ipvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  -o ipvlan_mode=l2 \
  ipvlan-l2

# IPvlan L3
docker network create -d ipvlan \
  --subnet=10.10.10.0/24 \
  -o parent=eth0 \
  -o ipvlan_mode=l3 \
  ipvlan-l3

# 3. Debug réseau

# Voir les iptables rules de Docker
sudo iptables -t nat -L -n -v | grep DOCKER
# DNAT rules pour le port mapping
# MASQUERADE rules pour le NAT sortant

# tcpdump dans un conteneur
docker run --net=container:myapp nicolaka/netshoot tcpdump -i eth0 port 5000

# Parcours d'un paquet (host:8080 → container:5000) :
# 1. Paquet arrive sur host:8080
# 2. iptables PREROUTING → DNAT vers 172.17.0.2:5000
# 3. Paquet traverse le bridge docker0
# 4. veth pair transmet au conteneur
# 5. Le conteneur reçoit sur eth0:5000

# Voir les veth pairs
ip link show type veth
bridge link show

# Voir le bridge
brctl show docker0  # ou: ip link show docker0
```
</details>

---

### Exercice 4.5 — Optimisation extrême des images

```
Tâches :
1. Réduis une image Python de 1GB à moins de 50MB.
2. Utilise upx pour compresser les binaires.
3. Implémente un système de cache de layers partagé entre projets.
4. Crée une image avec exactement 1 layer (squash).
5. Analyse chaque layer avec dive et élimine les fichiers inutiles.
```

<details>
<summary>Solution</summary>

```dockerfile
# Image Python ultra-optimisée
FROM python:3.11-slim AS builder
WORKDIR /build

# Installer les dépendances dans un virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Supprimer les fichiers inutiles des packages
RUN find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + && \
    find /opt/venv -type d -name "tests" -exec rm -rf {} + && \
    find /opt/venv -type d -name "test" -exec rm -rf {} + && \
    find /opt/venv -type f -name "*.pyc" -delete && \
    find /opt/venv -type f -name "*.pyo" -delete && \
    find /opt/venv -type f -name "*.txt" -delete && \
    find /opt/venv -type f -name "*.md" -delete

FROM python:3.11-slim
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY . .
USER nobody
CMD ["python", "app.py"]
```

```bash
# UPX pour binaires Go/C
FROM golang:1.22 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o server .
RUN apt-get update && apt-get install -y upx
RUN upx --best --lzma server
# -ldflags="-s -w" : strip debug info (~30% plus petit)
# upx : compression du binaire (~60% plus petit)

FROM scratch
COPY --from=builder /app/server /server
CMD ["/server"]

# Squash all layers
docker build --squash -t myapp .
# Crée une seule layer (EXPERIMENTAL)

# Analyse avec dive
dive myapp:latest
# Interface TUI qui montre :
# - Chaque layer et sa taille
# - Les fichiers ajoutés/modifiés/supprimés par layer
# - Le "wasted space" (fichiers supprimés dans des layers supérieures)
# - L'efficacité globale de l'image
```
</details>

---

## Niveau 5 : Expert / Deep

### Exercice 5.1 — Construire un runtime de conteneurs minimal

```
Contexte : Comprendre comment Docker fonctionne en implémentant
un mini-runtime de conteneurs en bash.

Tâches :
1. Crée un filesystem root minimal (avec debootstrap ou busybox).
2. Utilise chroot pour isoler le filesystem.
3. Ajoute les namespaces (PID, NET, UTS, MNT) avec unshare.
4. Configure les cgroups pour limiter CPU et mémoire.
5. Configure un réseau avec veth pairs et un bridge.
6. Le résultat : un "docker run" minimaliste en ~50 lignes de bash.
```

<details>
<summary>Solution</summary>

```bash
#!/bin/bash
# mini-container.sh — Un runtime de conteneurs en bash
set -e

CONTAINER_NAME=${1:-mycontainer}
COMMAND=${2:-/bin/sh}
ROOTFS="/var/containers/$CONTAINER_NAME/rootfs"
CGROUP_PATH="/sys/fs/cgroup/$CONTAINER_NAME"

# 1. Créer le rootfs
mkdir -p "$ROOTFS"
if [ ! -f "$ROOTFS/bin/busybox" ]; then
    # Méthode busybox (ultra-léger)
    docker export $(docker create busybox) | tar -C "$ROOTFS" -xf -
fi

# 2. Configurer les cgroups v2
mkdir -p "$CGROUP_PATH"
echo "256M" > "$CGROUP_PATH/memory.max"
echo "50000 100000" > "$CGROUP_PATH/cpu.max"  # 50% CPU
echo "$$" > "$CGROUP_PATH/cgroup.procs"

# 3. Configurer le réseau
ip link add veth-host type veth peer name veth-container
ip link set veth-host up
ip addr add 10.0.0.1/24 dev veth-host

# 4. Lancer avec namespaces
unshare --pid --fork --mount --uts --net --map-root-user bash << INNER
    # Monter /proc dans le nouveau namespace
    mount -t proc proc "$ROOTFS/proc"
    mount -t sysfs sysfs "$ROOTFS/sys"
    mount -t tmpfs tmpfs "$ROOTFS/tmp"
    mount -t devtmpfs devtmpfs "$ROOTFS/dev"

    # Configurer le réseau dans le namespace
    ip link set veth-container up
    ip addr add 10.0.0.2/24 dev veth-container
    ip route add default via 10.0.0.1

    # Changer le hostname
    hostname "$CONTAINER_NAME"

    # Pivot root
    cd "$ROOTFS"
    mkdir -p .old_root
    pivot_root . .old_root
    umount -l /.old_root
    rmdir /.old_root

    # Lancer la commande
    exec $COMMAND
INNER

# 5. Nettoyage
ip link delete veth-host 2>/dev/null
rmdir "$CGROUP_PATH" 2>/dev/null
```

**Ce que fait Docker en plus :**
- OCI runtime spec (runc)
- Image management (pull, layers, overlay)
- Networking plugins (CNI/CNM)
- Logging drivers
- API REST + CLI
- Security (seccomp, AppArmor, SELinux)
- Storage drivers (overlay2, btrfs, zfs)
</details>

---

### Exercice 5.2 — OCI, containerd et runc

```
Tâches :
1. Utilise runc directement (sans Docker) pour lancer un conteneur.
2. Utilise ctr (CLI de containerd) pour gérer des conteneurs.
3. Crée un OCI bundle manuellement.
4. Modifie le config.json OCI pour ajouter des restrictions.
5. Explique la stack complète : Docker CLI → dockerd → containerd → runc.
```

<details>
<summary>Solution</summary>

```bash
# 1. Créer un OCI bundle
mkdir -p mycontainer/rootfs
docker export $(docker create alpine) | tar -C mycontainer/rootfs -xf -

# 2. Générer la spec OCI
cd mycontainer
runc spec  # Crée config.json

# 3. Modifier config.json
# Changer le process :
# "args": ["sh"] → "args": ["/bin/echo", "Hello OCI"]

# Ajouter des restrictions de ressources :
# "linux": {
#   "resources": {
#     "memory": { "limit": 268435456 },
#     "cpu": { "quota": 50000, "period": 100000 }
#   }
# }

# 4. Lancer avec runc
sudo runc run mycontainer

# 5. Avec containerd (ctr)
sudo ctr images pull docker.io/library/alpine:latest
sudo ctr run --rm docker.io/library/alpine:latest test-container /bin/echo "Hello"

# Lister les conteneurs
sudo ctr containers list
sudo ctr tasks list

# 6. Stack complète
# docker CLI  →  REST API  →  dockerd (Docker daemon)
#                                  ↓
#                              containerd (gère le lifecycle)
#                                  ↓
#                              containerd-shim (process parent)
#                                  ↓
#                              runc (crée le conteneur avec namespaces/cgroups)
#                                  ↓
#                              process applicatif (PID 1 dans le conteneur)
```
</details>

---

### Exercice 5.3 — Docker in Docker (DinD) et alternatives

```
Tâches :
1. Lance Docker-in-Docker (DinD) et explique les risques.
2. Implémente l'alternative socket mounting (/var/run/docker.sock).
3. Utilise Kaniko pour builder des images sans Docker daemon.
4. Utilise Buildah pour builder des images sans daemon (rootless).
5. Compare les approches pour un pipeline CI/CD.
```

<details>
<summary>Solution</summary>

```bash
# 1. Docker-in-Docker (DinD)
docker run --privileged -d --name dind docker:dind
docker exec -it dind docker run hello-world
# Risques : --privileged donne un accès complet au kernel !

# 2. Socket mounting (Docker-outside-of-Docker)
docker run -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(which docker):/usr/bin/docker \
  my-ci-image docker ps
# Les conteneurs lancés sont des "frères" (pas des enfants)
# Risque : accès au daemon Docker de l'hôte = quasi root

# 3. Kaniko (pas de daemon, pas de privilèges)
docker run \
  -v $(pwd):/workspace \
  -v ~/.docker/config.json:/kaniko/.docker/config.json \
  gcr.io/kaniko-project/executor:latest \
  --dockerfile /workspace/Dockerfile \
  --destination registry.example.com/myapp:latest \
  --context /workspace

# 4. Buildah (rootless, daemonless)
buildah bud -t myapp .                    # build
buildah from scratch                       # créer depuis zéro
buildah copy mycontainer app /app          # ajouter des fichiers
buildah config --cmd "/app" mycontainer    # configurer
buildah commit mycontainer myapp:latest    # commiter en image
buildah push myapp:latest docker://registry.example.com/myapp:latest

# 5. Podman (alternative complète à Docker, daemonless, rootless)
podman build -t myapp .
podman run -d myapp
podman-compose up -d
# Compatible avec les Dockerfiles et docker-compose.yml
```

**Comparaison pour CI/CD :**
| Méthode | Privileges | Daemon | Sécurité | Vitesse |
|---------|-----------|--------|----------|---------|
| DinD | --privileged | Oui | Faible | Rapide |
| Socket mount | Non | Hôte | Moyenne | Rapide |
| Kaniko | Non | Non | Haute | Moyenne |
| Buildah | Non (rootless) | Non | Haute | Moyenne |
</details>

---

### Exercice 5.4 — Systèmes de fichiers et storage drivers en profondeur

```
Tâches :
1. Explique et démontre le fonctionnement d'OverlayFS.
2. Crée manuellement un overlay mount avec plusieurs layers.
3. Montre le copy-on-write en action.
4. Compare overlay2, btrfs, zfs, et devicemapper.
5. Implémente un système de layer caching custom.
```

<details>
<summary>Solution</summary>

```bash
# 1. Comprendre OverlayFS
# OverlayFS = union de plusieurs répertoires en un seul

# Structure :
# lower/  → couches read-only (image layers)
# upper/  → couche read-write (container layer)
# work/   → dossier temporaire pour OverlayFS
# merged/ → la vue unifiée

# 2. Créer un overlay manuellement
mkdir -p /tmp/overlay/{lower1,lower2,upper,work,merged}

# Layer 1 (base)
echo "base file" > /tmp/overlay/lower1/base.txt
echo "will be overridden" > /tmp/overlay/lower1/config.txt

# Layer 2
echo "layer 2 file" > /tmp/overlay/lower2/app.txt
echo "overridden value" > /tmp/overlay/lower2/config.txt

# Monter l'overlay
sudo mount -t overlay overlay \
  -o lowerdir=/tmp/overlay/lower2:/tmp/overlay/lower1,\
upperdir=/tmp/overlay/upper,\
workdir=/tmp/overlay/work \
  /tmp/overlay/merged

ls /tmp/overlay/merged/
# base.txt config.txt app.txt
cat /tmp/overlay/merged/config.txt
# "overridden value" (lower2 a priorité sur lower1)

# 3. Copy-on-Write en action
# Modifier un fichier de la couche lower :
echo "modified" > /tmp/overlay/merged/base.txt
ls /tmp/overlay/upper/
# base.txt → le fichier a été COPIÉ dans upper avant modification
cat /tmp/overlay/lower1/base.txt
# "base file" → l'original est intact !

# Supprimer un fichier :
rm /tmp/overlay/merged/app.txt
ls -la /tmp/overlay/upper/
# app.txt → c'est un "whiteout" (character device 0,0)
# Le fichier existe toujours dans lower2 mais est "masqué"

# 4. Comparaison storage drivers
# overlay2 : standard, performant, recommandé
# btrfs    : snapshots natifs, déduplication, nécessite btrfs
# zfs      : checksums, compression, snapshots, nécessite zfs
# devicemapper : block-level, plus lent, déprécié

# Voir le driver actuel
docker info | grep -i storage

# 5. Voir les layers d'une image
docker inspect --format='{{json .RootFS.Layers}}' myapp | python -m json.tool
# Liste les SHA des layers

# Voir physiquement les layers
ls /var/lib/docker/overlay2/
# Chaque dossier = une layer
# Le fichier "link" contient l'identifiant court
# Le fichier "lower" pointe vers les layers inférieures
```
</details>

---

### Exercice 5.5 — Docker et la sécurité en profondeur

```
Tâches :
1. Implémente un rootless Docker (pas de daemon root).
2. Configure user namespaces pour remapper UID/GID.
3. Crée un AppArmor profile custom pour un conteneur.
4. Implémente la signature d'images avec Cosign (Sigstore).
5. Configure un admission policy qui refuse les images non signées.
6. Scanne les images dans le pipeline CI et bloque le déploiement
   si des CVE critiques sont détectées.
```

<details>
<summary>Solution</summary>

```bash
# 1. Rootless Docker
dockerd-rootless-setuptool.sh install
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
docker run hello-world  # fonctionne sans root !

# 2. User namespace remapping
# /etc/docker/daemon.json
{
  "userns-remap": "default"
}
# Docker crée un user "dockremap"
# UID 0 dans le conteneur → UID 100000+ sur l'hôte
# Même si un attaquant s'échappe du conteneur, il n'est pas root

# 3. AppArmor profile custom
cat > /etc/apparmor.d/docker-custom << 'EOF'
#include <tunables/global>

profile docker-custom flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # Interdire l'écriture sur /etc et /usr
  deny /etc/** w,
  deny /usr/** w,

  # Autoriser la lecture
  /etc/** r,
  /usr/** r,

  # Autoriser /tmp et /app
  /tmp/** rw,
  /app/** rw,

  # Interdire les raw sockets
  deny network raw,

  # Interdire mount/umount
  deny mount,
  deny umount,
}
EOF
sudo apparmor_parser -r /etc/apparmor.d/docker-custom
docker run --security-opt apparmor=docker-custom myapp

# 4. Signature d'images avec Cosign
cosign generate-key-pair
cosign sign --key cosign.key registry.example.com/myapp:latest
cosign verify --key cosign.pub registry.example.com/myapp:latest

# 5. Pipeline CI avec scan et signature
#!/bin/bash
set -e
IMAGE="registry.example.com/myapp:${GIT_SHA}"

docker build -t $IMAGE .

# Scan avec trivy
trivy image --severity CRITICAL --exit-code 1 $IMAGE
if [ $? -ne 0 ]; then
    echo "CRITICAL CVEs found! Blocking deployment."
    exit 1
fi

# Push et signer
docker push $IMAGE
cosign sign --key cosign.key $IMAGE
echo "Image pushed and signed successfully."
```
</details>

---

### Exercice 5.6 — Debugging avancé des conteneurs

```
Contexte : Un conteneur crash en boucle, les logs ne disent rien d'utile.

Tâches :
1. Utilise docker events pour surveiller les événements en temps réel.
2. Utilise strace pour tracer les syscalls d'un processus dans un conteneur.
3. Utilise nsenter pour debugger un conteneur sans shell.
4. Analyse un core dump d'un conteneur crashé.
5. Utilise eBPF (bpftrace) pour tracer les appels réseau d'un conteneur.
6. Debug un OOM kill : identifie quel processus a été tué et pourquoi.
```

<details>
<summary>Solution</summary>

```bash
# 1. Docker events
docker events --filter container=myapp
docker events --filter event=die --filter event=oom

# 2. strace
# Option A : depuis l'hôte
PID=$(docker inspect --format '{{.State.Pid}}' myapp)
sudo strace -p $PID -f -e trace=network

# Option B : avec nsenter
sudo nsenter -t $PID -p -n strace -p 1

# 3. nsenter complet
PID=$(docker inspect --format '{{.State.Pid}}' myapp)
sudo nsenter -t $PID \
  --mount \   # filesystem du conteneur
  --uts \     # hostname
  --ipc \     # IPC
  --net \     # réseau
  --pid \     # processus
  bash

# 4. Core dump
# Configurer le core dump pattern sur l'hôte
echo "/tmp/cores/core.%e.%p" | sudo tee /proc/sys/kernel/core_pattern

docker run --ulimit core=-1 -v /tmp/cores:/tmp/cores myapp
# Après crash :
gdb /path/to/binary /tmp/cores/core.myapp.1234

# 5. eBPF / bpftrace
# Tracer les connexions TCP d'un conteneur
sudo bpftrace -e '
  tracepoint:syscalls:sys_enter_connect
  /comm == "python"/ {
    printf("%s connecting...\n", comm);
  }
'

# Tracer les appels réseau d'un namespace spécifique
NETNS=$(docker inspect --format '{{.NetworkSettings.SandboxKey}}' myapp)
sudo nsenter --net=$NETNS tcpdump -i eth0

# 6. OOM Kill debug
# Vérifier si un conteneur a été OOM-killed
docker inspect --format='{{.State.OOMKilled}}' myapp
# → true

# Voir dans les logs kernel
dmesg | grep -i "oom\|killed"
# Out of memory: Kill process 1234 (python) score 950 or sacrifice child

# Voir la consommation mémoire en temps réel
docker stats myapp

# Voir le détail mémoire dans les cgroups
cat /sys/fs/cgroup/docker/<id>/memory.current
cat /sys/fs/cgroup/docker/<id>/memory.events
# → oom 1    (nombre d'OOM kills)

# Solution : augmenter la limite ou optimiser l'app
docker update --memory=512m myapp
```
</details>

---

### Exercice 5.7 — Performance et tuning avancé

```
Tâches :
1. Benchmark le réseau Docker (bridge vs host vs macvlan).
2. Optimise les performances I/O avec les options de storage driver.
3. Configure les ulimits correctement pour la production.
4. Optimise le DNS resolution dans Docker.
5. Configure NUMA-aware container placement.
```

<details>
<summary>Solution</summary>

```bash
# 1. Benchmark réseau
# Bridge (défaut) : ~30-50% overhead vs host
docker run --rm --network bridge nicolaka/netshoot iperf3 -c host.docker.internal

# Host (pas d'overhead réseau)
docker run --rm --network host nicolaka/netshoot iperf3 -c <target>

# Macvlan (performance quasi-native)
docker run --rm --network macvlan-net nicolaka/netshoot iperf3 -c <target>

# 2. Optimisation I/O
docker run -d \
  --device-write-bps /dev/sda:100mb \
  --device-read-bps /dev/sda:100mb \
  --device-write-iops /dev/sda:1000 \
  myapp

# Utiliser tmpfs pour les fichiers temporaires
docker run -d --tmpfs /tmp:rw,size=256m,mode=1777 myapp

# 3. Ulimits production
docker run -d \
  --ulimit nofile=65535:65535 \
  --ulimit nproc=4096:4096 \
  --ulimit core=0:0 \
  --ulimit memlock=-1:-1 \
  myapp

# 4. DNS optimization
# /etc/docker/daemon.json
{
  "dns": ["8.8.8.8", "8.8.4.4"],
  "dns-opts": ["ndots:1", "timeout:2", "attempts:2"],
  "dns-search": ["example.com"]
}

# Par conteneur
docker run --dns=8.8.8.8 --dns-opt="ndots:1" myapp

# 5. NUMA-aware placement
docker run -d \
  --cpuset-cpus="0-3" \          # CPUs sur NUMA node 0
  --cpuset-mems="0" \            # Mémoire sur NUMA node 0
  --memory=4g \
  myapp

# Vérifier la topologie NUMA
numactl --hardware
lscpu | grep NUMA
```
</details>

---
