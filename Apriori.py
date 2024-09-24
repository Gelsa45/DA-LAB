import csv
from itertools import combinations


file_path = "apriori.csv"
transactions = []
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    transactions = [list(row) for row in reader]

def apriori(transactions, min_support):
    c1 = {}
    for transaction in transactions:
        for item in transaction:
            if item in c1:
                c1[item] += 1
            else:
                c1[item] = 1

    l1 = {key: value for key, value in c1.items() if value / len(transactions) >= min_support}
    l = [l1]
    k = 2

    while len(l[k - 2]) > 0:
        ck = {}
        for transaction in transactions:
            combos = combinations(transaction, k)
            for combo in combos:
                if combo in ck:
                    ck[combo] += 1
                else:
                    ck[combo] = 1
        
        lk = {key: value for key, value in ck.items() if value / len(transactions) >= min_support}
        l.append(lk)
        
        
        print(f"Frequent itemsets {k}: {lk}")
        
        k += 1

    return [item for sublist in l for item in sublist.keys()]

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


min_support = 2 / len(transactions)
frequent_itemsets = apriori(transactions, min_support)

'''print("Frequent item sets:")
for itemset in frequent_itemsets:
    print(itemset)'''


min_confidence = 0.75
rules = association_rule(frequent_itemsets, transactions, min_confidence)
print("\nAssociation Rules:")
for r in rules:
    print(r[0], "=>", r[1])
 
