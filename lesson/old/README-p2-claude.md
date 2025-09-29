# Corso Python: Infrastruttura e Best Practices
## Guida Pratica per Ricercatori (1 ora)

---

## 📋 Struttura del Corso (1 ora)

- **00:00-00:15** - Struttura Progetto Python e __init__.py
- **00:15-00:30** - Gestione Errori Professionale  
- **00:30-00:45** - Git e Workflow di Sviluppo
- **00:45-01:00** - Pipeline CI/CD Semplici

---

## Modulo 1: Struttura Progetto Python (15 minuti)

### ❌ Struttura Tipica Ricercatore
```
progetto/
├── script1.py
├── script2.py
├── data.csv
├── results.txt
└── old_version_backup.py
```

### ✅ Struttura Professionale
```
biomedical_project/
├── src/                      # Codice sorgente
│   └── biomedical/
│       ├── __init__.py      # IMPORTANTE: rende la cartella un package
│       ├── data/
│       │   ├── __init__.py
│       │   └── loader.py
│       ├── analysis/
│       │   ├── __init__.py
│       │   └── statistics.py
│       └── utils/
│           ├── __init__.py
│           └── config.py
├── tests/                    # Test separati dal codice
│   ├── __init__.py
│   ├── test_loader.py
│   └── test_statistics.py
├── data/                     # Dati (NON in git!)
│   └── .gitkeep
├── docs/                     # Documentazione
│   └── README.md
├── config/                   # Configurazioni
│   └── config.yaml
├── .gitignore               # File da ignorare
├── requirements.txt         # Dipendenze
├── setup.py                 # Installazione package
└── README.md               # Documentazione principale
```

### 🔑 Il Mistero di `__init__.py`

#### Cosa fa __init__.py?
```python
# src/biomedical/__init__.py

# 1. Rende la directory un package Python importabile
# 2. Può essere vuoto o contenere codice di inizializzazione

# Versione VUOTA (valida!)
# File vuoto ma DEVE esistere

# Versione con EXPORTS
"""Biomedical analysis package."""
__version__ = "1.0.0"

from .data.loader import DataLoader
from .analysis.statistics import Analyzer

# Ora posso fare: from biomedical import DataLoader
__all__ = ["DataLoader", "Analyzer"]  # Controlla cosa viene esportato
```

#### Import Corretti
```python
# SENZA __init__.py - NON FUNZIONA
from src.biomedical.data import loader  # ❌ ModuleNotFoundError

# CON __init__.py - FUNZIONA
from biomedical.data import loader      # ✅
from biomedical import DataLoader       # ✅ Se definito in __init__.py

# Import relativi (dentro il package)
from .data import loader               # ✅ Da analysis/statistics.py
from ..utils import config             # ✅ Salgo di un livello
```

### Setup.py per Installazione
```python
# setup.py - Rende il progetto installabile
from setuptools import setup, find_packages

setup(
    name="biomedical-analysis",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],
    python_requires=">=3.8",
)

# Ora posso installare con: pip install -e .
# -e = editable, modifiche immediate senza reinstallare
```

---

## Modulo 2: Gestione Errori Professionale (15 minuti)

### 🚫 Errori Tipici Ricercatori
```python
# ❌ SBAGLIATO - Ignora errori
try:
    data = pd.read_csv(file)
except:
    pass  # PERICOLOSO!

# ❌ SBAGLIATO - Catch generico
try:
    result = complex_analysis()
except Exception as e:
    print(f"Error: {e}")  # Nasconde problemi
```

### ✅ Gestione Errori Corretta

#### 1. Eccezioni Custom
```python
# exceptions.py
class BiomedicalError(Exception):
    """Base exception per il progetto."""
    pass

class DataValidationError(BiomedicalError):
    """Errore validazione dati."""
    pass

class AnalysisError(BiomedicalError):
    """Errore durante analisi."""
    pass

# Uso
def validate_patient_data(df):
    if 'patient_id' not in df.columns:
        raise DataValidationError(
            "Missing 'patient_id' column in dataset"
        )
    
    if df['age'].min() < 0:
        raise DataValidationError(
            f"Invalid age values: min={df['age'].min()}"
        )
```

#### 2. Context Manager per Risorse
```python
from contextlib import contextmanager
import tempfile
import shutil

@contextmanager
def temporary_analysis_dir():
    """Crea directory temporanea, garantisce cleanup."""
    temp_dir = tempfile.mkdtemp(prefix="analysis_")
    try:
        yield temp_dir
    finally:
        # Cleanup SEMPRE eseguito
        shutil.rmtree(temp_dir)

# Uso sicuro
with temporary_analysis_dir() as tmpdir:
    # Lavora con tmpdir
    process_files(tmpdir)
    # Cleanup automatico anche se c'è errore
```

#### 3. Retry Logic per Servizi Esterni
```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1.0):
    """Decorator per retry automatico."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2.0)
def call_ml_service(data):
    """Chiama servizio ML con retry automatico."""
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
```

#### 4. Logging degli Errori
```python
import logging
import traceback
from functools import wraps

def log_errors(logger):
    """Decorator per logging automatico errori."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"Error in {func.__name__}: {e}",
                    extra={
                        'traceback': traceback.format_exc(),
                        'args': args,
                        'kwargs': kwargs
                    }
                )
                raise
        return wrapper
    return decorator

@log_errors(logger)
def analyze_genome(data):
    # Se fallisce, errore loggato automaticamente
    return process(data)
```

