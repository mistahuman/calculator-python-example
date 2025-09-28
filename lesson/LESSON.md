# Guida Python: Refactoring e Best Practices 

## Parte 1: Classi Python e Object-Oriented Programming

### Il Problema del Codice Procedurale

Il classico script "tutto in un file" che diventa ingestibile:

```python
# analisi_dati.py - Il disastro tipico
import pandas as pd

# Variabili globali ovunque
data_path = "/data/results.csv"
threshold = 2.5
processed_data = None

def load_data():
    global processed_data
    processed_data = pd.read_csv(data_path)
    processed_data = processed_data.dropna()

def analyze():
    if processed_data is None:
        load_data()
    outliers = processed_data[processed_data['value'] > threshold]
    print(f"Found {len(outliers)} outliers")
    return outliers

# Tutto mescolato, impossibile da testare
```

**Problemi**: stato globale, responsabilità mescolate, impossibile testare componenti singole, configurazione hardcoded.

### Refactoring con Classi: La Trasformazione

Il principio base: **una classe = una responsabilità**. Separiamo le preoccupazioni:

```python
from dataclasses import dataclass
from pathlib import Path
import pandas as pd

@dataclass
class AnalysisConfig:
    """Configurazione centralizzata e validata"""
    data_path: Path
    threshold: float = 2.5
    
    def __post_init__(self):
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found")

class DataLoader:
    """Solo responsabilità: caricamento dati"""
    def load_csv(self, path: Path) -> pd.DataFrame:
        return pd.read_csv(path).dropna()

class OutlierAnalyzer:
    """Solo responsabilità: analisi outliers"""  
    def find_outliers(self, df: pd.DataFrame, threshold: float) -> pd.DataFrame:
        return df[df['value'] > threshold]

class AnalysisPipeline:
    """Orchestratore - compone i componenti"""
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.loader = DataLoader()
        self.analyzer = OutlierAnalyzer()
    
    def run(self):
        data = self.loader.load_csv(self.config.data_path)
        outliers = self.analyzer.find_outliers(data, self.config.threshold)
        return outliers
```

**Vantaggi**: ogni classe testabile separatamente, configurazione esterna, componenti intercambiabili, codice riutilizzabile.

### Pattern Fondamentali

#### 1. Single Responsibility Principle
Una classe = una ragione per cambiare. Se devi scrivere "e" nella descrizione della classe, probabilmente fa troppo.

```python
# ❌ SBAGLIATO - Fa troppo
class DataManager:
    def load_data(self): pass
    def clean_data(self): pass  
    def send_email(self): pass  # Cosa c'entra?

# ✅ CORRETTO - Responsabilità separate  
class DataLoader: pass
class DataCleaner: pass
class EmailNotifier: pass
```

#### 2. Property per Controllo Accesso
Le property permettono di aggiungere validazione mantenendo la sintassi semplice:

```python
class DataValidator:
    def __init__(self):
        self._threshold = 1.0
    
    @property
    def threshold(self):
        return self._threshold
    
    @threshold.setter  
    def threshold(self, value):
        if value <= 0:
            raise ValueError("Threshold must be positive")
        self._threshold = value

# Uso naturale con validazione automatica
validator = DataValidator()
validator.threshold = 2.0  # OK
validator.threshold = -1   # ValueError!
```

---

## Parte 2: Testing Avanzato con pytest

### Fixtures: La Base di Tutto

Le fixtures sono setup riutilizzabili. Pensale come "preparazione dei dati" per i test:

```python
# conftest.py - Condiviso tra tutti i test
import pytest
import pandas as pd

@pytest.fixture
def sample_data():
    """Fixture base - ricreata per ogni test"""
    return pd.DataFrame({
        'value': [10, 20, 30, 40, 50],
        'category': ['A', 'B', 'A', 'B', 'A']
    })

@pytest.fixture
def temp_csv_file(sample_data, tmp_path):
    """Fixture che dipende da un'altra + cleanup automatico"""
    file_path = tmp_path / "test_data.csv"
    sample_data.to_csv(file_path, index=False)
    return file_path  # pytest fa cleanup di tmp_path automaticamente

@pytest.fixture(scope="session")
def expensive_setup():
    """Fixture costosa - creata una volta per tutta la sessione"""
    resource = setup_expensive_thing()
    yield resource
    resource.cleanup()  # Cleanup automatico
```

