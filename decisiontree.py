import csv
import math

# Load data from a CSV file into a list of dictionaries
def load_data(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


# Calculate the entropy of the data
def entropy(data):
    total = len(data)
    if total == 0:
        return 0
    
    count_yes = sum(1 for row in data if row['class_buys_computer'] == 'yes')
    count_no = total - count_yes

    # Calculate probabilities
    p_yes = count_yes / total
    p_no = count_no / total

    # Calculate entropy
    entropy_yes = -p_yes * math.log2(p_yes) if p_yes > 0 else 0
    entropy_no = -p_no * math.log2(p_no) if p_no > 0 else 0
   
    return entropy_yes + entropy_no


# Calculate information gain for a given attribute
def information_gain(data, attribute):
    total_entropy = entropy(data)
    values = set(row[attribute] for row in data)  # Unique values of the attribute
    weighted_entropy = 0

    # Calculate weighted entropy for each value of the attribute
    for value in values:
        subset = [row for row in data if row[attribute] == value]
        weighted_entropy += (len(subset) / len(data)) * entropy(subset)
    
    return total_entropy - weighted_entropy


# Split data based on attribute value
def split_data(data, attribute, value):
    return [row for row in data if row[attribute] == value]


# Build the decision tree recursively
def build_tree(data, attributes):
    # Base cases for the recursion
    if all(row['class_buys_computer'] == 'yes' for row in data):
        return 'yes'
    if all(row['class_buys_computer'] == 'no' for row in data):
        return 'no'
    if not attributes:
        return 'yes' if sum(1 for row in data if row['class_buys_computer'] == 'yes') >= len(data) / 2 else 'no'
    
    # Select the best attribute based on information gain
    best_attribute = max(attributes, key=lambda attr: information_gain(data, attr))
    tree = {best_attribute: {}}
    
    # Split data for each value of the best attribute and build subtrees
    for value in set(row[best_attribute] for row in data):
        subset = split_data(data, best_attribute, value)
        subtree = build_tree(subset, [attr for attr in attributes if attr != best_attribute])
        tree[best_attribute][value] = subtree
    
    return tree


# Display the decision tree
def display_tree(tree, indent=''):
    if isinstance(tree, dict):
        for key, value in tree.items():
            print(f"{indent}{key}")
            for sub_key, sub_value in value.items():
                print(f"{indent}  {sub_key} ->", end=' ')
                display_tree(sub_value, indent + '    ')
    else:
        print(f"{indent}Predict: {tree}")


# Predict the outcome for a given instance using the decision tree
def predict(tree, instance):
    if not isinstance(tree, dict):
        return tree
    attribute = next(iter(tree))
    value = instance[attribute]
    subtree = tree[attribute].get(value, 'no')
    return predict(subtree, instance)


# Get user input for prediction
def get_user_input():
    age = input("Enter age (youth/middle_aged/senior): ")
    income = input("Enter income (high/medium/low): ")
    student = input("Are you a student? (yes/no): ")
    credit_rating = input("Enter credit rating (fair/excellent): ")
    return {'age': age, 'income': income, 'student': student, 'credit_rating': credit_rating}


# Main function to execute the program
    # Load the data and build the tree
data = load_data('dectree.csv')
#print(data)
attributes = ['age', 'income', 'student', 'credit_rating']
tree = build_tree(data, attributes)

#print(tree)
    # Display the tree and get user input for prediction
display_tree(tree)
instance = get_user_input()
prediction = predict(tree, instance)
print(f"Prediction for class_buys_computer: {prediction}")
