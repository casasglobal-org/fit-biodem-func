import os

from flask import (flash, request, render_template,
                   redirect, send_from_directory)
from werkzeug.utils import secure_filename

from .aws import upload_to_s3
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
        upload_to_s3(csv_upload_file)

        fit = fit_uploaded_data_aws(file.filename)
        fit_report_string = fit.fit_report().splitlines()

        png_plot_file = create_plot(fit, filename)

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
