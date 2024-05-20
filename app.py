from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import ssl

app = Flask(__name__)

# MongoDB connection with SSL verification disabled
client = MongoClient('mongodb+srv://jayaa:123@cluster1.4tdtwbr.mongodb.net/',
                     tls=True, tlsAllowInvalidCertificates=True)
db = client['mydatabase']
collection = db['pymongo2']

@app.route('/')
def index():
    documents = collection.find()
    return render_template('index.html', documents=documents)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        document = {
            "_id": request.form['_id'],
            "name": request.form['name'],
            "city": request.form['city']
        }
        collection.insert_one(document)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        query = {"_id": request.form['_id']}
        new_values = {
            "$set": {
                "name": request.form['new_name'],
                "city": request.form['new_city']
            }
        }
        collection.update_one(query, new_values)
        return redirect(url_for('index'))
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        query = {"_id": request.form['_id']}
        collection.delete_one(query)
        return redirect(url_for('index'))
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)
