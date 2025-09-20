# Actual size mapping (Customer Size -> Production Size)
size_mapping = {
    "6-12": "1-2", "0-1": "1-2", "1-2": "1-2",
    "2-3": "3-4", "3-4": "3-4",
    "4-5": "5-6", "5-6": "5-6",
    "6-7": "7-8", "7-8": "7-8",
    "8-9": "9-10", "9-10": "9-10",
    "10-11": "11-12", "11-12": "11-12",
    "12-13": "13-14", "13-14": "13-14", "14-15": "13-14"
}

# File name containing daily customer sizes (one size per line)
file_name = "daily_orders.txt"

# Read customer sizes from file
customer_orders = []
with open(file_name, "r") as file:
    for line in file:
        size = line.strip()
        if size:  # skip empty lines
            customer_orders.append(size)

# Count orders per customer size
customer_count = {}
for size in customer_orders:
    customer_count[size] = customer_count.get(size, 0) + 1

# Count orders per production size
production_count = {}
for size, count in customer_count.items():
    production_size = size_mapping.get(size, size)  # default to same if not mapped
    production_count[production_size] = production_count.get(production_size, 0) + count

# Calculate total pieces
total_pieces = sum(production_count.values())

# Print results
print("Customer Size Orders:")
for size, count in sorted(customer_count.items()):
    print(f"{size}({count})")

print("\nProduction Size Orders:")
for size, count in sorted(production_count.items()):
    print(f"{size}({count})")

print("---")
print(f"TOTAL PIECES: {total_pieces}")