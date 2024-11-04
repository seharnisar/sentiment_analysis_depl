from flask import Flask, request, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import mysql.connector
from datetime import datetime
import time

app = Flask(__name__)


# Initialize and train the model directly in the app
def create_model():
    texts = [
        "I love this!", "This is terrible.", "I enjoy this movie", "I dislike this product",
        "What an amazing experience!", "Absolutely awful, I hate it.", "Fantastic product, will buy again!",
        "Worst purchase I have ever made.", "I'm so happy with this.", "It didn’t meet my expectations.",
        "Totally worth it!", "I wouldn't recommend this to anyone.", "This is the best thing ever!",
        "I regret buying this.", "I'm delighted with the results.", "It broke on the first use.",
        "Such a wonderful feeling!", "The quality is disappointing.", "Highly recommended!",
        "Not satisfied at all with this."
    ]
    labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1 = Positive, 0 = Negative

    model = make_pipeline(CountVectorizer(), LogisticRegression())
    model.fit(texts, labels)
    return model


# Connect to MySQL database and create Log table if it doesn't exist
db = mysql.connector.connect(
    host="db",  # Use "db" as the hostname because it's the service name in Docker
    user="your_username",
    password="your_password",
    database="Model_Logger"
)

cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Log (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Current_Date_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Input_Params TEXT,
    Output TEXT,
    Response_Time FLOAT
);
""")
cursor.close()


# Function to log prediction results into the MySQL database
def log_prediction(input_text, prediction, response_time):
    cursor = db.cursor()
    query = "INSERT INTO Log (Input_Params, Output, Response_Time) VALUES (%s, %s, %s)"
    values = (input_text, prediction, response_time)
    cursor.execute(query, values)
    db.commit()
    cursor.close()


# Initialize the model
model = create_model()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    input_text = request.form['input_text']

    start_time = time.time()
    prediction = model.predict([input_text])
    response_time = time.time() - start_time

    sentiment = "Positive" if prediction[0] == 1 else "Negative"

    # Log prediction to the database
    log_prediction(input_text, sentiment, response_time)

    return render_template('result.html', prediction=sentiment)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
