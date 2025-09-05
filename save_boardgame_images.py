import pandas as pd
import requests
import xml.etree.ElementTree as ET
import time
import os
import kagglehub

path = kagglehub.dataset_download("mshepherd/board-games")

print("Path to dataset files:", path)

csv_path = os.path.join(path, "bgg_GameItem.csv")
df = pd.read_csv(csv_path)

if 'bgg_id' not in df.columns:
    raise ValueError("Brakuje wymaganej kolumny 'bgg_id' w pliku CSV.")

bgg_ids = df['bgg_id'].dropna()

print(f"Znaleziono {len(bgg_ids)} ID gier do przetworzenia")

results = []

for bgg_id in bgg_ids:
    try:
        url = f"https://boardgamegeek.com/xmlapi2/thing?id={int(bgg_id)}"
        response = requests.get(url, timeout=10)
        root = ET.fromstring(response.content)
        image_elem = root.find('.//image')
        image_url = image_elem.text if image_elem is not None else ""
        results.append({'bgg_id': int(bgg_id), 'image': image_url})
        print(f"{bgg_id}: {image_url}")
        time.sleep(1)  # BGG API rate limit
    except Exception as e:
        print(f"Błąd dla {bgg_id}: {e}")
        results.append({'bgg_id': int(bgg_id), 'image': ""})

# Zapisz wyniki do pliku CSV
output_csv = "boardgame_images.csv"
pd.DataFrame(results).to_csv(output_csv, index=False)
print(f"Zapisano {len(results)} rekordów do pliku {output_csv}.")