Titolo del ProgettoGeoFrazioni ER: Estrazione Resiliente Frazioni Emilia-Romagna da OpenStreetMapDescrizione Breve (Short Description)Script Python avanzato per estrarre e georeferenziare massivamente le frazioni di tutti i comuni dell'Emilia-Romagna usando OpenStreetMap (Overpass API + Nominatim), con gestione automatica di failover server, anti-rate-limit e disambiguazione geografica.Contenuto del README.md (Copia e incolla questo blocco)Markdown# GeoFrazioni ER 🌍📍

**GeoFrazioni ER** è un tool Python progettato per estrarre in modo massivo e preciso l'elenco delle frazioni (`village` e `suburb`) per tutti i comuni dell'Emilia-Romagna, georeferenziandole con latitudine e longitudine.

Il progetto risolve le classiche criticità dello scraping su OpenStreetMap (timeout, omonimie internazionali, limiti API) utilizzando un **approccio ibrido a due stadi** e un sistema di **Failover Multi-Server**.

## 🚀 Caratteristiche Principali

* **Georeferenziazione Ibrida Blindata**: Utilizza prima **Nominatim** per identificare il Bounding Box esatto del comune (evitando errori come "Lugo, Spagna" invece di "Lugo, Ravenna") e poi **Overpass API** per estrarre i dati solo dentro quel perimetro.
* **Failover Multi-Server Automatico**: Include una lista di rotazione dei server Overpass (Tedesco, Francese, Russo, Kumi Systems). Se il server principale va in timeout (504) o da errore DNS, lo script passa automaticamente al successivo senza interrompere il processo.
* **Gestione Intelligente Rate Limit**: Algoritmo di *backoff* che mette in pausa lo script dinamicamente quando l'API segnala troppe richieste (Error 429), evitando il ban dell'IP.
* **Filtro Semantico**: 
    * Estrae `place=village` (frazioni vere).
    * Estrae `place=suburb` (frazioni costiere/urbane) solo dove necessario (es. Cervia), escludendoli automaticamente per i grandi capoluoghi (es. Bologna) per evitare di mappare i quartieri cittadini.

## 🛠️ Come Funziona

Il processo è diviso in due script per garantire stabilità e controllo:

1.  **Script 1 (`geocoding_step.py`)**: Legge l'elenco dei comuni ISTAT e interroga Nominatim per ottenere le coordinate esatte (Bounding Box) di ogni comune.
2.  **Script 2 (`extraction_step.py`)**: Legge i Bounding Box generati e scarica le frazioni da Overpass usando la rotazione dei server.

## 📋 Prerequisiti

* Python 3.x
* Librerie: `pandas`, `requests`

```bash
pip install pandas requests
📂 Struttura Dati OutputIl file CSV finale (Frazioni_ER_Finali_Complete.csv) conterrà:ProvinciaComuneFrazioneTipologiaLatitudineLongitudinePiacenzaBobbioMezzano Scottivillage44.xxx9.xxxRavennaCerviaPinarellasuburb44.xxx12.xxx⚠️ Note sull'UtilizzoQuesto script rispetta le Usage Policy di OpenStreetMap:Pausa di 1 secondo tra le richieste Nominatim.Pausa dinamica tra le richieste Overpass.User-Agent personalizzato.Usare con responsabilità e non parallelizzare le richieste per non sovraccaricare i server pubblici gratuiti.
### Prossimi Passaggi per GitHub
1.  Crea un file chiamato `requirements.txt` con dentro:
    ```text
    pandas
    requests
    ```
2.  Salva i due script separatamente (es. `1_geocoding.py` e `2_extraction.py`) o uniscili in un notebook `.ipynb` se preferisci (molto comodo per Colab).
3.  Carica il file CSV di input (`Codice ISTAT...`) come esempio.

Vuoi che ti aiuti a creare anche il file `.gitignore` per evitare di caricare file temporanei inutili?