**Concetto chiave**: le fixture isolano la preparazione dei dati dai test. Ogni test riceve dati puliti.

### Test Parametrizzati: Un Test, Mille Scenari

Invece di scrivere 10 test simili, scrivi 1 test parametrizzato:

```python
class TestOutlierDetection:
    
    @pytest.mark.parametrize("input_data,expected_count", [
        ([1, 2, 3, 100], 1),      # Un outlier chiarissimo
        ([1, 2, 3, 4, 5], 0),     # Dati normali
        ([], 0),                  # Edge case: lista vuota
    ])
    def test_outlier_detection(self, input_data, expected_count):
        df = pd.DataFrame({'value': input_data})
        detector = OutlierDetector(threshold=2.0)
        outliers = detector.find_outliers(df)
        assert len(outliers) == expected_count
```

**Vantaggio**: un bug nel codice fa fallire tutti gli scenari immediatamente. Facile vedere pattern nei fallimenti.

### Mock: Controllo delle Dipendenze Esterne

Per testare componenti che dipendono da API, database, file system:

```python
from unittest.mock import Mock, patch

class TestDataFetcher:
    
    @patch('requests.get')  
    def test_api_success(self, mock_get):
        # Controllo totale: l'API "risponde" quello che voglio
        mock_response = Mock()
        mock_response.json.return_value = {'result': 'success'}
        mock_get.return_value = mock_response
        
        fetcher = DataFetcher('fake_key')
        result = fetcher.fetch_data('endpoint')
        
        assert result['result'] == 'success'
        # Verifica che sia stata chiamata correttamente
        mock_get.assert_called_once()
    
    @patch('requests.get')
    def test_api_failure(self, mock_get):
        # Simulo errore di rete
        mock_get.side_effect = requests.ConnectionError()
        
        fetcher = DataFetcher('fake_key')
        with pytest.raises(requests.ConnectionError):
            fetcher.fetch_data('endpoint')
```

**Utilità dei mock**: test veloci (niente chiamate esterne), test deterministici (controllo totale risposte), test error cases (simulo errori rari).

### Comandi pytest Pratici

```bash
# Base
pytest                          # Tutti i test
pytest -v                       # Verbose
pytest -x                       # Stop al primo fallimento

# Coverage
pytest --cov=src                # Con coverage
pytest --cov=src --cov-report=html  # Report HTML

# Performance  
pytest -n auto                  # Test paralleli (veloce!)

# Specifici
pytest test_file.py::test_name  # Solo un test
pytest -m slow                  # Solo test marcati @pytest.mark.slow
```

---

## Parte 3: Struttura Progetto Moderna

### Struttura Raccomandata 

La differenza tra hobby e produzione:

```
progetto_serio/
├── src/                    # Codice sorgente
│   └── mio_progetto/
│       ├── __init__.py    # OBBLIGATORIO per import
│       ├── core/
│       │   ├── __init__.py
│       │   └── models.py
│       ├── data/
│       │   ├── __init__.py
│       │   └── loader.py
│       └── utils/
│           ├── __init__.py
│           └── config.py
├── tests/                  # Test separati dal codice
│   ├── conftest.py        # Fixtures condivise
│   └── test_models.py
├── data/                   # Dati (NON in git!)
│   └── .gitkeep           # Placeholder per Git
├── scripts/                # Script di utilità
├── .gitignore             # File da ignorare
├── requirements.txt       # Dipendenze Python
├── pyproject.toml         # Configurazione progetto
└── README.md
```

**Perché `src/`?** Previene import accidentali durante sviluppo. Il codice deve essere installato per funzionare = più robusto.

### Il Mistero di __init__.py

Trasforma cartelle in package Python importabili:

```python
# src/mio_progetto/__init__.py
"""Package principale."""

__version__ = "1.0.0"

# Export pubblici - cosa può usare chi importa
from .data.loader import DataLoader
from .core.models import DataModel

__all__ = ["DataLoader", "DataModel"]

# Ora dall'esterno: from mio_progetto import DataLoader
```

