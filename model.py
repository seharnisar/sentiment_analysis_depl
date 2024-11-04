from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pickle

# Sample data
texts = [
    "I love this!", "This is terrible.", "I enjoy this movie", "I dislike this product",
    "What an amazing experience!", "Absolutely awful, I hate it.", "Fantastic product, will buy again!",
    "Worst purchase I have ever made.", "I'm so happy with this.", "It didn’t meet my expectations.",
    "Totally worth it!", "I wouldn't recommend this to anyone.", "This is the best thing ever!",
    "I regret buying this.", "I'm delighted with the results.", "It broke on the first use.",
    "Such a wonderful feeling!", "The quality is disappointing.", "Highly recommended!",
    "Not satisfied at all with this."
]

labels = [
    1, 0, 1, 0,
    1, 0, 1,
    0, 1, 0,
    1, 0, 1,
    0, 1, 0,
    1, 0, 1, 0
]  # 1 = Positive, 0 = Negative


# Create a simple pipeline with a vectorizer and logistic regression model
model = make_pipeline(CountVectorizer(), LogisticRegression())

# Train the model
model.fit(texts, labels)

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)


