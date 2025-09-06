import pandas as pd
import requests
import xml.etree.ElementTree as ET
import time
import os

MAX_BATCH_NUMBER = 158

print(f"Uzupełnianie plików 0-{MAX_BATCH_NUMBER-1} o kolumnę description...")

for batch_num in range(MAX_BATCH_NUMBER):
    csv_filename = f"boardgame_images_batch_{batch_num}.csv"
    
    if not os.path.exists(csv_filename):
        print(f"Plik {csv_filename} nie istnieje - pomijam")
        continue
    
    # Wczytaj istniejący plik
    df = pd.read_csv(csv_filename)
    
    # Sprawdź czy już ma kolumnę description
    if 'description' in df.columns:
        print(f"Batch {batch_num}: już ma description - pomijam")
        continue
    
    print(f"Batch {batch_num}: uzupełniam o description ({len(df)} gier)")
    
    descriptions = []
    for _, row in df.iterrows():
        bgg_id = row['bgg_id']
        try:
            url = f"https://boardgamegeek.com/xmlapi2/thing?id={bgg_id}"
            response = requests.get(url, timeout=10)
            root = ET.fromstring(response.content)
            
            # Pobieranie opisu
            description_elem = root.find('.//description')
            description = description_elem.text if description_elem is not None else ""
            descriptions.append(description)
            
            time.sleep(1)  # limitowanie zapytań
        except Exception as e:
            print(f"  Błąd dla gry {bgg_id}: {e}")
            descriptions.append("")
    
    # Dodaj kolumnę description
    df['description'] = descriptions
    
    # Zapisz zaktualizowany plik
    df.to_csv(csv_filename, index=False)
    print(f"Batch {batch_num}: zaktualizowano i zapisano")

print(f"\nUkończono uzupełnianie plików 0-{MAX_BATCH_NUMBER-1}!")