import csv
import random

import sorts as sort

VAERSVAX_FILES = ['/Users/jane/CSC365_Data/2020VAERSVAX.csv', '/Users/jane/CSC365_Data/2021VAERSVAX.csv.crdownload']
VAERSDATA_FILES = ['/Users/jane/CSC365_Data/2020VAERSData.csv', '/Users/jane/CSC365_Data/2021VAERSData.csv.crdownload']
VAERSSYMPTOMS_FILES = ['/Users/jane/CSC365_Data/2020VAERSSYMPTOMS.csv',
                       '/Users/jane/CSC365_Data/2021VAERSSYMPTOMS.csv.crdownload']

COVID19_DATA = {}
TASK2_DATA = []
SYMPTOMS = {}
TASK1_HEADER = []
TASK2_HEADER = ["VAERS_ID", "AGE_YRS", "SEX", "VAX_NAME", "RPT_DATE", "SYMPTOM", "DIED", "DATEDIED", "SYMPTOM_TEXT"]
TASK2_INFO = ["VAERS_ID", "AGE_YRS", "SEX", "VAX_NAME", "RPT_DATE", "DIED", "DATEDIED", "SYMPTOM_TEXT"]
TASK3_DATA = [[], [], [], [], [], [], [], [], [], [], [], []]

MAX_SYMPTOMS = 0


def task1():
    get_ids(VAERSVAX_FILES)
    get_task1_data(VAERSDATA_FILES, True)
    get_task1_data(VAERSSYMPTOMS_FILES, False)
    create_task1_csv()


