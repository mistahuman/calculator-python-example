# Corso Python: Refactoring di Codice Biomedicale
## Materiale Completo per Sessione Hands-On di 2 Ore

---

## 📋 Struttura del Corso (2 ore)

### Timeline Dettagliata
- **00:00-00:30** - Modulo 1: Gestione Classi e OOP (30 min)
- **00:30-01:00** - Modulo 2: Testing con pytest (30 min)
- **01:00-01:30** - Modulo 3: PEP8 e Scrittura Sicura (30 min)
- **01:30-02:00** - Modulo 4: Esempio Pratico Integrato (30 min)

---

## Modulo 1: Gestione Classi Python (30 minuti)

### 🎯 Obiettivi
- Trasformare codice procedurale in object-oriented
- Applicare principi SOLID (Single Responsibility, Separation of Concerns)
- Implementare pattern di refactoring comuni

### 📝 Esempio Completo: Pipeline Analisi Dati

#### PRIMA - Script Monolitico (Problemi Comuni)
```python
# analisi_biomedica.py - Codice tipico da ricercatore
import pandas as pd
import numpy as np

# Variabili globali
DATA_PATH = "/data/patients.csv"
THRESHOLD = 0.05
data = None
results = {}

def analyze():
    global data, results
    
    # Tutto mescolato insieme
    print("Loading...")
    data = pd.read_csv(DATA_PATH)
    data = data.dropna()
    
    # Magic numbers ovunque
    data['normalized'] = data['value'] / 100
    
    # Logica business e I/O mescolati
    if data['normalized'].mean() > THRESHOLD:
        print("Significant!")
        results['status'] = 'sig'
    
    # Nessuna gestione errori
    with open("results.txt", 'w') as f:
        f.write(str(results))
```

#### DOPO - Architettura a Classi
```python
from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass
import logging

@dataclass
class PipelineConfig:
    """Configurazione centralizzata e validata"""
    input_path: Path
    output_path: Path
    significance_threshold: float = 0.05
    
    def validate(self) -> None:
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input not found: {self.input_path}")

class DataLoader:
    """Single Responsibility: Caricamento Dati"""
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def load_csv(self, path: Path) -> pd.DataFrame:
        try:
            self.logger.info(f"Loading from {path}")
            return pd.read_csv(path)
        except Exception as e:
            self.logger.error(f"Load failed: {e}")
            raise

class DataProcessor:
    """Single Responsibility: Processamento"""
    def __init__(self, config: PipelineConfig):
        self.config = config
    
    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        df['normalized'] = df['value'] / df['value'].max()
        return df

class StatisticalAnalyzer:
    """Single Responsibility: Analisi"""
    def analyze_significance(self, df: pd.DataFrame, threshold: float) -> Dict:
        mean_val = df['normalized'].mean()
        return {
            'mean': mean_val,
            'significant': mean_val > threshold
        }

class BiomedicalPipeline:
    """Orchestratore con Dependency Injection"""
    def __init__(self, config: PipelineConfig,
                 loader: Optional[DataLoader] = None):
        self.config = config
        self.logger = self._setup_logger()
        self.loader = loader or DataLoader(self.logger)
        self.processor = DataProcessor(config)
        self.analyzer = StatisticalAnalyzer()
    
    def run(self) -> Dict[str, Any]:
        # Pipeline chiara e testabile
        data = self.loader.load_csv(self.config.input_path)
        data = self.processor.normalize(data)
        results = self.analyzer.analyze_significance(
            data, self.config.significance_threshold
        )
        return results
```

### 🔑 Principi Chiave del Refactoring

1. **Single Responsibility Principle**: Ogni classe ha UNA responsabilità
2. **Dependency Injection**: Componenti intercambiabili per testing
3. **Configuration Management**: Niente valori hardcoded
4. **Error Handling**: Gestione errori robusta
5. **Logging**: Tracciabilità completa

---

## Modulo 2: Testing con pytest (30 minuti)

