import sqlite3
from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook

app = Flask(__name__)
discord_webhook_url = 'https://discord.com/api/webhooks/1290990002716807228/-F3mIDlwYzaCO5MCAsDYAXkv3j_gPOqgNleOhJfE_XZJzklfIBauPvDsYMhAfu7uzSxT'

conn = sqlite3.connect('messages.db',check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
     CREATE TABLE IF NOT EXISTS messagges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        timestamp DATETIME
        )
''')
conn.commit()

def save_to_database(text):
    try:
        timestamp = datetime.now()
        cursor.execute('INSERT INTO messages (content,timestamp) Values (?,?)', (text,timestamp))
        conn.commit()
        print("Message saved successfully!")
    except Exception as e:
        print(f'Error saving the message: {e}')

@app.route('/input_text',methods =['POST'])

def input_text():
    try:
        text = request.form['text']
        print(f"Received text: {text}")

        send_to_discord(text)

        save_to_database(text)

        return render_template('index.html',success=True)
    except Exception as e:
        print(f"Error in input_text: {e}")
        return render_template('index.html', success=False, error_message=str(e))

def send_to_discord(text):
    webhook = DiscordWebhook(url=discord_webhook_url, content=text)
    webhook.execute()


@app.route('/get_messages', methods=['GET'])
def get_messages():
    try:
        cutoff_time = datetime.now() - timedelta(minutes=30)

        cursor.execute('SELECT content, timestamp FROM messages WHERE timestamp >= ?', (cutoff_time,))
        messages = cursor.fetchall()
        return jsonify({"status": "success", "messages": messages})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
















