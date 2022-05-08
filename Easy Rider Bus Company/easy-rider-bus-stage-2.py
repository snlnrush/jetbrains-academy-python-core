import json
import re


json_data = input()

test_data = """[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Av.",
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
        "a_time": "8:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "OO",
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:77"
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
        "stop_name": "Elm",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "09:45"
    },
    {
        "bus_id": 256,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 7,
        "stop_type": "A",
        "a_time": "09:59"
    },
    {
        "bus_id": 256,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "10.12"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "bourbon street",
        "next_stop": 6,
        "stop_type": "S",
        "a_time": "38:13"
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

json_obj = json.loads(json_data)


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


error_dict, all_errors = check_format(json_obj)

print(f'Format validation: {all_errors} errors')
for key, val in error_dict.items():
    print(f'{key}: {val}')


"""
Stage 2/6: Correct syntax
Description
You managed to fill in all the missing data and correct the mistakes with the types. However, you noticed that there are multiple problems with suffix names for the stops: sometimes they are incorrect, and sometimes they are simply missing. As if that was not enough, you also realized that there are errors in the arrival times.

It seems like you have to carefully look at the entire "Format" column in the first part of the documentation.

Here are the documents that you have: documentation and diagram of the bus lines.

Objectives
The string containing the data in JSON format is passed to standard input.
Check that the data format complies with the documentation.
Only the fields that have such a requirement are relevant, i.e. stop_name, stop_type, a_time, so, please, count errors only for them.
Like in the previous stage, print the information about the number of found errors in total and in each field. Remember that there might be no errors at all.
The output should have the same formatting as shown in the example.
If you can't find the necessary information in the stage description, it can probably be found in the attached documentation.

Note that the time format is military time (24 hours, hh:mm). That means that there are certain restrictions:

the first digit cannot be 3, 4, etc.;
hours less than 10 should have zero in front of them, e.g. 08:34;
the delimiter should be colon :.
Example
Input:

[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Av.",
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
        "a_time": "8:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "OO",
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:77"
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
        "stop_name": "Elm",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "09:45"
    },
    {
        "bus_id": 256,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 7,
        "stop_type": "A",
        "a_time": "09:59"
    },
    {
        "bus_id": 256,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "10.12"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "bourbon street",
        "next_stop": 6,
        "stop_type": "S",
        "a_time": "38:13"
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

Format validation: 9 errors
stop_name: 3
stop_type: 2
a_time: 4
"""