### 🎯 Obiettivi
- Scrivere test PRIMA di refactorizzare (characterization tests)
- Implementare test unitari e di integrazione
- Usare mock per dipendenze esterne

### 📝 Esempi Pratici

#### 1. Characterization Test per Codice Legacy
```python
import pytest
import pandas as pd
from pathlib import Path
import tempfile

class TestLegacyBehavior:
    """Cattura il comportamento attuale prima del refactoring"""
    
    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            'patient_id': [1, 2, 3],
            'value': [10, 20, 30],
            'group': ['A', 'B', 'A']
        })
    
    @pytest.fixture
    def temp_csv(self, sample_data):
        """File temporaneo per test"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            sample_data.to_csv(f.name, index=False)
            path = Path(f.name)
        yield path
        path.unlink()  # Cleanup
    
    def test_legacy_output(self, temp_csv, monkeypatch):
        """Verifica che l'output rimanga consistente"""
        import legacy_code
        monkeypatch.setattr(legacy_code, 'DATA_PATH', str(temp_csv))
        
        result = legacy_code.analyze()
        
        # Asserzioni sul comportamento attuale
        assert isinstance(result, dict)
        assert 'status' in result
```

#### 2. Test Unitari per Codice Refactorizzato
```python
from unittest.mock import Mock, patch
import pandas as pd

class TestDataProcessor:
    @pytest.fixture
    def processor(self):
        config = Mock(significance_threshold=0.05)
        return DataProcessor(config)
    
    def test_normalize_values(self, processor):
        df = pd.DataFrame({'value': [10, 20, 30]})
        result = processor.normalize(df)
        
        assert result['normalized'].max() == 1.0
        assert result['normalized'].min() == 1/3
    
    @pytest.mark.parametrize("input_val,expected", [
        ([10, 20], [0.5, 1.0]),
        ([5, 5, 5], [1.0, 1.0, 1.0]),
    ])
    def test_normalize_parametrized(self, processor, input_val, expected):
        df = pd.DataFrame({'value': input_val})
        result = processor.normalize(df)
        assert list(result['normalized']) == expected
```

#### 3. Mock per Servizi Esterni
```python
@patch('docker.from_env')
def test_ml_model_docker(mock_docker):
    """Mock container Docker per ML"""
    mock_container = Mock()
    mock_container.run.return_value = b'{"prediction": 0.95}'
    mock_docker.return_value.containers = mock_container
    
    # Test del codice che usa Docker
    result = analyze_with_ml_model("data")
    assert result['prediction'] == 0.95

@patch('requests.post')
def test_external_api(mock_post):
    """Mock API REST"""
    mock_post.return_value.json.return_value = {'score': 0.87}
    
    result = call_biomedical_api("sample")
    assert result['score'] == 0.87
```

### 🛠️ Comandi pytest Essenziali
```bash
# Coverage report
pytest --cov=module --cov-report=html

# Test specifici
pytest test_file.py::TestClass::test_method

# Test paralleli
pytest -n auto

# Con output verbose
pytest -v -s
```

---

## Modulo 3: PEP8 e Scrittura Sicura (30 minuti)

### 🎯 Obiettivi
- Applicare standard PEP8 per leggibilità
- Implementare type hints per sicurezza
- Gestire errori e logging professionalmente

### 📝 Esempi "Prima e Dopo"

#### 1. Naming e Formatting
```python
# ❌ SBAGLIATO
def CalcBMI(W,H):
    BMIval=W/(H**2)
    return BMIval

# ✅ CORRETTO
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calcola Body Mass Index."""
    bmi_value = weight_kg / (height_m ** 2)
    return bmi_value
```

