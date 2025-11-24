**🌍 GeoFrazioni ER: Estrazione Intelligente Frazioni da OpenStreetMap**

Descrizione (da inserire nel README)
Questo progetto fornisce un Jupyter Notebook (.ipynb) completo per scaricare, georeferenziare e catalogare tutte le frazioni dei comuni dell'Emilia-Romagna (o di altre regioni configurabili), risolvendo le criticità tipiche dello scraping su OpenStreetMap.

A differenza di semplici script di query, questo tool utilizza un approccio a due stadi per garantire precisione geografica e resilienza contro i blocchi server.

🚀 Come Funziona (Logica dello Script)
Il notebook esegue due operazioni sequenziali:

Stage 1: Geocoding Blindato (Nominatim)

Interroga l'API di Nominatim per ogni comune del file ISTAT.

Recupera il Bounding Box (BBox) esatto (coordinate min/max).

Obiettivo: Risolve le omonimie internazionali (es. evita che "Lugo" venga cercato in Spagna o "San Clemente" in Argentina) confinando la ricerca al rettangolo geografico corretto.

Stage 2: Estrazione Resiliente (Overpass API)

Utilizza i BBox calcolati per scaricare puntualmente i nodi place=village (frazioni) e place=suburb (località costiere/urbane).

Sistema Multi-Server Failover: Lo script integra una lista di server Overpass (Germania, Francia, Russia, Kumi). Se il server principale va in timeout (504) o cade la connessione, il tool ruota automaticamente sul server successivo senza interrompere il lavoro.

Filtro Intelligente: Esclude automaticamente i suburb per i grandi capoluoghi (es. Bologna, Modena) per evitare di mappare i quartieri cittadini come frazioni, mantenendoli invece per le località turistiche (es. Pinarella di Cervia).

🛠️ Configurazione e Requisiti
Il codice è ottimizzato per Google Colab ma funziona su qualsiasi ambiente Jupyter locale.

Input: File CSV con colonne Denominazione Comune e Provincia.

Output: File CSV (Frazioni_ER_Finali_Complete.csv) contenente:

Comune e Provincia

Nome Frazione

Tipologia (village o suburb)

Coordinate (Lat/Lon)

📦 Dipendenze
Plaintext

pandas
requests
