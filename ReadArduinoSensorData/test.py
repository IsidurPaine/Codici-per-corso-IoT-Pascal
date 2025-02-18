stringa = "Humidity: 22.00%,  Temperature: 18.00°C 64.40°F,  IdC: 16.43°C 61.57°F"
print(f"Stringa iniziale {stringa}")
umi = stringa.split(",")[2]
print(f"Primo risultato split della , {umi}")
umidi = umi.split(" ")[4]
print(f"Risultato split dello spazio {umidi}")
umidit = umidi.split("°")[0]
print(f"Risultato split del carattere {umidit}")




stringa = "-12,-546,3,10"
stringa.split(",")
print(stringa.split(","))