#### 2. Type Hints Scientifici
```python
from typing import List, Dict, Optional, Tuple
import numpy as np
import pandas as pd
from numpy.typing import NDArray

def analyze_biomarkers(
    data: pd.DataFrame,
    markers: List[str],
    threshold: float = 0.05
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Type hints per dati biomedici."""
    filtered = data[data['p_value'] < threshold]
    stats = {m: data[m].mean() for m in markers}
    return filtered, stats

def process_genome_data(
    matrix: NDArray[np.float64],
    gene_ids: List[str]
) -> Dict[str, NDArray]:
    """Type hints per array NumPy."""
    return {
        'expression': np.mean(matrix, axis=1),
        'variance': np.var(matrix, axis=1)
    }
```

#### 3. Validazione con Pydantic
```python
from pydantic import BaseModel, Field, validator
from enum import Enum

class BloodType(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    O_POS = "O+"

class PatientData(BaseModel):
    """Modello validato automaticamente"""
    patient_id: str = Field(regex="^P[0-9]{6}$")
    age: int = Field(ge=0, le=120)
    weight_kg: float = Field(gt=0, le=300)
    blood_type: BloodType
    
    @validator('patient_id')
    def validate_id(cls, v):
        if not v.startswith('P'):
            raise ValueError('Invalid patient ID')
        return v

# Uso con validazione automatica
patient = PatientData(
    patient_id="P123456",
    age=45,
    weight_kg=75,
    blood_type="A+"
)
```

#### 4. Logging Professionale
```python
# ❌ SBAGLIATO
print("Starting analysis...")
print(f"Result: {result}")

# ✅ CORRETTO
import logging
from logging.handlers import RotatingFileHandler

def setup_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    
    # File handler con rotation
    handler = RotatingFileHandler(
        'analysis.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

logger = setup_logger()
logger.info("Starting analysis", extra={'context': 'biomedical'})
```

#### 5. Gestione Sicura
```python
import os
from pathlib import Path
from dotenv import load_dotenv

# ❌ SBAGLIATO
API_KEY = "sk-1234567890"

# ✅ CORRETTO
load_dotenv()

class SecureConfig:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("Missing API_KEY")

# Path traversal prevention
def safe_file_access(user_input: str, base_dir: Path) -> Path:
    base = base_dir.resolve()
    requested = (base / user_input).resolve()
    
    if not str(requested).startswith(str(base)):
        raise ValueError(f"Invalid path: {user_input}")
    
    return requested
```

---

## Modulo 4: Esempio Integrato Step-by-Step (30 minuti)

### 🎯 Esercizio Pratico Completo

#### Script Iniziale da Refactorizzare (70 righe)
```python
# lab_analysis.py - Da trasformare insieme
import pandas as pd
import numpy as np

# TODO: Problemi da risolvere:
# 1. Variabili globali
# 2. No error handling
# 3. No tests
# 4. Mixed concerns
# 5. Magic numbers

data_file = "lab_results.csv"
threshold = 2.5
results = []

def process():
    # Load data
    data = pd.read_csv(data_file)
    
    # Clean - TODO: extract method
    data = data.dropna()
    data = data[data['value'] > 0]
    
    # Calculate - TODO: separate logic
    data['zscore'] = (data['value'] - data['value'].mean()) / data['value'].std()
    
    # Analyze - TODO: create class
    abnormal = data[abs(data['zscore']) > threshold]
    
    print(f"Found {len(abnormal)} abnormal results")
    
    # Save - TODO: error handling
    abnormal.to_csv("abnormal.csv")
    
    return abnormal

if __name__ == "__main__":
    process()
```

### ✅ Checklist di Refactoring

1. **[ ] Estrai configurazione**
   - Crea classe Config con validazione
   - Rimuovi magic numbers

2. **[ ] Separa responsabilità**
   - DataLoader per I/O
   - DataCleaner per pulizia
   - StatisticalAnalyzer per calcoli
   - ResultExporter per output

3. **[ ] Aggiungi type hints**
   - Parametri funzioni
   - Return types
   - Variabili classe

4. **[ ] Implementa error handling**
   - Try/except specifici
   - Custom exceptions
   - Logging invece di print

