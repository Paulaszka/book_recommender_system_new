import pandas as pd
import os
import glob

# Folder z batchami
input_dir = "img_and_desc"
output_file = "boardgame_images_merged.csv"

# Wyszukanie wszystkich plików batch w folderze
csv_files = sorted(glob.glob(os.path.join(input_dir, "boardgame_images_batch_*.csv")))

if not csv_files:
    print("❌ Nie znaleziono żadnych plików batch w folderze:", input_dir)
else:
    print(f"🔍 Znaleziono {len(csv_files)} plików – łączę je w jeden...")

    # Wczytanie i scalenie
    dfs = [pd.read_csv(f) for f in csv_files]
    merged_df = pd.concat(dfs, ignore_index=True)

    # Zapis do jednego pliku
    merged_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"✅ Zapisano scalony plik: {output_file} ({len(merged_df)} rekordów)")
