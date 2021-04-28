import csv
import os
import boto3
import io

from .fit_lib import DevelopmentRateModel, plt


def fit_uploaded_data_aws(file_name, bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    obj = bucket.Object(key='uploads/' + file_name)
    response = obj.get()
    data = response['Body'].read().decode('utf-8')
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


def create_plot(target_folder, fit, filename):
    base_filename = os.path.splitext(filename)[0]
    png_plot_file = os.path.join(target_folder, base_filename + '.png')
    plt.ioff()
    plt.figure()
    fit.plot_fit()
    fit.plot_residuals()
    plt.savefig(png_plot_file, dpi=300)
    return png_plot_file