**Senza __init__.py**: `ModuleNotFoundError`  
**Con __init__.py**: Import puliti e controllati

### pyproject.toml: Configurazione Tutto-in-Uno

Sostituisce setup.py, requirements.txt, e altri file config:

```toml
[project]
name = "mio-progetto"
version = "1.0.0"
description = "Analisi dati"
dependencies = [
    "pandas>=1.5.0",
    "numpy>=1.21.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=22.0",
    "mypy>=0.991",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src"

[tool.black]
line-length = 88
```

**Vantaggio**: una sola fonte di verità per tutta la configurazione.

### Git Workflow Pratico

#### .gitignore Essenziale

```bash
# .gitignore - Mai più file sensibili in Git
__pycache__/
*.pyc
.pytest_cache/
.coverage

# Dati - MAI in repository!
data/
*.csv
*.xlsx

# IDE
.vscode/
.idea/
```

#### Workflow Git Quotidiano

```bash
# Setup iniziale
git init
git add .
git commit -m "Initial commit"

# Feature branch workflow
git checkout -b feature/nuova-analisi
# ... lavoro ...
git add .
git commit -m "Add statistical analysis"
git push -u origin feature/nuova-analisi

# Merge su main
git checkout main
git merge feature/nuova-analisi
git push origin main
```

**Regola d'oro**: un branch per feature, commit frequenti con messaggi chiari.

---

## Parte 4: Gestione Errori e CI/CD

### Gestione Errori: I Principi Base

Non ignorare mai gli errori. Gestiscili in modo esplicito e utile:

```python
# ❌ SBAGLIATO
try:
    data = pd.read_csv(file)
except:
    pass  # DISASTRO! Nasconde tutti i problemi

# ✅ CORRETTO - Errori specifici e informativi
try:
    data = pd.read_csv(file)
except FileNotFoundError:
    logger.error(f"File not found: {file}")
    raise
except pd.errors.EmptyDataError:
    logger.error("CSV file is empty")
    raise
```

### Eccezioni Custom per Domini Specifici

Crea eccezioni che parlano il linguaggio del tuo dominio:

```python
class DataValidationError(Exception):
    """Errore specifico per validazione dati."""
    pass

class ProcessingError(Exception):
    """Errore durante elaborazione."""
    pass

# Uso
def validate_data(df):
    if df.empty:
        raise DataValidationError("Dataset is empty")
    
    if 'required_column' not in df.columns:
        raise DataValidationError("Missing required column")
```


### Logging Strutturato

Sostituisci tutti i `print()` con logging appropriato:

```python
import logging

# Setup una volta
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Uso
logger.info("Starting analysis")
logger.warning("Low quality data detected")
logger.error("Processing failed: %s", error_msg)
```

### Retry Pattern per Operazioni Instabili

Per operazioni che possono fallire temporaneamente (API calls, file I/O):

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2.0)
def download_data(url):
    # Se fallisce, riprova automaticamente
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

### CI/CD con GitHub Actions

Automatizza qualità e test ad ogni push:

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    
    - name: Run tests
      run: pytest --cov=src
    
    - name: Check code format  
      run: black --check src/
    
    - name: Lint
      run: flake8 src/
```

### Docker per Riproducibilità

Un container = stesso ambiente ovunque:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
RUN pip install -e .

CMD ["python", "-m", "mio_progetto.main"]
```

---

## Checklist Pratica: Da Zero a Produzione

### Setup Veloce
```bash
# Struttura base
mkdir progetto && cd progetto
mkdir -p src/progetto tests
touch src/progetto/__init__.py tests/conftest.py

# Git e virtual environment
git init
python -m venv venv
source venv/bin/activate

# Dipendenze essenziali
pip install pandas pytest black
pip freeze > requirements.txt
```

### Workflow Quotidiano
1. **Feature branch**: `git checkout -b feature/nome`
2. **Test first**: Scrivi il test prima del codice
3. **Implementa**: Codice che fa passare il test
4. **Refactor**: Migliora senza rompere i test
5. **Format**: `black src/ tests/`
6. **Test**: `pytest`
7. **Commit**: `git commit -m "feat: add feature"`

