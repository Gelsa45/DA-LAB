import csv
from itertools import combinations

# Load data from CSV file
file_path = "apriori.csv"
transactions = []
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    transactions = [list(row) for row in reader]

# Apriori Algorithm
def apriori(transactions, min_support):
    # Count occurrences of each item in transactions to create C1
    c1 = {}
    for transaction in transactions:
        for item in transaction:
            if item in c1:
                c1[item] += 1
            else:
                c1[item] = 1

    # Generate L1, filtering items based on min_support
    l1 = {key: value for key, value in c1.items() if value / len(transactions) >= min_support}
    
    # Print Frequent 1-itemsets
    print("Frequent 1-itemsets:")
    for item, support in l1.items():
        print(f"{item}: {support}")
    
    l = [l1]
    k = 2

    # Generate frequent itemsets for k >= 2
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
        lk = {key: value for key, value in ck.items() if value / len(transactions) >= min_support}
        l.append(lk)
        
        # Print frequent k-itemsets
        print(f"Frequent {k}-itemsets: {lk}")
        
        k += 1

    # Flatten the list of frequent itemsets
    return [item for sublist in l for item in sublist.keys()]

# Association Rule Generation
def association_rule(frequent_itemsets, transactions, min_confidence):
    rules = []
    for itemset in frequent_itemsets:
        for i in range(1, len(itemset)):
            antecedents = [x for x in combinations(itemset, i)]
            for antecedent in antecedents:
                consequent = tuple([item for item in itemset if item not in antecedent])
                antecedent_support = sum([1 for transaction in transactions if set(antecedent).issubset(set(transaction))])
                both_support = sum([1 for transaction in transactions if set(antecedent + consequent).issubset(set(transaction))])
                
                try:
                    confidence = both_support / antecedent_support
                    if confidence >= min_confidence:
                        rules.append((antecedent, consequent))
                except ZeroDivisionError:
                    pass 
    return rules

# Set minimum support and confidence
min_support = 2 / len(transactions)
frequent_itemsets = apriori(transactions, min_support)

# Set minimum confidence
min_confidence = 0.75
rules = association_rule(frequent_itemsets, transactions, min_confidence)

# Print association rules
print("\nAssociation Rules:")
for a, c in rules:
    print(f"{' '.join(a)} => {' '.join(c)}")
