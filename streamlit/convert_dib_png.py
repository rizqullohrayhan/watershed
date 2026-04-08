import os
from PIL import Image

folder_asal = '../../BBBC018_v1_images'
folder_tujuan = '../../BBBC018_v1_images_png'

if not os.path.exists(folder_tujuan):
    os.makedirs(folder_tujuan)

for file_name in os.listdir(folder_asal):
    if file_name.endswith('.DIB') or file_name.endswith('.dib'):
        img_path = os.path.join(folder_asal, file_name)
        with Image.open(img_path) as img:
            # Simpan sebagai PNG
            base_name = os.path.splitext(file_name)[0]
            img.save(os.path.join(folder_tujuan, f"{base_name}.png"))

print("Konversi selesai!")