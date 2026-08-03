
x =  int(input("Masukkan Nilai X: "))
if x % 2 == 0:
    print(f"Bilangan {x} termasuk Bilangan genap")
else:
    print(f"Bilangan {x} termasuk Bilangan ganjil")

    ulang = input("cek lagi? (lagi/tidak): ") .lower( )
    if ulang != 'lagi' :
        print("program selesai.")