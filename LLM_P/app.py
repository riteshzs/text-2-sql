from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=os.getenv("SSL_CA"),
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )
    return connection

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/query", methods=["POST"])
def query_db():
    data = request.json
    natural_language_query = data.get("query")

    # Convert natural language to SQL using OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Convert the following natural language into an SQL query: {natural_language_query}"}
            ]
        )

        sql_query = response['choices'][0]['message']['content'].strip()

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()

        # Assuming a simple result for demonstration
        labels = [row[0] for row in result]
        values = [row[1] for row in result]

        return jsonify({"labels": labels, "values": values})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
