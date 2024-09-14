from itertools import product
from random import randint
import json

# Prime number used to define the prime field
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

# Function to generate a random polynomial of degree `threshold - 1` with the given constant term (the secret)
def generate_random_polynomial(secret, threshold):
    coefficients = [secret] + [randint(1, p - 1) for _ in range(threshold-1)]
    return coefficients

# Function to evaluate the polynomial at a given x (used to create shares)
def evaluate_polynomial(coefficients, x):
    result = 0
    power_of_x = 1
    for coeff in coefficients:
        result += coeff * power_of_x
        power_of_x = (power_of_x * x) % p
    return result % p

# Function to generate shares from a secret
def generate_shares(secret, num_shares, threshold):
    coefficients = generate_random_polynomial(secret, threshold)
    shares = [(x, evaluate_polynomial(coefficients, x)) for x in range(1, num_shares + 1)]
    return shares

# Reconstruct the secret using Lagrange interpolation
def lagrange_interpolation(shares, prime):
    def interpolate_lagrange(x, shares, prime):
        result = 0
        for i in range(len(shares)):
            xi, yi = shares[i]
            numerator, denominator = 1, 1
            for j in range(len(shares)):
                if i != j:
                    xj, yj = shares[j]
                    numerator = (numerator * (x - xj)) % prime
                    denominator = (denominator * (xi - xj)) % prime
            result = (result + (numerator * pow(denominator, -1, prime) * yi)) % prime
        return result

    return interpolate_lagrange(0, shares, prime)

# Read JSON input from file
with open('gg.json', 'r') as file:
    data = json.load(file)

# Extract number of shares and threshold from the JSON
num_shares = data["keys"]["n"]
threshold = data["keys"]["k"]

# Convert secret values from their respective bases to integers
secrets = []
for key, value in data.items():
    if key != "keys":
        base = int(value["base"])
        secret_value = int(value["value"], base)
        secrets.append(secret_value)

# Use the first secret value for sharing (you can modify this logic as needed)
secret = secrets[0]

# Generate shares
shares = generate_shares(secret, num_shares, threshold)


# Reconstruct the secret from shares
reconstructed_secret = lagrange_interpolation(shares[:threshold], p)

# Print the reconstructed secret
print("Reconstructed Secret:", reconstructed_secret-1)
