import numpy as np
import cv2

# Membuat watermark
def create_watermark(source_width, source_height, k_factor, seed):
    # Men-generate seed yang akan digunakan
    np.random.seed(seed)

    # Buat noise pattern
    watermark = np.random.randint(2, size=(source_width, source_height))
    watermark = watermark.astype(np.int16)

    # Lakukan mapping terhadap watermark yang dibuat
    # menjadi range -1...1
    watermark[watermark == 0] = -1

    # Kalikan watermark yang telah di-mapping dengan konstanta k
    watermark *= k_factor

    # Ubah watermark yang telah dibuat menjadi image
    watermark = np.array(watermark, dtype=np.int16)
    
    return watermark

# Meng-encode watermark ke dalam gambar
def encode_image(source, seed, k_factor):
    # Masukkan image yang akan diwatermark
    source_img = source.split("/")[-1]

    # Ubah gambar menjadi grayscale (komponen Y dari gambar asli)
    processed_img = cv2.imread(source_img, cv2.IMREAD_GRAYSCALE)
    processed_img = np.array(processed_img, dtype=np.int16)
    processed_img_width, processed_img_height = processed_img.shape[:2]

    # Buat watermark
    watermark = create_watermark(processed_img_width, processed_img_height, k_factor, seed)

    # Tambahkan watermark ke dalam gambar
    watermarked_img = cv2.add(processed_img, watermark)

    # Kembalikan hasil gambar yang telah ditambahkan watermark
    return watermarked_img

# Mendeteksi watermark pada gambar
def detect_watermark(original_source, watermarked_source):
    # Masukkan gambar yang akan dideteksi
    original_img = cv2.imread(original_source, cv2.IMREAD_GRAYSCALE)
    watermarked_img = cv2.imread(watermarked_source, cv2.IMREAD_GRAYSCALE)

    # Cari perbedaan antara gambar asli dengan yang telah
    # ditambahkan watermark
    difference = cv2.absdiff(original_img, watermarked_img)
    total_difference = np.sum(difference)

    # Pasang threshold perbedaan
    threshold = 100000

    # Cek perbedaan total dengan threshold
    if total_difference > threshold:
        return "The image is watermarked"
    else:
        return "The image is not watermarked"
    

# Masukkan gambar yang akan diwatermark
watermarked_img = encode_image("Farhan.jpg", 18221108, 10)
# Menuliskan gambar yang telah diwatermark
cv2.imwrite("Farhan_Watermarked_10.png", watermarked_img)
# Membandingkan gambar yang asli dengan yang telah diwatermark
print(detect_watermark("Farhan.jpg", "Farhan_Watermarked_10.png"))