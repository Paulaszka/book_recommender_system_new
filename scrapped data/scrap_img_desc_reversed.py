import pandas as pd
import requests
import xml.etree.ElementTree as ET
import time
import os
import kagglehub

BATCH_SIZE = 100

path = kagglehub.dataset_download("mshepherd/board-games")
csv_path = os.path.join(path, "bgg_GameItem.csv")
df = pd.read_csv(csv_path)

all_bgg_ids = df['bgg_id'].dropna().astype(int)
total_games = len(all_bgg_ids)
total_batches = (total_games + BATCH_SIZE - 1) // BATCH_SIZE

output_dir = "img_and_desc"
os.makedirs(output_dir, exist_ok=True)

start_batch = total_batches - 1

try:
    while start_batch >= 0:
        start_idx = start_batch * BATCH_SIZE
        end_idx = min((start_batch + 1) * BATCH_SIZE, total_games)
        current_batch_ids = all_bgg_ids.iloc[start_idx:end_idx]

        print(f"\nBatch {start_batch} ({len(current_batch_ids)} gier: {start_idx}–{end_idx-1})")

        output_csv = os.path.join(output_dir, f"boardgame_images_batch_{start_batch}.csv")
        if os.path.exists(output_csv):
            print(f"Plik {output_csv} już istnieje – pomijam.")
            start_batch -= 1
            continue

        results = []
        for bgg_id in current_batch_ids:
            try:
                url = f"https://boardgamegeek.com/xmlapi2/thing?id={bgg_id}"
                response = requests.get(url, timeout=10)
                root = ET.fromstring(response.content)
                
                image_elem = root.find('.//image')
                image_url = image_elem.text if image_elem is not None else ""
                
                description_elem = root.find('.//description')
                description = description_elem.text if description_elem is not None else ""
                
                results.append({
                    'bgg_id': bgg_id, 
                    'image': image_url,
                    'description': description
                })
                time.sleep(1)
            except Exception:
                results.append({
                    'bgg_id': bgg_id, 
                    'image': "",
                    'description': ""
                })

        pd.DataFrame(results).to_csv(output_csv, index=False)
        print(f"Zapisano batch {start_batch} ({len(results)} rekordów) -> {output_csv}")

        start_batch -= 1
        
    print("\nWszystkie batche przetworzone!")

except KeyboardInterrupt:
    print(f"\nPrzerwano ręcznie w batchu {start_batch}.")