# Getting ids from VAERSVAX and storing their data into a dict
def get_ids(files):
    for file in files:
        with open(file, 'r', encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0 and files.index(file) == 0:
                    TASK1_HEADER.extend(row)
                else:
                    vaccine = row[1]
                    if vaccine == "COVID19":
                        vaers_id = row[0]
                        COVID19_DATA[vaers_id] = row
                line_count += 1


# Get rest of data from VAERSData and VAERSSYMPTOMS
def get_task1_data(files, data):
    for file in files:
        with open(file, 'r', encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            prev_id = ""  # check if repeating id
            for row in csv_reader:
                if line_count == 0 and files.index(file) == 0:
                    if data:
                        TASK1_HEADER[1:1] = row[1:len(row)]  # insert header before VAERSVAX
                else:
                    multiple_symps = False
                    vaers_id = row[0]
                    if prev_id == vaers_id:
                        multiple_symps = True
                    prev_id = vaers_id

                    if vaers_id in COVID19_DATA.keys():  # if VAERS_ID is in the hashmap
                        if data:  # from VAERSData
                            COVID19_DATA[vaers_id][1:1] = row[1:len(row)]
                        else:  # from VAERSSymptoms
                            read_symptoms_row(row, multiple_symps, vaers_id)
                line_count += 1
    create_symptom_rows()


def read_symptoms_row(row, multiple_symps, vaers_id):
    symptoms = {"symptoms": [], "version": []}
    i = 1
    while i < len(row) - 1:
        symptom = row[i]
        version = row[i + 1]
        if symptom is not '':
            symptoms["symptoms"].append(symptom)
            symptoms["version"].append(version)
        else:
            break
        i += 2

    if multiple_symps:
        SYMPTOMS[vaers_id]["symptoms"].extend(symptoms["symptoms"])
        SYMPTOMS[vaers_id]["version"].extend(symptoms["version"])
    else:
        SYMPTOMS[vaers_id] = symptoms

    global MAX_SYMPTOMS
    if len(SYMPTOMS[vaers_id]["symptoms"]) > MAX_SYMPTOMS:
        MAX_SYMPTOMS = len(SYMPTOMS[vaers_id]["symptoms"])


def create_symptom_rows():
    for i in range(1, int(MAX_SYMPTOMS) + 1):  # Adding extra columns to match max symptoms
        TASK1_HEADER.extend(["SYMPTOM" + str(i)])
        TASK1_HEADER.extend(["SYMPTOMVERSION" + str(i)])

    for key in COVID19_DATA.keys():
        row = COVID19_DATA[key]
        symp_arr_length = 0
        if key in SYMPTOMS.keys():
            symptoms_dict = SYMPTOMS[key]
            symp_arr_length = len(symptoms_dict["symptoms"])
            for i in range(0, symp_arr_length - 1):
                row.append(symptoms_dict["symptoms"][i])
                row.append(symptoms_dict["version"][i])

        for i in range(symp_arr_length * 2, MAX_SYMPTOMS - 1):  # Adding extra commas for empty slots
            row.extend([""])


def create_task1_csv():
    with open('/Users/jane/CSC365_Data/VAERS_COVID_DataAugust2021.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(TASK1_HEADER)
        for key in COVID19_DATA.keys():
            row = COVID19_DATA[key]
            writer.writerow(row)
    print(len(COVID19_DATA.keys()))


def task2():
    create_task2_data()
    create_task2_data_2()
    sort_task2_data()
    sort_task2_data_random()


def create_task2_data():
    column_idx = []

    for data in TASK2_INFO:
        index = TASK1_HEADER.index(data)
        column_idx.append(index)

    with open('/Users/jane/CSC365_Data/SYMPTOMDATA_2.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(TASK2_HEADER)
        for key in COVID19_DATA.keys():
            row = COVID19_DATA[key]
            vaers_id = row[0]
            task2_data = []
            for idx in column_idx:
                task2_data.append(row[idx])
            if vaers_id in SYMPTOMS.keys():
                symptoms = SYMPTOMS[vaers_id]["symptoms"]
                for symptom in symptoms:
                    task2_data_symps = task2_data.copy()
                    task2_data_symps.insert(5, symptom)
                    writer.writerow(task2_data_symps)
                    TASK2_DATA.append(task2_data_symps)
            else:
                writer.writerow(task2_data)
                TASK2_DATA.append(task2_data)


def create_task2_data_2():  # For task 3 - all symptoms in one row
    column_idx = []

    for data in TASK2_INFO:
        index = TASK1_HEADER.index(data)
        column_idx.append(index)

    with open('/Users/jane/CSC365_Data/SYMPTOMDATA_2.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(TASK2_HEADER)
        for key in COVID19_DATA.keys():
            row = COVID19_DATA[key]
            vaers_id = row[0]
            task2_data = []
            for idx in column_idx[:5]:
                task2_data.append(row[idx])
            if vaers_id in SYMPTOMS.keys():
                symptoms = SYMPTOMS[vaers_id]["symptoms"]
                for symptom in symptoms:
                    task2_data.append(symptom)
            for idx in column_idx[5:]:
                task2_data.append(row[idx])
            writer.writerow(task2_data)


def sort_task2_data():
    all_data = []
    with open('/Users/jane/CSC365_Data/SYMPTOMDATA.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            all_data.append(row)

    print(len(all_data))

    print("Insertion sort: ")
    print("10: ", sort.insertion_sort(all_data.copy()[1:10]))
    print("100: ", sort.insertion_sort(all_data.copy()[1:100]))
    print("1000: ", sort.insertion_sort(all_data.copy()[1:1000]))
    print("10000: ", sort.insertion_sort(all_data.copy()[1:10000]))
    print("100000: ", sort.insertion_sort(all_data.copy()[1:100000]))
    print("1000000: ", sort.insertion_sort(all_data.copy()[1:1000000]))
    print("All data: ", sort.insertion_sort(all_data.copy()[1:]))

    print("Quick sort: ")
    print("10: ", sort.quick_sort(all_data.copy()[1:10]))
    print("100: ", sort.quick_sort(all_data.copy()[1:100]))
    print("1000: ", sort.quick_sort(all_data.copy()[1:1000]))
    print("10000: ", sort.quick_sort(all_data.copy()[1:10000]))
    print("100000: ", sort.quick_sort(all_data.copy()[1:100000]))
    print("1000000: ", sort.quick_sort(all_data.copy()[1:1000000]))
    print("All data: ", sort.quick_sort(all_data.copy()[1:]))

    print("Merge sort: ")
    print("10: ", sort.merge_sort(all_data.copy()[1:10]))
    print("100: ", sort.merge_sort(all_data.copy()[1:100]))
    print("1000: ", sort.merge_sort(all_data.copy()[1:1000]))
    print("10000: ", sort.merge_sort(all_data.copy()[1:10000]))
    print("100000: ", sort.merge_sort(all_data.copy()[1:100000]))
    print("1000000: ", sort.merge_sort(all_data.copy()[1:1000000]))
    print("All data: ", sort.merge_sort(all_data.copy()[1:]))


def sort_task2_data_random():
    all_data = []
    with open('/Users/jane/CSC365_Data/SYMPTOMDATA.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            all_data.append(row)

    random.shuffle(all_data)

    print("Insertion sort: ")
    print("10: ", sort.insertion_sort(all_data.copy()[1:10]))
    print("100: ", sort.insertion_sort(all_data.copy()[1:100]))
    print("1000: ", sort.insertion_sort(all_data.copy()[1:1000]))
    print("10000: ", sort.insertion_sort(all_data.copy()[1:10000]))
    print("100000: ", sort.insertion_sort(all_data.copy()[1:100000]))
    print("1000000: ", sort.insertion_sort(all_data.copy()[1:1000000]))
    print("All data: ", sort.insertion_sort(all_data.copy()[1:]))

    print("Quick sort: ")
    print("10: ", sort.quick_sort(all_data.copy()[1:10]))
    print("100: ", sort.quick_sort(all_data.copy()[1:100]))
    print("1000: ", sort.quick_sort(all_data.copy()[1:1000]))
    print("10000: ", sort.quick_sort(all_data.copy()[1:10000]))
    print("100000: ", sort.quick_sort(all_data.copy()[1:100000]))
    print("1000000: ", sort.quick_sort(all_data.copy()[1:1000000]))
    print("All data: ", sort.quick_sort(all_data.copy()[1:]))

    print("Merge sort: ")
    print("10: ", sort.merge_sort(all_data.copy()[1:10]))
    print("100: ", sort.merge_sort(all_data.copy()[1:100]))
    print("1000: ", sort.merge_sort(all_data.copy()[1:1000]))
    print("10000: ", sort.merge_sort(all_data.copy()[1:10000]))
    print("100000: ", sort.merge_sort(all_data.copy()[1:100000]))
    print("1000000: ", sort.merge_sort(all_data.copy()[1:1000000]))
    print("All data: ", sort.merge_sort(all_data.copy()[1:]))


def task3():
    age_dict()
    sort_task3_data()


def age_dict():
    with open('/Users/jane/CSC365_Data/SYMPTOMDATA_2.csv', 'r') as f:
        csv_reader = csv.reader(f)
        line_count = 0
        for row in csv_reader:
            if 0 < line_count:
                age = row[1]
                if age is '':
                    gender_bin(TASK3_DATA[11], "unknown", row)
                else:
                    age = float(age)
                    if age < 1.0:
                        gender_bin(TASK3_DATA[0], "<1", row)
                    elif 1.0 <= age < 3.0:
                        gender_bin(TASK3_DATA[1], "1-3", row)
                    elif 4.0 <= age < 11.0:
                        gender_bin(TASK3_DATA[2], "4-11", row)
                    elif 12.0 <= age < 18.0:
                        gender_bin(TASK3_DATA[3], "12-18", row)
                    elif 19.0 <= age < 30.0:
                        gender_bin(TASK3_DATA[4], "19-30", row)
                    elif 31.0 <= age < 40.0:
                        gender_bin(TASK3_DATA[5], "31-40", row)
                    elif 41.0 <= age < 50.0:
                        gender_bin(TASK3_DATA[6], "41-50", row)
                    elif 51.0 <= age < 60.0:
                        gender_bin(TASK3_DATA[7], "51-60", row)
                    elif 61.0 <= age < 70.0:
                        gender_bin(TASK3_DATA[8], "61-70", row)
                    elif 71.0 <= age < 80.0:
                        gender_bin(TASK3_DATA[9], "71-80", row)
                    elif 80.0 <= age:
                        gender_bin(TASK3_DATA[10], ">80", row)
                    else:
                        gender_bin(TASK3_DATA[11], "unknown", row)
            line_count += 1


def gender_bin(bin, age, row):
    if len(bin) < 1:
        bin.append(age)
        bin.append(0)
        bin.append([[], [], []])
    gender = row[2]

    if gender == 'F':
        vaccine_bin(bin[2][0], 'F', row)
    elif gender == 'M':
        vaccine_bin(bin[2][1], 'M', row)
    else:
        vaccine_bin(bin[2][2], 'unknown', row)

    if row[len(row) - 3] == 'Y':
        bin[1] += 1


def vaccine_bin(bin, gender, row):
    if len(bin) < 1:
        bin.append(gender)
        bin.append(0)
        bin.append([[], [], [], []])
    vaccine = row[3]

    if vaccine == "COVID19 (COVID19 (PFIZER-BIONTECH))":
        task2_data_array(bin[2][0], "Pfizer", row)
    elif vaccine == "COVID19 (COVID19 (MODERNA))":
        task2_data_array(bin[2][1], "Moderna", row)
    elif vaccine == "COVID19 (COVID19 (JANSSEN))":
        task2_data_array(bin[2][2], "J&J", row)
    else:
        task2_data_array(bin[2][3], "unknown", row)

    if row[len(row) - 3] == 'Y':
        bin[1] += 1


def task2_data_array(bin, vaccine_name, row):
    if len(bin) < 1:
        bin.append(vaccine_name)
        bin.append(0)
        bin.append([])

    bin[2].append(row)

    if row[len(row) - 3] == 'Y':
        bin[1] += 1


def sort_task3_data():
    total_deaths = 0
    for age_group in TASK3_DATA:
        if len(age_group) > 1:
            print("Age:", age_group[0])
            print("Deaths:", age_group[1])
            total_deaths += age_group[1]
            for gender in age_group[2]:
                if len(gender) > 1:
                    print("     Gender:", gender[0])
                    print("     Deaths:", gender[1])
                    for vaccine in gender[2]:
                        if len(vaccine) > 1:
                            print("         Vaccine name:", vaccine[0])
                            print("         Deaths:", vaccine[1])
                            sort.insertion_sort(vaccine[2])
    print("Total deaths:", total_deaths)


if __name__ == '__main__':
    task1()
    task2()
    task3()
