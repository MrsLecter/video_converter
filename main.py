import os
from celery import Celery
from datetime import datetime
from celery_worker import toMP3
from flask import Flask, render_template, request, flash, request, redirect, url_for
from src.constants import UPLOAD_FOLDER
from src.utils import allowed_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

celery = Celery('tasks', backend='rpc://', broker='pyamqp://')
celery.conf.update(
    task_routes = {
        'proj.tasks.add': {'queue': 'hipri'},
    },
)

task_id = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print('filename: ' + filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            task = toMP3.apply_async(args=[filename],queue='hipri')
            time_now = datetime.now()
            task_id[time_now.utcnow()] = task
            return redirect("/check", code=302)
            
    return render_template('convert.html')


@app.route('/check')
def check():
    return render_template('check.html', data=task_id)


@app.route('/check/<task_id>')
def status_task( task_id):
    result = toMP3.AsyncResult(task_id, app=celery)
    return render_template('status.html', data={'state': result.state, 'key': task_id, 'done': result.ready(), 'sucessful': result.successful()})

if __name__=='__main__':
    app.run()