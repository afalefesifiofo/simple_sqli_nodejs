import requests
import time
import statistics
import random
import string
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import numpy as np
"""
Write a script that starts multiple clients in parallel with each client that makes 100 authentication requests per second. For each request, a random value of the email and password must be generated.
Use the script you wrote above to get the metrics (mean latency, 95th and 99th percentiles) to evaluate from which number of clients, latency and percentiles drop by more than 40% (compared to when there is only one client).


"""
# Configuration
URL = "http://localhost:3000/auth"  # Endpoint to test
DURATION = 3  # Duration of each test in seconds
REQUESTS_PER_CLIENT = 100  # Number of requests per client per second
MAX_CLIENTS = 20  # Maximum number of parallel clients to test
DROP_THRESHOLD = 0.4  # 40% degradation threshold

def generate_random_email_and_password():
    """Generate a random email and password."""
    email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + "@example.com"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return email, password

def send_auth_request():
    """Send a single authentication request with random credentials and measure latency."""
    email, password = generate_random_email_and_password()
    start_time = time.time()
    response = requests.post(URL, json={"username": email, "password": password})
    end_time = time.time()
    latency = end_time - start_time
    return latency

def run_client(client_id):
    """Run a single client sending 100 requests per second for the duration."""
    latencies = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=REQUESTS_PER_CLIENT) as executor:
        while time.time() - start_time < DURATION:
            futures = [executor.submit(send_auth_request) for _ in range(REQUESTS_PER_CLIENT)]
            for future in futures:
                latencies.append(future.result())
            time.sleep(1)  # Wait for the next second
    return latencies

def analyze_results(latencies):
    """Analyze latency data to calculate mean, 95th, and 99th percentiles."""
    avg_latency = statistics.mean(latencies)
    percentile_95 = statistics.quantiles(latencies, n=100)[94]  # 95th percentile
    percentile_99 = statistics.quantiles(latencies, n=100)[98]  # 99th percentile
    return avg_latency, percentile_95, percentile_99

def evaluate_performance():
    """Run tests with increasing numbers of clients and evaluate performance drop."""
    results = {}
    base_metrics = None

    for num_clients in range(1, MAX_CLIENTS + 1):
        print(f"Testing with {num_clients} client(s)...")
        latencies = []
        with ThreadPoolExecutor(max_workers=num_clients) as executor:
            futures = [executor.submit(run_client, client_id) for client_id in range(num_clients)]
            for future in futures:
                latencies.extend(future.result())
        
        avg, p95, p99 = analyze_results(latencies)
        results[num_clients] = [avg, p95, p99]
        print(f"Results for {num_clients} client(s): Avg={avg:.4f}s, 95th={p95:.4f}s, 99th={p99:.4f}s")

        # Record base metrics for single client
        if num_clients == 1:
            base_metrics = (avg, p95, p99)

        # Check if metrics dropped by more than 40%
        if base_metrics:
            avg_drop = (base_metrics[0] - avg) / base_metrics[0]
            p95_drop = (base_metrics[1] - p95) / base_metrics[1]
            p99_drop = (base_metrics[2] - p99) / base_metrics[2]
            if avg_drop < -DROP_THRESHOLD or p95_drop < -DROP_THRESHOLD or p99_drop < -DROP_THRESHOLD:
                print(f"Performance dropped by more than 40% with {num_clients} clients.")
                break

    return results

def plot_results(results):
    """Plot the results of latency metrics."""
    clients = list(results.keys())
    avg_latencies = [results[c][0] for c in clients]
    p95_latencies = [results[c][1] for c in clients]
    p99_latencies = [results[c][2] for c in clients]

    x = np.arange(len(clients))
    width = 0.2

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width, avg_latencies, width, label='Mean Latency')
    ax.bar(x, p95_latencies, width, label='95th Percentile')
    ax.bar(x + width, p99_latencies, width, label='99th Percentile')

    ax.set_xlabel("Number of Clients")
    ax.set_ylabel("Latency (seconds)")
    ax.set_title("Authentication Performance by Number of Clients")
    ax.set_xticks(x)
    ax.set_xticklabels(clients)
    ax.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    performance_results = evaluate_performance()
    plot_results(performance_results)
