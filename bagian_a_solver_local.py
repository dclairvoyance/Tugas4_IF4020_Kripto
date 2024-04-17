from Crypto.Util.number import *
import random
from sympy import nextprime
import time
import gmpy2
from decimal import Decimal, getcontext

def factor_n_A(n):
  for i in range(gmpy2.isqrt(n)-40000, gmpy2.isqrt(n)+40000):
    if n % i == 0:
      return i, n // i

def find_c_C(n, e, c):
  for i in range(2**15, 2**16):
    dec = gmpy2.powmod(c, i, n)
    if(gmpy2.powmod(dec, e, n) == c):
      return i

def answer_A(n,e,enc):
  p,q = factor_n_A(n)
  # print("p: " + str(p))
  # print("q: " + str(q))
  tot = (p-1) * (q-1)
  d = pow(e, -1, tot) 
  dec = pow(enc, d, n)
  return dec

def answer_B(n,e,enc):
  p = gmpy2.isqrt(n)
  # print("p: " + str(p))
  tot = p * (p-1)
  # print("tot p: " + str(tot))
  d = pow(e, -1, tot)
  dec = pow(enc, d, n)
  return dec

def answer_C(n,e,enc):
  d = find_c_C(n, e, enc)
  # print("d: " + str(d))
  dec = pow(enc, d, n)
  return dec

def answer_D(enc):
  getcontext().prec = 300
  dec = round(enc ** (Decimal(1)/Decimal(3)))
  # print(dec)
  return dec

def answer_E(n,e,enc):
  d = pow(e, -1, n-1)
  # print("d: " + str(d))
  dec = pow(enc, d, n)
  return dec

flag = "RAHASIA"
tahap = 30
paket_soal = ["A", "B", "C", "D", "E"]
print(f"Selesaikan {tahap} tahap untuk mendapatkan flag!\n")
print("Kirimkan plainteks dalam bentuk format KRIPTOGRAFIITB{secret}!\n")
print("Tips: buatlah kode untuk otomasi :D\n")
counter = 0

try:
    for step in range(tahap):
        print(f"---------------- Tahap-{step}----------------\n")
        message_asli = "KRIPTOGRAFIITB{" + str(random.randint(1, 10000)) + "}"
        message_asli = message_asli.encode('utf-8')
        message_int = bytes_to_long(message_asli)
        version = random.choice(paket_soal)
        print(f"paket_soal = {version}\n")

        if version == "A":
            while True:
                ran = random.randint(1, 100)
                p = nextprime(getStrongPrime(1024) - ran)
                q = nextprime(nextprime(nextprime(nextprime(p) + ran) + ran) - ran)
                # ini generasi q berdekatan banget sama p, soalnya kalau 128 digit terus ditambahin bilangan antara 1-100 itu kecil jaraknya
                # karena nilainya mirip berarti angkanya ga akan beda jauh dari akar dari n
                # bisa di brute force cari p sama q nya (anggap aja range 40.000)
                n = p * q
                e = 65537
                check = GCD(e, (p-1)*(q-1)) == 1
                if check: break
            enc = pow(message_int, e, n)

        elif version == "B":
            p = getStrongPrime(1024)
            # ini p sama q hasilnya sama jadi bisa dicek pake kuadrat/akar
            n = p * p
            e = 65537
            enc = pow(message_int, e, n)

        elif version == "C":
            # melakukan enkripsi dengan kunci d, bukan e sehingga kita tahu range e dari kode
            # bisa pake brute force ngecek e sebagai kunci dekripsi
            while True:
                p = getStrongPrime(1024)
                q = getStrongPrime(1024)
                e = random.randrange(1, 65537)
                n = p * q
                tot = (p-1) * (q-1)
                e = random.randint(2**15, 2**16)
                check = GCD(e, tot) == 1
                if check: break
            d = pow(e, -1, tot)
            enc = pow(message_int, d, n)
            e = d

        elif version == "D":
            # nilai e terlalu kecil
            p = getStrongPrime(1024)
            q = getStrongPrime(1024)
            n = p * q
            e = 3
            enc = pow(message_int, e, n)

        elif version == "E":
            # asumsi p = n dan q = 1, totien jadinya p-1
            n = getStrongPrime(1024)
            e = 65537
            enc = pow(message_int, e, n)

        print(f"n = {n}\n")
        print(f"e = {e}\n")
        print(f"c = {enc}\n")

        try:
            if version == "A":
              dec = answer_A(n,e,enc)
            elif version == "B":
              dec = answer_B(n,e,enc)
            elif version == "C":
              dec = answer_C(n,e,enc)
            elif version == "D":
              dec = answer_D(enc)
            elif version == "E":
              dec = answer_E(n,e,enc)
            message = long_to_bytes(dec)
            input_dec = message.decode()
            print("Jawaban = " + input_dec)
            if input_dec == message_asli.decode():
                print("Uwaw keren!!!\n")
                counter += 1
            else:
                print(":((((((\n")
        except Exception as e:
            print(e)
            break

except Exception as e:
    print("Error\n")

finally:
    if counter == tahap:
        print(f"Uhuyyyy {flag}\n")
    else:
        print("Tetap semangat dan jangan putus asa!\n")