from flask import Flask, render_template, request, jsonify
import psycopg2
import random
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST"),
        database=os.environ.get("POSTGRES_DATABASE"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD")
    )
    return conn

@app.route('/')
def index():
    table_choice = random.choice(['botquotes', 'cgptquotes'])
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, quote FROM {table_choice} ORDER BY RANDOM() LIMIT 2")
    quotes = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', quotes=quotes, table_choice=table_choice)

@app.route('/rate', methods=['POST'])
def rate():
    data = request.json
    rating = data['rating']
    table_choice = data['table']
    quote_ids = data['quote_ids']
    

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_choice}_ratings (quote1_id, quote2_id, rating) VALUES (%s, %s, %s)", 
                   (quote_ids[0], quote_ids[1], rating))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/get_new_quotes', methods=['GET'])
def get_new_quotes():
    table_choice = random.choice(['botquotes', 'cgptquotes'])

    # Fetch two random quotes from the chosen table
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, quote FROM {table_choice} ORDER BY RANDOM() LIMIT 2")
    quotes = cursor.fetchall()
    conn.close()

    return jsonify({'quotes': quotes, 'table_choice': table_choice})

if __name__ == '__main__':
    app.run(debug=True)