5. **[ ] Scrivi test**
   - Unit test per ogni metodo
   - Integration test per pipeline
   - Mock per I/O

6. **[ ] Documenta**
   - Docstrings per classi/metodi
   - Type hints completi
   - README con esempi

---

## 📊 Metriche di Successo del Refactoring

### Prima del Refactoring
- 🔴 Cyclomatic Complexity: 12+
- 🔴 Test Coverage: 0%
- 🔴 Type Coverage: 0%
- 🔴 Maintainability Index: 40/100

### Dopo il Refactoring
- 🟢 Cyclomatic Complexity: 3-4
- 🟢 Test Coverage: 90%+
- 🟢 Type Coverage: 100%
- 🟢 Maintainability Index: 85/100

---

## 🛠️ Setup Ambiente di Sviluppo

### Requirements
```txt
# requirements.txt
pandas>=1.3.0
numpy>=1.21.0
scipy>=1.7.0
pytest>=7.0.0
pytest-cov>=3.0.0
pytest-mock>=3.6.0
pydantic>=1.9.0
python-dotenv>=0.19.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.940
```

### Pre-commit Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
  
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        args: [--max-line-length=88]
```

### VS Code Settings
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true
}
```

---

## 📚 Risorse Aggiuntive

### Cheat Sheet Comandi

```bash
# Testing
pytest                          # Run all tests
pytest --cov=.                 # With coverage
pytest -v -s                   # Verbose with prints
pytest -n auto                 # Parallel execution

# Code Quality
black .                        # Format code
isort .                       # Sort imports
flake8 .                      # Check style
mypy .                        # Type checking

# Documentation
pdoc --html module            # Generate docs
```

### Pattern di Refactoring Comuni

1. **Extract Method**: Codice duplicato → metodo riutilizzabile
2. **Extract Class**: Gruppo di metodi correlati → classe
3. **Replace Magic Number**: Costante hardcoded → configurazione
4. **Introduce Parameter Object**: Molti parametri → oggetto configurazione
5. **Replace Conditional with Polymorphism**: If/else complessi → strategy pattern

### Best Practices Biomedicali

1. **Data Privacy**: Mai loggare dati sensibili pazienti
2. **Audit Trail**: Log completo per compliance
3. **Validation**: Sempre validare range valori clinici
4. **Reproducibility**: Seed random, versioning dati
5. **Documentation**: Riferimenti a standard/protocolli

---

## 🎯 Esercitazione Finale (Homework)

### Progetto: Refactoring Pipeline Genomica

Trasformate questo script in codice production-ready:

```python
# genomic_analysis.py - DA REFACTORIZZARE
import pandas as pd

genes = pd.read_csv("genes.csv")
genes = genes[genes['expression'] > 100]
genes['log_expr'] = genes['expression'].apply(lambda x: np.log2(x))

significant = []
for gene in genes.iterrows():
    if gene[1]['log_expr'] > 5:
        significant.append(gene[1]['gene_id'])

print(f"Found {len(significant)} significant genes")

with open("results.txt", "w") as f:
    for g in significant:
        f.write(g + "\n")
```

**Requisiti:**
1. Separare in almeno 3 classi
2. Aggiungere type hints completi
3. Implementare error handling
4. Scrivere almeno 5 test
5. Documentare con docstrings
6. Configurazione esterna
7. Logging invece di print

---

## 📧 Contatti e Supporto

Per domande durante il tutoring del progetto di refactoring:
- Consultate prima questo materiale
- Usate i pattern e gli esempi forniti
- Applicate la checklist di refactoring
- Testate incrementalmente ogni modifica

**Ricordate**: Il refactoring è un processo iterativo. Non cercate la perfezione al primo tentativo, ma migliorate progressivamente la qualità del codice mantenendo sempre i test verdi!

---

*Materiale del corso creato per sviluppatori con esperienza base che faranno da tutor in progetti di refactoring di codice biomedicale. Versione 1.0 - Dicembre 2024*