from flask import Flask
import os
import tempfile
from flask import send_file
from database.dbapi import DatabaseConnector

app = Flask(__name__)
db = DatabaseConnector()


@app.route('/download/<book_id>', methods=['POST', 'GET'])
def load_record(book_id):
    df = db.book_statistics(book_id)

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, f'book_{book_id}_stats.xlsx')
        df.to_excel(file_path, index=False)

        return send_file(file_path, as_attachment=True)


app.run("0.0.0.0", port=8080)