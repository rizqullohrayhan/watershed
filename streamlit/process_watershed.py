import cv2
import numpy as np
from matplotlib import pyplot as plt

def process_watershed(image_path, dist_transform):
    # 1. Load citra dalam grayscale
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Pre-processing: Blur untuk mengurangi noise mikroskopis
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Thresholding: Menggunakan Otsu untuk memisahkan sel dari background hitam
    ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 4. Morphological Operations: Menghilangkan noise kecil (Opening)
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Menutup lubang di dalam sel (Closing)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    # 5. Background Area (Dilation)
    sure_bg = cv2.dilate(closing, kernel, iterations=3)

    # 6. Foreground Area (Distance Transform)
    # Ini sangat penting untuk BBBC agar sel yang menempel bisa terpisah
    # dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 5)
    # Ambil puncak dari tiap sel sebagai marker foreground
    ret, sure_fg = cv2.threshold(dist_transform, 0.4 * dist_transform.max(), 255, 0)

    # 7. Marker Labelling
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # 8. Watershed
    markers = cv2.watershed(img, markers)
    
    # Visualisasi: Warnai batas sel dengan warna hijau
    img[markers == -1] = [0, 255, 0]
    
    return img, markers, ret - 1 # ret - 1 adalah jumlah sel yang terhitung

# Contoh eksekusi
# result, map_markers, total_sel = proses_sel_bbbc('path_ke_file_bbbc.png')
# print(f"Jumlah sel terdeteksi: {total_sel}")