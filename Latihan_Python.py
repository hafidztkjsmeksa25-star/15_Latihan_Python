def bilangan_genap_ganjil():
    while True:
        try:
            x = int(input("Masukkan Nilai X: "))
        except ValueError:
            print("Input tidak valid, masukkan angka!")
            continue

        if x % 2 == 0:
            print(f"Bilangan {x} termasuk Bilangan genap")
        else:
            print(f"Bilangan {x} termasuk Bilangan ganjil")


if __name__ == "__main__":
    bilangan_genap_ganjil()
