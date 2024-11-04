import csv
# Step 2: Calculate Prior Probabilities P(class)
def calculate_prior_probabilities(data):
    """Calculates the prior probabilities for each class label."""
    total_samples = len(data)
    class_counts = {}

    for features, label in data:
        if label in class_counts:
          class_counts[label] += 1
        else:
          class_counts[label] = 1


    # Calculate prior probabilities
    priors = {label: count / total_samples for label, count in class_counts.items()}
    return priors

# Step 3: Calculate Likelihood P(feature|class)
'''def calculate_likelihoods(data):
    """Calculates the likelihood of each feature given the class label."""
    # Initialize dictionaries to count features and classes
    feature_counts = {}  # Counts of features for each class
    class_counts = {}    # Total count of samples for each class

    # Iterate through each sample in the dataset
    for features, label in data:
    # Check if the class label has been encountered before
        if label in class_counts:
            class_counts[label] += 1  # Increment count for this class
        else:
            class_counts[label] = 1   # Initialize count for this class label
            feature_counts[label] = [{} for feature in features]  # Prepare feature count dictionary for each feature position

    # Loop through each feature and update its count for the current class
        for i, feature in enumerate(features):
            if feature in feature_counts[label][i]:
                feature_counts[label][i][feature] += 1  # Increment count if feature already exists
            else:
                feature_counts[label][i][feature] = 1  # Initialize count if feature not seen yet


    # Calculate likelihoods using Laplace smoothing
    likelihoods = {}
    for label in feature_counts:
        likelihoods[label] = []  # Prepare to store likelihoods for this class
        total_count = class_counts[label]  # Total samples for this class

        # Iterate over each feature's counts for the current class
        for feature_count in feature_counts[label]:
            # Calculate the likelihood for each feature with Laplace smoothing
            likelihood = {}
            for feature, count in feature_count.items():
                # Apply Laplace smoothing: add 1 to count and total feature count
                likelihood[feature] = (count + 1) / (total_count + len(feature_count))
            likelihoods[label].append(likelihood)  # Store the calculated likelihoods

    return likelihoods  # Return the likelihoods for each class'''
def calculate_likelihoods(data):
    feature_counts = {}
    class_counts = {}

    for features, label in data:
        if label not in class_counts:
            class_counts[label] = 0
            feature_counts[label] = [{} for _ in range(len(features))]
        class_counts[label] += 1
        for i in range(len(features)):
            if features[i] not in feature_counts[label][i]:
                feature_counts[label][i][features[i]] = 0
            feature_counts[label][i][features[i]] += 1

    likelihoods = {}
    for label in feature_counts:
        likelihoods[label] = []
        for i in range(len(feature_counts[label])):
            likelihoods[label].append({key: feature_counts[label][i][key] / class_counts[label]
                                       for key in feature_counts[label][i]})
    print("likelihoods")
    print(likelihoods)
    return likelihoods



# Step 5: Running the classifier on new data
def naive_bayes_classifier(data, new_data):
    """Main function to run the Naive Bayes classifier."""
    priors = calculate_prior_probabilities(data)  # Calculate prior probabilities
    likelihoods = calculate_likelihoods(data)      # Calculate likelihoods
    #return classify(priors, likelihoods, new_data)          # Classify new data
    posteriors = {}

    for label in priors:
        posteriors[label] = priors[label]
        for i in range(len(new_data)):
            # Multiply prior by likelihood of each feature given the class
            posteriors[label] *= likelihoods[label][i].get(new_data[i], 0)  # Default to 0 if feature not found

    # Print the posterior probabilities for each class
    for label, posterior in posteriors.items():
        print(f"Posterior probability for {label}: {posterior:.4f}")

    return max(posteriors, key=posteriors.get)  # Return class with the highest probability


# Main execution

filename = 'naive.csv'  # Name of your CSV file
data = []
with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            features = row[1:-1]  # Extract features (all but the last column)
            label = row[-1]       # Extract the label (last column)
            data.append((features, label))
 # Read training data

    # Classify the new data: X = (age=youth, income=medium, student=yes, credit_rating=fair)
new_sample = ['youth', 'medium', 'yes', 'fair']
predicted_class = naive_bayes_classifier(data, new_sample)
print(f'Predicted class for {new_sample}: {predicted_class}')
