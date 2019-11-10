import csv
import os


LABELS = ["Id", "Story Title", "User Story", "Acceptance Criteria", "Business value", "Estimation", "Status"]
FILENAME = "database/user_stories.csv"


def import_list_of_dicts(filename=FILENAME):
    exists = os.path.isfile(filename)
    if not exists:
        return None
    else:
        with open(filename, 'r') as f:
            read_dictionary = csv.DictReader(f, delimiter=',')
            result = []
            for row in read_dictionary:
                result.append(dict(row))
            return result


def export_dict(some_data_to_add, labels=LABELS, filename=FILENAME):
    exists = os.path.isfile(filename)

    with open(filename, "a+") as f:
        writer = csv.DictWriter(f, fieldnames=labels, delimiter=',')
        if not exists:
            writer.writeheader()
        writer.writerow(some_data_to_add)


def overwrite_file(updated_stories, filename=FILENAME, labels=LABELS):
    with open(filename, "w+") as f:
        writer = csv.DictWriter(f, fieldnames=labels, delimiter=',')
        writer.writeheader()
        for item in updated_stories:
            writer.writerow(item)