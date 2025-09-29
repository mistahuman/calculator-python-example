import pandas as pd

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
    data["normalized"] = data["value"] / 100

    # Logica business e I/O mescolati
    if data["normalized"].mean() > THRESHOLD:
        print("Significant!")
        results["status"] = "sig"

    # Nessuna gestione errori
    with open("results.txt", "w") as f:
        f.write(str(results))