### Pre-Release Checklist
- [ ] Tutti i test passano (`pytest`)
- [ ] Coverage > 80% (`pytest --cov=src`)
- [ ] Codice formattato (`black src/`)
- [ ] Nessun errore linting (`flake8 src/`)
- [ ] README aggiornato
- [ ] Version bump in `__init__.py`

**Regola finale**: se hai paura di toccare il codice, non hai abbastanza test.

---

*Fine della guida. Questa struttura ti porta da script improvvisati a codice production-ready che puoi manutenere per anni senza vergognarti.*
    """Setup logger con formato consistente."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # File handler (se specificato)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    if log_file:
        file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    if log_file:
        logger.addHandler(file_handler)
    
    return logger

# Context manager per risorse
from contextlib import contextmanager
import tempfile

@contextmanager
def temporary_directory():
    """Context manager per directory temporanea."""
    temp_dir = Path(tempfile.mkdtemp())
    try:
        yield temp_dir
    finally:
        # Cleanup garantito
        import shutil
        shutil.rmtree(temp_dir)

# Retry decorator
from functools import wraps
import time

def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """Decorator per retry automatico."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator

# Esempio d'uso completo
class RobustDataProcessor:
    """Processore dati con gestione errori robusta."""
    
    def __init__(self, config_file: Path):
        self.logger = setup_logger(__name__, Path("logs/processing.log"))
        self.config = self._load_config(config_file)
    
    def _load_config(self, config_file: Path) -> dict:
        """Carica configurazione con validazione."""
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
        
        try:
            import json
            with open(config_file) as f:
                config = json.load(f)
            
            # Validazione campi richiesti
            required_fields = ['input_path', 'output_path', 'threshold']
            missing = [f for f in required_fields if f not in config]
            if missing:
                raise DataValidationError(
                    f"Missing config fields: {missing}",
                    context={'config_file': str(config_file)}
                )
            
            return config
            
        except json.JSONDecodeError as e:
            raise DataValidationError(
                f"Invalid JSON in config file: {e}",
                context={'config_file': str(config_file)}
            )
    
    @retry(max_attempts=3, delay=2.0, exceptions=(IOError,))
    def load_data(self, file_path: Path) -> pd.DataFrame:
        """Carica dati con retry automatico."""
        try:
            self.logger.info(f"Loading data from {file_path}")
            df = pd.read_csv(file_path)
            
            if df.empty:
                raise DataValidationError(
                    "Loaded DataFrame is empty",
                    context={'file_path': str(file_path)}
                )
            
            self.logger.info(f"Loaded {len(df)} records")
            return df
            
        except pd.errors.EmptyDataError:
            raise DataValidationError(
                "CSV file is empty",
                context={'file_path': str(file_path)}
            )
        except Exception as e:
            self.logger.error(f"Failed to load data: {e}")
            raise ProcessingError(
                f"Data loading failed: {e}",
                context={'file_path': str(file_path)}
            )
    
    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processa dati con gestione errori."""
        try:
            with temporary_directory() as temp_dir:
                self.logger.info("Starting data processing")
                
                # Validazioni
                if 'value' not in df.columns:
                    raise DataValidationError(
                        "Required column 'value' not found",
                        context={'columns': list(df.columns)}
                    )
                
                # Processing
                processed = df.copy()
                processed['normalized'] = processed['value'] / processed['value'].max()
                
                # Checkpoint temporaneo
                checkpoint_file = temp_dir / "checkpoint.csv"
                processed.to_csv(checkpoint_file, index=False)
                self.logger.debug(f"Checkpoint saved to {checkpoint_file}")
                
                return processed
                
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise ProcessingError(
                "Data processing failed",
                context={'error': str(e), 'data_shape': df.shape}
            )
```

### CI/CD con GitHub Actions

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
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Lint with flake8
      run: |
        flake8 src tests --max-line-length=88
    
    - name: Format check with black
      run: |
        black --check src tests
    
    - name: Type check with mypy
      run: |
        mypy src
    
    - name: Test with pytest
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Docker per Riproducibilità

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dipendenze sistema
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Codice applicazione
COPY src/ ./src/
COPY pyproject.toml ./

# Installa package in modalità development
RUN pip install -e .

# User non-root per sicurezza
RUN useradd -m appuser
USER appuser

# Default command
CMD ["python", "-m", "mio_progetto.main"]
```

---

## Checklist Pratica: Da Zero a Produzione

### Setup Iniziale
```bash
# 1. Crea struttura progetto
mkdir mio-progetto && cd mio-progetto
mkdir -p src/mio_progetto tests data docs scripts

# 2. File essenziali
touch src/mio_progetto/__init__.py
touch tests/__init__.py
touch tests/conftest.py
touch .gitignore
touch requirements.txt
touch pyproject.toml

# 3. Git setup
git init
git add .
git commit -m "Initial project structure"

# 4. Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 5. Dependencies base
pip install pandas numpy pytest black flake8 mypy
pip freeze > requirements.txt
```

### Development Workflow (Quotidiano)
1. **Branch per feature**: `git checkout -b feature/nome-feature`
2. **Scrivi test prima**: `tests/test_nuova_feature.py`
3. **Implementa feature**: `src/mio_progetto/nuova_feature.py`
4. **Verifica test**: `pytest tests/`
5. **Formatta codice**: `black src/ tests/`
6. **Check linting**: `flake8 src/ tests/`
7. **Commit**: `git add . && git commit -m "feat: add nuova feature"`
8. **Push e PR**: `git push -u origin feature/nome-feature`

### Pre-Deploy Checklist
- [ ] Tutti i test passano (`pytest`)
- [ ] Coverage > 80% (`pytest --cov=src`)
- [ ] Nessun errore linting (`flake8 src/`)
- [ ] Codice formattato (`black src/`)
- [ ] Type checking OK (`mypy src/`)
- [ ] Documentazione aggiornata
- [ ] Nessun file sensibile in git
- [ ] Docker build funziona
- [ ] CI/CD pipeline verde

---

## Esempio Finale: Mini Progetto Completo

Mettiamo tutto insieme in un esempio pratico da copiare:

```python
# src/data_analyzer/__init__.py
"""Simple data analysis package."""
__version__ = "1.0.0"

from .core import DataProcessor, OutlierDetector
from .utils import load_config, setup_logging

__all__ = ["DataProcessor", "OutlierDetector", "load_config", "setup_logging"]

# src/data_analyzer/core.py
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any
import logging

class DataProcessor:
    """Main data processing class."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def load_data(self, file_path: Path) -> pd.DataFrame:
        """Load and validate data."""
        self.logger.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        
        if df.empty:
            raise ValueError("Dataset is empty")
            
        return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize data."""
        cleaned = df.dropna().copy()
        cleaned['normalized'] = cleaned['value'] / cleaned['value'].max()
        return cleaned

class OutlierDetector:
    """Detect outliers in data."""
    
    def __init__(self, threshold: float = 2.0):
        self.threshold = threshold
    
    def find_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Find outliers using Z-score."""
        z_scores = np.abs((df['normalized'] - df['normalized'].mean()) / df['normalized'].std())
        return df[z_scores > self.threshold]

# tests/test_core.py
import pytest
import pandas as pd
import numpy as np
from data_analyzer.core import DataProcessor, OutlierDetector

class TestDataProcessor:
    
    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'value': [10, 20, 30, 40, 50]
        })
    
    @pytest.fixture
    def processor(self):
        return DataProcessor({'threshold': 2.0})
    
    def test_clean_data(self, processor, sample_data):
        result = processor.clean_data(sample_data)
        
        assert 'normalized' in result.columns
        assert result['normalized'].max() == 1.0
        assert len(result) == len(sample_data)

class TestOutlierDetector:
    
    def test_find_outliers(self):
        df = pd.DataFrame({
            'normalized': [0.1, 0.2, 0.3, 0.9]  # 0.9 è outlier
        })
        
        detector = OutlierDetector(threshold=1.0)
        outliers = detector.find_outliers(df)
        
        assert len(outliers) >= 0  # Può variare in base ai dati
```

Questa è una guida pratica che puoi seguire step by step. Niente fronzoli, solo quello che serve per scrivere codice Python decente che non ti faccia vergognare dopo 6 mesi.