

symbols = ['SHSE.003000','SHSE.3001000','SZSE.60023','SHSE.688123']
print(symbols)

symbols=[ item for item in symbols if not item.split(".")[1].startswith("300") and not item.split(".")[1].startswith("688")]

print(symbols)
