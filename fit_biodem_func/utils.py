import csv

from .fit_lib import DevelopmentRateModel


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
