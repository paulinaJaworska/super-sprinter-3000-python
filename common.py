import data_manager
import os
# import uuid

FILENAME = "database/user_stories.csv"
STATUSES = ['planning', 'todo', 'in progress', 'review', 'done']

# generates id automatically, we should be careful because a few user might log sth at the same time
# instead use UUID
def id_generator(filename=FILENAME):
    exists = os.path.isfile(filename)
    result = None
    if not exists:
        return "0"
    else:
        with open(filename, 'r') as f:
            data = data_manager.import_list_of_dicts()
            for row in data:
                result = int(row["Id"])
        return str(result + 1)
    #return uuid.uuid1()

# saves the data to csv file
def save_row_to_file(data_to_save):
    next_id = id_generator()
    data_to_save.update({'Id': next_id})
    data_to_save.update({'Status': STATUSES[0]})
    data_manager.export_dict(data_to_save)


# read the data from the file and returns it as a list of dicts
def get_data_from_file():
    result = data_manager.import_list_of_dicts()
    return result


def update_story(story_id, data_to_save):
    stories = data_manager.import_list_of_dicts()
    data_to_save.update({"Id": story_id})
    story_line = int(story_id)
    for story in stories:
        if story["Id"] == story_id:
            stories[story_line] = data_to_save
    data_manager.overwrite_file(stories)