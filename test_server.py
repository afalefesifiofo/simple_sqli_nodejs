import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import numpy as np

# Configuration
URL = "http://localhost:3000/auth"  # Endpoint à tester
EMAIL = "test@example.com"
PASSWORD = "password123"
DURATION = 30  # Durée du test en secondes
N_REQUESTS = [1, 50, 100]  # Nombre de requêtes par seconde

def send_auth_request():
    """Envoie une requête d'authentification et mesure la latence."""
    start_time = time.time()
    response = requests.post(URL, json={"username": EMAIL, "password": PASSWORD})
    end_time = time.time()
    latency = end_time - start_time
    return latency

def run_test(n_requests_per_second):
    """Exécute un test pour un nombre donné de requêtes par seconde."""
    latencies = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=n_requests_per_second) as executor:
        while time.time() - start_time < DURATION:
            futures = [executor.submit(send_auth_request) for _ in range(n_requests_per_second)]
            for future in futures:
                latencies.append(future.result())
            time.sleep(1)  # Attendre la prochaine seconde
    return latencies

def analyze_results(latencies):
    """Analyse les résultats pour extraire les métriques."""
    avg_latency = statistics.mean(latencies)
    percentile_95 = statistics.quantiles(latencies, n=100)[94]  # 95e percentile
    percentile_99 = statistics.quantiles(latencies, n=100)[98]  # 99e percentile
    return avg_latency, percentile_95, percentile_99

def plot_latency_results(latency_data, n_values, percentiles, title="Confronto delle latenze"):
    """
    Plotta un istogramma per confrontare le latenze medie e i percentili per diverse frequenze di richieste.
    
    Parameters:
    - latency_data (dict): Dizionario con le latenze, chiavi sono i valori di `n` (richieste/s), 
                           valori sono liste [media, 95° percentile, 99° percentile].
    - n_values (list): Lista di valori `n` usati per le richieste al secondo.
    - percentiles (list): Lista delle metriche (es. ["Media", "95° Percentile", "99° Percentile"]).
    - title (str): Titolo del grafico.
    """
    x = np.arange(len(percentiles))
    width = 0.25  # Larghezza delle barre
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i, n in enumerate(n_values):
        offset = (i - len(n_values) / 2) * width + width / 2
        ax.bar(x + offset, latency_data[n], width, label=f"n={n}")
    
    # Etichette e titolo
    ax.set_xlabel("Metriche", fontsize=12)
    ax.set_ylabel("Latenza (secondi)", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(percentiles, fontsize=10)
    ax.legend(title="Frequenza (richieste/s)")
    
    plt.tight_layout()
    plt.show()

def main():
    results = {}
    for n in N_REQUESTS:
        print(f"Test avec {n} requêtes par seconde...")
        latencies = run_test(n)
        avg, p95, p99 = analyze_results(latencies)
        results[n] = [avg, p95, p99]
        print(f"Résultats pour {n} req/s: Moyenne={avg:.4f}s, 95ᵉ perc={p95:.4f}s, 99ᵉ perc={p99:.4f}s")
    return results

if __name__ == "__main__":
    data = main()
    print("Résultats finaux :", data)
    
    percentiles_example = ["Media", "95° Percentile", "99° Percentile"]
    plot_latency_results(data, N_REQUESTS, percentiles_example)
