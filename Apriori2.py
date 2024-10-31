from itertools import chain, combinations

# Load data from a CSV file into a list of transactions
def load_data(file_path):
    transactions = []
    with open(file_path, 'r') as file:
        next(file)  # Skip header
        for line in file:
            _, items = line.strip().split(',', 1)
            transaction = set(items.replace('"', '').split())  # Split items in each transaction
            transactions.append(transaction)
    return transactions

# Get unique items as 1-itemsets (initial candidate itemsets)
def get_unique_items(transactions):
    unique_items = set()
    for transaction in transactions:
        for item in transaction:
            unique_items.add(frozenset([item]))  # Store each item as a frozenset (1-itemset)
    return unique_items

# Calculate the support count of an itemset in all transactions
def calculate_support(transactions, itemset):
    return sum(1 for transaction in transactions if itemset.issubset(transaction))

# Generate candidate itemsets of size k from frequent itemsets of size k-1
def generate_candidates(previous_itemsets, k):
    candidates = set()
    previous_itemsets_list = list(previous_itemsets)
    for i in range(len(previous_itemsets_list)):
        for j in range(i + 1, len(previous_itemsets_list)):
            union_itemset = previous_itemsets_list[i] | previous_itemsets_list[j]
            if len(union_itemset) == k:  # Only keep itemsets of the correct size
                candidates.add(union_itemset)
    return candidates

# Apriori algorithm to find all frequent itemsets
def apriori(transactions, min_support):
    unique_items = get_unique_items(transactions)
    frequent_itemsets = {}
    k = 1  # Start with 1-itemsets

    while True:
        # Generate candidate itemsets
        if k == 1:
            candidate_itemsets = unique_items
        else:
            candidate_itemsets = generate_candidates(frequent_itemsets_k.keys(), k)
        
        # Calculate support for each candidate itemset and filter by min_support
        frequent_itemsets_k = {}
        for itemset in candidate_itemsets:
            support = calculate_support(transactions, itemset)
            if support >= min_support:
                frequent_itemsets_k[itemset] = support
        
        # Stop if no frequent itemsets were found
        if not frequent_itemsets_k:
            break
        
        # Add frequent itemsets of this size to the main list and proceed to the next size
        frequent_itemsets.update(frequent_itemsets_k)
        k += 1

    return frequent_itemsets

# Generate all possible non-empty subsets of an itemset
def powerset(itemset):
    return chain.from_iterable(combinations(itemset, r) for r in range(1, len(itemset)))

# Generate association rules from frequent itemsets
def generate_rules(transactions, itemset, itemset_support, min_confidence):
    rules = []
    for antecedent in map(set, powerset(itemset)):
        if antecedent and antecedent != itemset:  # Exclude empty and full itemsets
            consequent = itemset - antecedent
            antecedent_support = calculate_support(transactions, antecedent)
            if antecedent_support > 0:
                confidence = itemset_support / antecedent_support
                if confidence >= min_confidence:
                    rules.append((antecedent, consequent, confidence))
    return rules

# Parameters
min_support = 2
min_confidence = 0.75

# Load transactions
transactions = load_data("cono.csv")

# Find frequent itemsets
frequent_itemsets = apriori(transactions, min_support)

# Print frequent itemsets and their support counts
print("Frequent Itemsets :Counts:")
for itemset, support in frequent_itemsets.items():
    print(f"{set(itemset)}: {support}")

# Generate and print association rules
print("\nAssociation Rules:")
for itemset, support in frequent_itemsets.items():
    rules = generate_rules(transactions, itemset, support, min_confidence)
    for antecedent, consequent, confidence in rules:
        print(f"{set(antecedent)} => {set(consequent)} (Confidence: {confidence:.2f})")
          
