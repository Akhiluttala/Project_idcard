import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        Rollnumber = request.form['Rollnumber']
        Branch = request.form['Branch']

        photo = request.files['photo']
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)

        return render_template(
            'preview.html',
            name=name,
            year=year,
            Rollnumber=Rollnumber,
            Branch=Branch,
            photo=filename
        )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
