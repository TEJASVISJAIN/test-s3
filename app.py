from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET,S3_KEY,S3_SECRET 
from filters import datetimeformat 
import cv2 as cv
import numpy as np
from PIL import Image as im
from resources import get_bucket, get_buckets_list
from werkzeug.utils import secure_filename

s3 = boto3.client(
  's3',
  aws_access_key_id=S3_KEY,
  aws_secret_access_key=S3_SECRET
  )


app = Flask(__name__)
Bootstrap(app)
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.secret_key = "secret"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/files')
def files():
  my_bucket = get_bucket()
  summaries = my_bucket.objects.all()

  return render_template('files.html', my_bucket=my_bucket, files=summaries)

@app.route('/upload', methods=['POST'])
def upload():
  size= request.form.get('size')
  file = request.files.get['file']
  print(size)
  print(file)

  filename = secure_filename(file.filename)
  

  my_bucket = get_bucket()
  my_bucket.Object(file.filename).put(Body=file)

  flash('File uploaded successfully')
  return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )

if __name__ == "__main__":
    app.run()