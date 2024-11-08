import csv
from itertools import combinations

# Load data from CSV file
file_path = "apriori.csv"
transactions = []
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    transactions = [list(row) for row in reader]

# Set minimum support and confidence
min_support = 2
min_confidence = 0.75

# Step 1: Generate Frequent 1-itemsets
c1 = {}
for transaction in transactions:
    for item in transaction:
        if item in c1:
            c1[item] += 1
        else:
            c1[item] = 1

# Filter C1 to get L1 (Frequent 1-itemsets)
l1 = {key: value for key, value in c1.items() if value >= min_support}

# Print Frequent 1-itemsets
print("Frequent 1-itemsets:")
for item, support in l1.items():
    print(f"{item}: {support}")

# Initialize variables for frequent itemset generation
l = [l1]
k = 2
frequent_itemsets = []

# Add L1 items to frequent itemsets list
frequent_itemsets.extend(l1.keys())

# Step 2: Generate frequent itemsets for k >= 2
while len(l[k - 2]) > 0:
    ck = {}
    for transaction in transactions:
        # Generate combinations of items in the transaction of size k
        combos = combinations(transaction, k)
        for combo in combos:
            if combo in ck:
                ck[combo] += 1
            else:
                ck[combo] = 1

    # Filter candidate itemsets based on min_support
    lk = {key: value for key, value in ck.items() if value >= min_support}
    l.append(lk)
    
    # Print frequent k-itemsets
    print(f"Frequent {k}-itemsets:")
    for itemset, support in lk.items():
        print(f"{itemset}: {support}")

    # Add Lk items to frequent itemsets list
    frequent_itemsets.extend(lk.keys())
    
    k += 1
#print(frequent_itemsets)

# Step 3: Generate Association Rules
print("\nAssociation Rules:")
for itemset in frequent_itemsets:
    if isinstance(itemset, tuple):  # Only consider itemsets with more than one item
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                consequent = tuple(item for item in itemset if item not in antecedent)
                antecedent_support = sum(1 for transaction in transactions if set(antecedent).issubset(transaction))
                both_support = sum(1 for transaction in transactions if set(itemset).issubset(transaction))
                
                if antecedent_support > 0:
                    confidence = both_support / antecedent_support
                    if confidence >= min_confidence:
                        print(f"{' '.join(antecedent)} => {' '.join(consequent)} (Confidence: {confidence:.2f})")

