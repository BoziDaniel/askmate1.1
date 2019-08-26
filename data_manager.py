import connection as cn


def generate_new_id(file_path): #át kéne írni általánosabban úgy, h az answer id-ra is jó legyen
    sorted_questions = descending_sort_data_by_parameter(
        (cn.get_all_data_from_file(file_path)), 'submission_time')
    newest_id = (sorted_questions[0])['id']
    new_id = int(newest_id)+1
    return new_id


def descending_sort_data_by_parameter(data_to_be_sorted, parameter):
    sorted_data = sorted(data_to_be_sorted, key=lambda k: k[parameter], reverse=True)
    return sorted_data


def get_subdictionary_by_id(question_id, file_path):
    data = cn.get_all_data_from_file(file_path)
    filtered_data = []
    for element in data:
        if question_id in element.values():
            filtered_data.append(element)
    return filtered_data


def get_values_from_dict(dict_data):
    values_of_a_dict = []
    for key in dict_data:
        values_of_a_dict.append(dict_data[key])
    return values_of_a_dict


def get_a_column_from_data(column_name, list_of_dicts):
    items_in_column = []
    for subdict in list_of_dicts:
        items_in_column.append(subdict[column_name])
    return items_in_column


# #mind2 fv müxik, ez a 2. ra próba
# x = [{"id": 112, "name": "aga"}, {"id": 214, "name": "wzew"}, {"id": 1, "name": "awrrza"}]
# y = descending_sort_data_by_id(x)
# print(y)
# z = get_values_from_dict({"id": 112, "name": "aga"})
# print(z)
#
# print(get_a_column_from_data('title', questions_path))