---

## Modulo 3: Git e Workflow di Sviluppo (15 minuti)

### 📝 .gitignore Essenziale
```bash
# .gitignore per progetti biomedici Python

# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/

# Dati sensibili - MAI in repository!
*.csv
*.xlsx
*.h5
data/
results/
patient_data/

# Configurazioni locali
.env
config/local.yaml

# IDE
.vscode/
.idea/
*.swp

# Jupyter
.ipynb_checkpoints/
```

### 🌲 Git Flow Semplificato

#### Branch Strategy
```bash
main/              # Codice stabile, testato
├── develop/       # Sviluppo attivo
│   ├── feature/   # Nuove funzionalità
│   └── fix/       # Bug fixes
└── release/       # Preparazione release
```

#### Comandi Essenziali
```bash
# Setup iniziale
git init
git remote add origin <url>

# Workflow quotidiano
git checkout -b feature/analisi-statistica
# ... lavoro ...
git add -p  # Aggiungi interattivamente
git commit -m "feat: add statistical analysis module"
git push -u origin feature/analisi-statistica

# Commit semantici (convenzione)
# feat: nuova funzionalità
# fix: correzione bug
# docs: documentazione
# test: aggiunta test
# refactor: refactoring codice
```

#### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: no-data-files
        name: Check no data files
        entry: bash -c 'git diff --cached --name-only | grep -E "\.(csv|xlsx|h5)$" && exit 1 || exit 0'
        language: system
        
      - id: no-print-statements
        name: No print statements
        entry: bash -c 'git diff --cached --name-only | xargs grep -l "print(" && exit 1 || exit 0'
        language: system
        files: \.py$

# Installa: pre-commit install
```

### 📊 Template Commit Message
```bash
# .gitmessage
# <type>: <subject> (max 50 chars)

# <body> (optional, wrap at 72 chars)

# Type can be:
#   feat     (new feature)
#   fix      (bug fix)
#   docs     (documentation)
#   style    (formatting)
#   refactor (refactoring code)
#   test     (adding tests)
#   chore    (maintain)

# Example:
# feat: add patient data validation
#
# - Check age ranges (0-120)
# - Validate patient ID format
# - Add missing data handling

# Setup: git config --global commit.template .gitmessage
```

---

## Modulo 4: Pipeline CI/CD Semplici (15 minuti)

### 🔄 GitHub Actions - Pipeline Base
```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Cache dependencies
      uses: actions/cache@v2
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8
    
    - name: Lint with flake8
      run: |
        # Stop if syntax errors
        flake8 . --count --select=E9,F63,F7,F82 --show-source
        # Warning for complexity
        flake8 . --count --max-complexity=10 --max-line-length=88
    
    - name: Test with pytest
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### 🐳 Docker per Riproducibilità
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Dipendenze sistema (se necessarie)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Codice
COPY src/ ./src/
COPY config/ ./config/

# Non eseguire come root
RUN useradd -m myuser
USER myuser

CMD ["python", "-m", "biomedical.main"]
```

### 🔧 Makefile per Automazione
```makefile
# Makefile - Comandi comuni
.PHONY: help test install clean

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Check code style"
	@echo "  make clean    - Clean cache files"

install:
	pip install -r requirements.txt
	pip install -e .
	pre-commit install

test:
	pytest tests/ -v --cov=src

lint:
	black src/ tests/
	isort src/ tests/
	flake8 src/ tests/
	mypy src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov/

run:
	python -m biomedical.main

docker-build:
	docker build -t biomedical-analysis .

docker-run:
	docker run -v $(PWD)/data:/app/data biomedical-analysis
```

---

## 📋 Checklist Finale per Ricercatori

### Prima di Ogni Commit
- [ ] Test passano? (`pytest`)
- [ ] Nessun file dati? (`git status`)
- [ ] Codice formattato? (`black .`)
- [ ] Nessun `print()`? (usa logging)
- [ ] Documentazione aggiornata?

### Setup Nuovo Progetto
```bash
# 1. Struttura
mkdir -p src/progetto tests docs config data
touch src/progetto/__init__.py

# 2. Git
git init
echo "*.csv" >> .gitignore
git add .
git commit -m "Initial commit"

# 3. Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 4. Dipendenze
pip install pandas numpy pytest black
pip freeze > requirements.txt

# 5. Pre-commit
pre-commit install
```

### Configurazione VS Code
```json
{
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  },
  "python.testing.pytestEnabled": true,
  "python.linting.enabled": true,
  "editor.formatOnSave": true,
  "git.ignoreLimitWarning": true
}
```

---

## 🚀 Take-Home Messages

1. **__init__.py**: File vuoto che trasforma cartelle in package Python importabili
2. **Errori**: Mai ignorarli, sempre loggare, custom exceptions per domini specifici
3. **Git**: Mai committare dati sensibili, usa branch per features
4. **CI/CD**: Automatizza test e quality check, anche pipeline semplici aiutano molto
5. **Docker**: Garantisce riproducibilità tra ambienti diversi

---

*Guida complementare per trasformare codice di ricerca in software professionale - v1.0*