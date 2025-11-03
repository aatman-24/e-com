size_mapping = {
    "6-12": "1-2", "0-1": "1-2", "1-2": "1-2",
    "2-3": "3-4", "3-4": "3-4",
    "4-5": "5-6", "5-6": "5-6",
    "6-7": "7-8", "7-8": "7-8",
    "8-9": "9-10", "9-10": "9-10",
    "10-11": "11-12", "11-12": "11-12",
    "12-13": "13-14", "13-14": "13-14", "14-15": "13-14"
}

# Define age-group order for sorting
customer_size_order = [
    "0-1", "6-12", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8",
    "8-9", "9-10", "10-11", "11-12", "12-13", "13-14", "14-15"
]
production_size_order = [
    "1-2", "3-4", "5-6", "7-8", "9-10", "11-12", "13-14"
]

file_name = "daily_orders.txt"

customer_orders = []
with open(file_name, "r") as file:
    for line in file:
        size = line.strip()
        if size:
            customer_orders.append(size)

customer_count = {}
for size in customer_orders:
    customer_count[size] = customer_count.get(size, 0) + 1

production_count = {}
for size, count in customer_count.items():
    production_size = size_mapping.get(size, size)
    production_count[production_size] = production_count.get(production_size, 0) + count

total_pieces = sum(production_count.values())

print("Customer Size Orders:")
for size in customer_size_order:
    if size in customer_count:
        print(f"{size}({customer_count[size]})")

print("\nProduction Size Orders:")
for size in production_size_order:
    if size in production_count:
        print(f"{size}({production_count[size]})")

print("---")
print(f"TOTAL PIECES: {total_pieces}")