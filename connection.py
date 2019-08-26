import csv


def get_all_data_from_file(file_path):
    file_content = []
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_in_file = dict(row)
            file_content.append(row_in_file)
    return file_content   # list of dictonarys


def add_new_question(file_path, list_of_data):
    with open(file_path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list_of_data)

