import subprocess
import gmpy2
from Crypto.Util.number import *
from sympy import nextprime
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
  tot = (p-1) * (q-1)
  d = pow(e, -1, tot) 
  dec = pow(enc, d, n)
  return dec

def answer_B(n,e,enc):
  p = gmpy2.isqrt(n)
  tot = p * (p-1)
  d = pow(e, -1, tot)
  dec = pow(enc, d, n)
  return dec

def answer_C(n,e,enc):
  d = find_c_C(n, e, enc)
  dec = pow(enc, d, n)
  return dec

def answer_D(enc):
  getcontext().prec = 300
  dec = round(enc ** (Decimal(1)/Decimal(3)))
  return dec

def answer_E(n,e,enc):
  d = pow(e, -1, n-1)
  dec = pow(enc, d, n)
  return dec


host = "165.232.161.196"
port = 4020
send_data = "Z4xUM4c3y0"

process = subprocess.Popen(['ncat', host, str(port)],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)

response = process.stdout.readline()
print(f"Received response: {response}")

process.stdin.write(send_data)
process.stdin.flush()

response = ""
for _ in range(3):
  line = process.stdout.readline().strip()
  if not line:
    break
  response += line + '\n'

print(response)

count = 0
while count<30:
  line = process.stdout.readline()
  version = process.stdout.readline().split('=')[1].strip()
  n = int(process.stdout.readline().split('=')[1].strip())
  e = int(process.stdout.readline().split('=')[1].strip())
  enc = int(process.stdout.readline().split('=')[1].strip())

  print("versi: " + str(version))
  print("n: " + str(n))
  print("e: " + str(e))
  print("enc: " + str(enc))

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
  print("jawaban: " + str(input_dec))

  process.stdin.write(input_dec)
  process.stdin.flush()
  
  print(process.stdout.readline().split('=')[1].strip())
  count+=1

final_response = ""
for _ in range(5):
  line = process.stdout.readline().strip()
  if not line:
    break
  final_response += line + '\n'

print(final_response)

process.terminate()
try:
    process.wait(timeout=1)
except subprocess.TimeoutExpired:
    process.kill()
    process.wait()