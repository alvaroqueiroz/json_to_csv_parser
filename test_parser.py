def test_json_to_csv():

    from parse_json_to_csv import json_to_csv

    import csv

    json_to_csv('datafile1.json', 'out1.csv')
    json_to_csv('datafile2.json', 'out2.csv')

    with open('out1.csv', newline='') as csvfile:
        obj1 = csv.DictReader(csvfile)

        str_obj1 = ''
        for row in obj1:
            str_obj1 = str_obj1+str(row)

    with open('out2.csv', newline='') as csvfile:
        obj2 = csv.DictReader(csvfile)

        str_obj2 = ''
        for row in obj2:
            str_obj2 = str_obj2+str(row)

    with open('out_expected.csv', newline='') as csvfile:
        obj_expected = csv.DictReader(csvfile)

        str_obj_expected = ''
        for row in obj_expected:
            str_obj_expected = str_obj_expected+str(row)

    assert str_obj1 == str_obj_expected
    assert str_obj2 == str_obj_expected