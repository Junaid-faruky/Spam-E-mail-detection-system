# Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import gradio as gr
import re

# Step 1: Load the dataset
file_path = 'spam.csv'  # Replace with the correct path to your dataset
try:
    df = pd.read_csv(file_path, encoding='latin1')
except FileNotFoundError:
    print("Error: The file 'spam.csv' was not found. Ensure the file is in the correct directory.")
    raise

# Step 2: Clean and process the dataset
df = df.rename(columns={'v1': 'label', 'v2': 'text'})
df = df[['label', 'text']]
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# Function to clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
    text = ' '.join([word for word in text.split() if word not in ENGLISH_STOP_WORDS])
    return text

df['text'] = df['text'].apply(clean_text)

# Step 3: Split the data into training and testing sets
X = df['text']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Step 4: TF-IDF Vectorization
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Step 5: Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Step 6: Evaluate the model
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Print evaluation metrics
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")

# Step 7: Plot the confusion matrix
def plot_confusion_matrix(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()

plot_confusion_matrix(y_test, y_pred)

# Step 8: Create the Gradio Interface
def classify_email(email):
    email_cleaned = clean_text(email)
    email_tfidf = vectorizer.transform([email_cleaned])
    prediction = model.predict(email_tfidf)
    classification = "Spam" if prediction[0] == 1 else "Ham"
    result = f"Classification: {classification}\n"
    result += f"Accuracy: {accuracy:.2f}\n"
    result += f"Precision: {precision:.2f}\n"
    result += f"Recall: {recall:.2f}\n"
    result += f"F1 Score: {f1:.2f}"
    return result

# Launch Gradio Interface
interface = gr.Interface(
    fn=classify_email,
    inputs="text",
    outputs="text",
    title="Email Spam Classifier",
    description="Enter an email text to classify it as Spam or Ham, and view the evaluation metrics."
)

interface.launch(share=True)
