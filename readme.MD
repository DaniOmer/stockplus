# StockPlus Backend

#### 1. Project installation (Local development)

```bash
    git clone https://github.com/DaniOmer/stockplus.git
```

#### 1.a Installation without docker

##### - Development environment installation

```bash
    python3 -m venv .venv
    pip install -r configuration/requirements/development.txt
```

##### - Environment variables settings

```bash
    source configuration/environments/development
```

#### 1.b Installation with docker

##### - Build the docker image

```bash
    docker compose -f compose.dev.yaml build
```

##### - Start services

```bash
    docker compose -f compose.dev.yaml up -d
```
