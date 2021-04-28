import csv
import os
import io

from .aws import retrieve_from_s3, upload_to_s3
from .fit_lib import DevelopmentRateModel, plt


def fit_uploaded_data_aws(file_name):
    data = retrieve_from_s3(f"uploads/{file_name}")
    temperature_list = []
    development_rate_list = []
    for row in csv.DictReader(io.StringIO(data), delimiter='\t'):
        temperature_list.append(float(row['temperature']))
        development_rate_list.append(float(row['dev_rate']))
    # print(temperature_list)
    # print(development_rate_list)
    # Instantiate model
    model = DevelopmentRateModel()
    # Guess parameters
    params = model.guess(development_rate_list,
                         temperature=temperature_list)
    # Fit function
    fit = model.fit(development_rate_list, params,
                    temperature=temperature_list)
    # Print fit report
    return fit


# https://viveksb007.github.io/2018/04/uploading-processing-downloading-files-in-flask
def fit_uploaded_data(full_path_file):
    # Deduce the format of the CSV file
    with open(full_path_file, newline='') as csvfile:
        # dialect = csv.Sniffer().sniff(csvfile.readline(), ['\t', ','])
        # csvfile.seek(0)  # sets the pointer to the biginning
        reader = csv.DictReader(csvfile, delimiter='\t')
        # reader.fieldnames = 'temperature', 'development_rate'
        # next(reader)
        temperature_list = []
        development_rate_list = []
        for row in reader:
            temperature_list.append(float(row['temperature']))
            development_rate_list.append(float(row['dev_rate']))
        # print(temperature_list)
        # print(development_rate_list)
        # Instantiate model
        model = DevelopmentRateModel()
        # Guess parameters
        params = model.guess(development_rate_list,
                             temperature=temperature_list)
        # Fit function
        fit = model.fit(development_rate_list, params,
                        temperature=temperature_list)
        # Print fit report
        return fit


def create_plot(fit, filename, target_folder="plots"):
    target_filename = os.path.splitext(
        os.path.basename(filename)
    )[0] + '.png'

    plt.ioff()
    plt.figure()
    fit.plot_fit()
    fit.plot_residuals()

    # https://stackoverflow.com/a/40925995
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    ret = upload_to_s3(target_filename, img_data,
                       folder="plots")
    print(ret)

    return ret
