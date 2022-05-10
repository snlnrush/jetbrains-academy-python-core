import json
import re
from collections import Counter


json_data = input()

test_data = """[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "08:12"
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 5,
        "stop_type": "",
        "a_time": "08:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": 256,
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "09:20"
    },
    {
        "bus_id": 256,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "09:45"
    },
    {
        "bus_id": 256,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 7,
        "stop_type": "",
        "a_time": "09:59"
    },
    {
        "bus_id": 256,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "10:12"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "Bourbon Street",
        "next_stop": 6,
        "stop_type": "S",
        "a_time": "08:13"
    },
    {
        "bus_id": 512,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:16"
    }
]"""


def check_bus_id(value):
    return isinstance(value, int)


def check_stop_id(value):
    return isinstance(value, int)


def check_stop_name(value):
    if isinstance(value, str) and bool(value):
        elements = value.split(' ')
        return elements[0].istitle() and len(elements) > 1 and elements[-1] in {'Avenue', 'Street', 'Road', 'Boulevard'}
    else:
        return False


def check_next_stop(value):
    return isinstance(value, int)


def check_stop_type(value):
    return isinstance(value, str) and (value in {'', 'S', 'O', 'F'})


def check_a_time(value):
    reg_exp = '[0-2][0-9]:[0-5][0-9]$'
    return bool(re.match(reg_exp, value))


def check_format(js_obj, all_err=0):
    err_dict = {'stop_name': 0, 'stop_type': 0, 'a_time': 0}
    for dict_obj in js_obj:
        for key, check_def in {'stop_name': check_stop_name, 'stop_type': check_stop_type,
                               'a_time': check_a_time}.items():
            if not check_def(dict_obj[key]):
                err_dict[key] += 1
                all_err += 1
    return err_dict, all_err


def check_bus_line(js_obj):
    stops_list = []
    for obj in js_obj:
        if check_bus_id(obj['bus_id']):
            stops_list.append(obj['bus_id'])
    stops_dict = Counter(stops_list)
    print('Line names and number of stops:')
    for key, val in stops_dict.items():
        print(f'bus_id: {key}, stops: {val}')


json_obj = json.loads(json_data)


check_bus_line(json_obj)


"""
Stage 3/6: Bus line info
Description
It wasn't easy, but finally, you verified the data format and the required fields. It is now time to check how many bus lines we have and how many stops there are on each line. Before we can go further with sorting out the database, it would be a good idea to check that the information is complete.

Here are the documents that you have: documentation and diagram of the bus lines.

Objectives
The string containing the data in JSON format is passed to standard input.
Find the names of all the bus lines.
Verify the number of stops for each line.
The output should have the same formatting as shown in the example.
If you can't find the necessary information in the stage description, it can probably be found in the attached documentation.

Example
Input:

[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "08:12"
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 5,
        "stop_type": "",
        "a_time": "08:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": 256,
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "09:20"
    },
    {
        "bus_id": 256,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "09:45"
    },
    {
        "bus_id": 256,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 7,
        "stop_type": "",
        "a_time": "09:59"
    },
    {
        "bus_id": 256,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "10:12"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "Bourbon Street",
        "next_stop": 6,
        "stop_type": "S",
        "a_time": "08:13"
    },
    {
        "bus_id": 512,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:16"
    }
]
Output:

Line names and number of stops:
bus_id: 128, stops: 4
bus_id: 256, stops: 4
bus_id: 512, stops: 2
"""