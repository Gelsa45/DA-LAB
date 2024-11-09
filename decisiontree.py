import csv
import math

# Step 1: Load data from CSV
filename = 'dectree.csv'
data = []
with open(filename, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)
print("Data Loaded:", data)

# Step 2: Calculate the entropy of the data
def calculate_entropy(data):
    total = len(data)
    if total == 0:
        return 0

    count_yes = sum(1 for row in data if row['class_buys_computer'] == 'yes')
    count_no = total - count_yes

    p_yes = count_yes / total
    p_no = count_no / total

    entropy_yes = -p_yes * math.log2(p_yes) if p_yes > 0 else 0
    entropy_no = -p_no * math.log2(p_no) if p_no > 0 else 0

    return entropy_yes + entropy_no

# Step 3: Calculate information gain for an attribute
def calculate_information_gain(data, attribute):
    total_entropy = calculate_entropy(data)
    values = set(row[attribute] for row in data)
    weighted_entropy = 0

    for value in values:
        subset = [row for row in data if row[attribute] == value]
        weighted_entropy += (len(subset) / len(data)) * calculate_entropy(subset)

    return total_entropy - weighted_entropy

# Step 4: Build the decision tree
def build_decision_tree(data, attributes):
    if all(row['class_buys_computer'] == 'yes' for row in data):
        return 'yes'
    if all(row['class_buys_computer'] == 'no' for row in data):
        return 'no'
    if not attributes:
        return 'yes' if sum(1 for row in data if row['class_buys_computer'] == 'yes') >= len(data) / 2 else 'no'

    best_attribute = max(attributes, key=lambda attr: calculate_information_gain(data, attr))
    tree = {best_attribute: {}}

    for value in set(row[best_attribute] for row in data):
        subset = [row for row in data if row[best_attribute] == value]
        subtree = build_decision_tree(subset, [attr for attr in attributes if attr != best_attribute])
        tree[best_attribute][value] = subtree

    return tree

attributes = ['age', 'income', 'student', 'credit_rating']
tree = build_decision_tree(data, attributes)

# Step 5: Display the decision tree
def display_tree(tree, indent=''):
    if isinstance(tree, dict):
        for key, value in tree.items():
            print(f"{indent}{key}")
            for sub_key, sub_value in value.items():
                print(f"{indent}  {sub_key} ->", end=' ')
                display_tree(sub_value, indent + '    ')
    else:
        print(f"{indent}Predict: {tree}")

print("Decision Tree:")
display_tree(tree)

# Step 6: Predict based on user input
def predict(tree, instance):
    if not isinstance(tree, dict):
        return tree
    attribute = next(iter(tree))
    value = instance[attribute]
    subtree = tree[attribute].get(value, 'no')
    return predict(subtree, instance)

# User input for prediction
age = input("Enter age (youth/middle_aged/senior): ")
income = input("Enter income (high/medium/low): ")
student = input("Are you a student? (yes/no): ")
credit_rating = input("Enter credit rating (fair/excellent): ")
instance = {'age': age, 'income': income, 'student': student, 'credit_rating': credit_rating}

prediction = predict(tree, instance)
print(f"Prediction for class_buys_computer: {prediction}")
