import os
from flask import (
    flash, request, render_template, redirect,
    url_for, send_from_directory)
from werkzeug.utils import secure_filename

from .user_data import create_app
from .utils import fit_uploaded_data
from .fit_lib import plt

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'fit_biodem_func/uploads')
PLOT_FOLDER = os.path.join(os.getcwd(), 'fit_biodem_func/plots')
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = create_app()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PLOT_FOLDER'] = PLOT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    fit_report_string = None
    png_plot_file = None
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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            csv_upload_file = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)
            file.save(csv_upload_file)
            fit = fit_uploaded_data(csv_upload_file)
            fit_report_string = fit.fit_report()
            base_filename = os.path.splitext(filename)[0]
            png_plot_file = os.path.join(
                app.config['PLOT_FOLDER'], base_filename + '.png')
            plt.ioff()
            plt.figure()
            fit.plot_fit()
            fit.plot_residuals()
            plt.savefig(png_plot_file, dpi=300)

            # return redirect(url_for('uploaded_file',
            # filename=filename))
    return render_template('index.html',
                           png_plot=png_plot_file,
                           report_string=fit_report_string)


# Serving the uploaded file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# This route was defined as / and therefor overrode the earlier '/' endpoint
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
