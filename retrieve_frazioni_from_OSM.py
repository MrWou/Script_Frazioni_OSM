import requests
import json
import pandas as pd
import time
import os

# Percorso della cartella dello script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Percorso del file comuni.csv
CSV_FILE = os.path.join(BASE_DIR, "Codice ISTAT Comuni ER_update_07_2024.csv")

# Percorso di output per il file delle frazioni
OUTPUT_FILE = os.path.join(BASE_DIR, "Comuni ER con frazioni.csv")

def get_fractions_from_osm(city_name, max_retries=5, initial_retry_delay=5):
    url = "https://overpass.kumi.systems/api/interpreter"  # Usare sempre il primo endpoint
    retry_delay = initial_retry_delay
    
    for attempt in range(max_retries):
        try:
            print(f"Tentativo {attempt + 1} su {max_retries} per {city_name}")
            response = requests.get(url, params={'data': f"""
                [out:json];
                area["name"="{city_name}"]["boundary"="administrative"]["admin_level"="8"];
                (node["place"="village"](area);
                 node["place"="hamlet"](area);
                );
                out body; >;
                out skel qt;
            """}, timeout=10)  # Timeout massimo di 10 secondi
            
            response.raise_for_status()  # Solleva errore per codici 4xx o 5xx
            data = response.json()
            
            # Se i dati sono vuoti, passiamo oltre
            if 'elements' in data and len(data['elements']) > 0:
                return [
                    {
                        'city': city_name,
                        'name': element['tags']['name'],
                        'place_type': element['tags'].get('place', 'unknown'),
                        'latitude': element['lat'],
                        'longitude': element['lon']
                    }
                    for element in data.get('elements', []) if 'tags' in element and 'name' in element['tags']
                ]
            else:
                print(f"Nessun dato per {city_name}. Passo al prossimo comune.")
                return []  # Passa direttamente al comune successivo
        except requests.exceptions.RequestException as e:
            print(f"Errore: {e}. Riprovo tra {retry_delay} secondi...")
        
        time.sleep(retry_delay)
    
    print(f"Errore definitivo per {city_name} dopo {max_retries} tentativi.")
    return []  # Evita il crash, continua con il prossimo comune

# Leggere il file CSV con i comuni
df_comuni = pd.read_csv(CSV_FILE)
comuni_list = df_comuni["Denominazione Comune"].tolist()

# Recuperare le frazioni per tutti i comuni
all_fractions = []
for comune in comuni_list:
    print(f"Recupero frazioni per: {comune}")
    all_fractions.extend(get_fractions_from_osm(comune))
    time.sleep(2)  # Pausa ridotta a 2 secondi tra le richieste per ottimizzare i tempi

# Creare DataFrame finale
df_fractions = pd.DataFrame(all_fractions)

# Salvare il DataFrame in CSV nella stessa cartella dello script
df_fractions.to_csv(OUTPUT_FILE, index=False)

print(f"File salvato in: {OUTPUT_FILE}")

# Mostrare i risultati
df_fractions.head()
