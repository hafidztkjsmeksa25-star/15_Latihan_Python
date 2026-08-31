import math

# === FUNGSI MATEMATIKA & LOGIKA (VERSI BARU) ===
def luas_persegi(sisi):
    return sisi * sisi

def keliling_persegi(sisi):
    return 4 * sisi

def is_prima(n):
    if n <= 1:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def status_genap_ganjil(x):
    if x % 2 == 0:
        return "Bilangan Genap"
    else:
        return "Bilangan Ganjil"

def luas_lingkaran(r):
    return 3.14 * r * r

def luas_segitiga(alas, tinggi):
    return 0.5 * alas * tinggi


# === MENU UTAMA (TUGAS 3) ===
while True:
    print("\n========================================")
    print("   MODUL MATEMATIKA & LOGIKA PYTHON    ")
    print("========================================")
    print("1. Hitung Luas Persegi")
    print("2. Hitung Keliling Persegi")
    print("3. Cek Bilangan Prima")
    print("4. Cek Bilangan Genap / Ganjil")
    print("5. Hitung Luas Lingkaran")
    print("6. Hitung Luas Segitiga")
    print("7. Keluar")
    
    pilihan = input("Pilih menu (1-7): ")
    
    if pilihan == "1":
        print("\n--- MODUL 1: LUAS PERSEGI ---")
        print(" Penjelasan: Sisi x Sisi")
        print(" Rumus: Luas = s * s")
        sisi = float(input("Masukkan sisi: "))
        luas = luas_persegi(sisi)
        print(" Penyelesaian:")
        print(f" -> {sisi} x {sisi} = {luas}")
        
    elif pilihan == "2":
        print("\n--- MODUL 2: KELILING PERSEGI ---")
        print(" Penjelasan: 4 kali panjang sisi")
        print(" Rumus: Keliling = 4 * s")
        sisi = float(input("Masukkan sisi: "))
        keliling = keliling_persegi(sisi)
        print(" Penyelesaian:")
        print(f" -> 4 x {sisi} = {keliling}")
        
    elif pilihan == "3":
        print("\n--- MODUL 3: BILANGAN PRIMA ---")
        print(" Penjelasan: Hanya bisa dibagi 1 & dirinya sendiri")
        angka = int(input("Masukkan angka: "))
        print(" Penyelesaian:")
        if is_prima(angka):
            print(f" -> {angka} adalah Bilangan Prima.")
        else:
            print(f" -> {angka} bukan Bilangan Prima.")
            
    elif pilihan == "4":
        print("\n--- MODUL 4: GENAP / GANJIL ---")
        print(" Penjelasan: Cek sisa bagi 2 (mod 2)")
        x = int(input("Masukkan angka: "))
        hasil = status_genap_ganjil(x)
        print(" Penyelesaian:")
        print(f" -> {x} adalah {hasil}.")
            
    elif pilihan == "5":
        print("\n--- MODUL 5: LUAS LINGKARAN ---")
        print(" Penjelasan: 3.14 x jari-jari x jari-jari")
        print(" Rumus: Luas = 3.14 * r * r")
        r = float(input("Masukkan jari-jari (r): "))
        luas_lingkaran_hasil = luas_lingkaran(r)
        print(" Penyelesaian:")
        print(f" -> 3.14 x {r} x {r} = {luas_lingkaran_hasil}")

    elif pilihan == "6":
        print("\n--- MODUL 6: LUAS SEGITIGA ---")
        print(" Penjelasan: Setengah alas kali tinggi")
        print(" Rumus: Luas = 0.5 * alas * tinggi")
        alas = float(input("Masukkan alas: "))
        tinggi = float(input("Masukkan tinggi: "))
        luas_segitiga_hasil = luas_segitiga(alas, tinggi)
        print(" Penyelesaian:")
        print(f" -> 0.5 x {alas} x {tinggi} = {luas_segitiga_hasil}")
        
    elif pilihan == "7":
        print("\nProgram selesai, terima kasih!")
        break
    else:
        print("\nPilihan salah, masukkan angka 1 sampai 7.")
