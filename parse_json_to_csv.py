def flatten_json(dict_data, delim):
    """
    function to serialize or "flatten" json data
    inputs
    dict_data: python dict
    delim: string to separate nested fields
    output
    dict with flatten fields

    """
    flatten = {}
    for key in dict_data.keys():

        if isinstance(dict_data[key], dict):
            nested_keys = flatten_json(dict_data[key], delim)

            for nested_key in nested_keys.keys():
                flatten[key + delim + nested_key] = nested_keys[nested_key]
        else:
            flatten[key] = dict_data[key]

    return flatten

def json_to_csv(data_file_input, data_file_output='out.csv', delim='_'):
    """
    function that reads a file with data in a json-like format
    and translates that to a csv formats and writtes it to a file

    inputs
    data_file_inpput: string name of the file with json-like format
    data_file_output: string with name of the file to be created with csv data
    delim: string with delimeter for when there are nested objects in the json

    output
    file with name given with csv data
    """

    # first, open file with data to read its contents as string in a variable
    with open(data_file_input) as data_file:
        data_str = data_file.read()

    # problem: json.loads method needs double quotes in key/values, but some values have quotations
    # ex: "somekey":" some value "cake tips" more text"
    # this is a problem in python
    # we need to find the double ticks (") inside the key-values and replace them with (')
    # one possible solution is to use regexes to find the quotations and lambda functions to replace them
    
    import re
    data_str = re.sub(r'[A-Za-z0-9 ]"[A-Za-z0-9 ]*"[A-Za-z0-9 ]',
                    lambda x: x.group().replace('"', "'"), data_str)
    
    # we need to test if the string is already in the list of dicts format
    if not data_str.startswith('[') and not data_str.endswith(']'):
        # json.loeads expects a list of objects, so we need to add [] and , between the objects
        # and add (,) between objects
        data_str = '['+data_str.replace("}\n{", "}, {")+']'

    # for some 'reasons' we need to exclude symbols that appear only in raw strings
    data_str = data_str.replace('\\"', '')
    data_str = data_str.replace('\\r', '')
    data_str = data_str.replace('\\n', '')
    data_str = data_str.replace('\\', '')

    # finally we can use json.loads to load the string as a list of python dicts
    import json
    dict_list = json.loads(data_str)

    # if there is nested data, we flatten it
    flatten_json_list = []
    for dict_data in dict_list:
        flatten_json_list.append(flatten_json(dict_data, delim))

    # csv files normally contain a header with field names
    header = []

    # append all key-names of the first entry as the header
    for key in flatten_json_list[0]:
        header.append(key)

    # we use csv writter to create the file
    import csv
    f = csv.writer(open(data_file_output, "w"))
    f.writerow(header)

    # for each entry, we need to loop over keys and append data to line
    for record in flatten_json_list:
        currentrecord = []
        for key in header:
            currentrecord.append(record[key])
        f.writerow(currentrecord)

if __name__ == '__main__':
    json_to_csv('all_data.json')