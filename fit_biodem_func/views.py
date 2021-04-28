import os
import boto3
from flask import (flash, request, render_template,
                   redirect, send_from_directory)
from werkzeug.utils import secure_filename

from .user_data import create_app
from .utils import fit_uploaded_data_aws, create_plot

# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'fit_biodem_func/uploads')
# PLOT_FOLDER = os.path.join(os.getcwd(), 'fit_biodem_func/plots')
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = create_app()

# The old local way
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['PLOT_FOLDER'] = PLOT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


# The AWS way
FILE_URL = 'https://{bucket}.s3.eu-west-1.amazonaws.com/{filename}'
S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


def upload_to_s3(filepath, bucket=S3_BUCKET):
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
# PyBites tip 172 is suboptimal because
# https://stackoverflow.com/a/60239208/8677447
    s3 = session.resource('s3')
    ret = s3.Bucket(bucket).put_object(
        Key='uploads/'+filepath.filename,
        Body=filepath.read(),
        ACL='public-read')
    return FILE_URL.format(bucket=bucket, filename=ret.key)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    fit_report_string, png_plot_file = None, None

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if not allowed_file(file.filename):
            msg = (
                    f'File extension not allowed'
                    f' ({", ".join(ALLOWED_EXTENSIONS)})'
            )
            flash(msg)
            return redirect(request.url)

        filename = secure_filename(file.filename)
        print(filename)
        # csv_upload_file = os.path.join(
        #     app.config['UPLOAD_FOLDER'], filename)
        # file.save(csv_upload_file)

        csv_upload_file = file
        upload_to_s3(csv_upload_file, bucket=S3_BUCKET)

        fit = fit_uploaded_data_aws(file.filename, S3_BUCKET)
        fit_report_string = fit.fit_report().splitlines()

        png_plot_file = create_plot(app.config['PLOT_FOLDER'], fit, filename)

    png_plot_file = os.path.basename(png_plot_file) if png_plot_file else None

    return render_template('index.html',
                           filename=png_plot_file,
                           report_string=fit_report_string)


@app.route('/plots/<filename>')
def send_plot_file(filename):
    return send_from_directory(app.config['PLOT_FOLDER'], filename)


@app.route('/userdata', methods=['GET', 'POST'])
def get_userdata():
    if request.method == 'POST' and 'first_name' in request.form:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
    return render_template('index.html',
                           first_name=first_name,
                           last_name=last_name,
                           email=email)
