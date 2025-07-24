import random
import json

Anzahl = 100
numbers = []

for _ in range(Anzahl):
    numbers.append(random.randint(100000, 999999))

# Save to /src/tokens.json
with open('./src/tokens.json', 'w') as f:
    json.dump(numbers, f, indent=2)
