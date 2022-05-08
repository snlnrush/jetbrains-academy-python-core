import json


json_data = input()

check_data = """[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": 8.12
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "",
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
        "stop_id": "7",
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": "",
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": ""
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
        "next_stop": "0",
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
        "bus_id": "512",
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 0,
        "stop_type": 5,
        "a_time": "08:16"
    }
]"""

error_dict = {'bus_id': 0, 'stop_id': 0, 'stop_name': 0, 'next_stop': 0, 'stop_type': 0, 'a_time': 0}

json_obj = json.loads(json_data)
all_errors = 0


def check_bus_id(value):
    return isinstance(value, int)


def check_stop_id(value):
    return isinstance(value, int)


def check_stop_name(value):
    return isinstance(value, str) and bool(value)


def check_next_stop(value):
    return isinstance(value, int)


def check_stop_type(value):
    return isinstance(value, str) and (value in {'', 'S', 'O', 'F'})


def check_a_time(value):
    return bool(value) and isinstance(value, str) and ':' in value


for dict_obj in json_obj:
    for key, check_def in {'bus_id': check_bus_id, 'stop_id': check_stop_id,
                           'stop_name': check_stop_name, 'next_stop': check_next_stop,
                           'stop_type': check_stop_type, 'a_time': check_a_time}.items():
        if not check_def(dict_obj[key]):
            error_dict[key] += 1
            all_errors += 1

print(f'Type and required field validation: {all_errors} errors')
for key, val in error_dict.items():
    print(f'{key}: {val}')


"""
Stage 1/6: Checking the data type

Description

You just started sorting out the existing database of the "Easy Rider" bus company. As you take the first look at the data, you realize that it's not going to be easy.

Sometimes numbers are missing from where they should definitely be. You also noticed that sometimes there are too many or too few characters.
Fortunately, there is documentation to help you sort out this mess.
However, this documentation is not a hundred percent complete: part of it was torn away when your colleague spilled coffee on it.
Let's see what we can make out.

Here are the documents that you have: documentation and diagram of the bus lines.

Objectives

The string containing the data in JSON format is passed to standard input.
Check that the data types match.
Check that the required fields are filled in.
Display the information about the number of found errors in total and in each field. Keep in mind that there might be no errors at all.
The output should have the same formatting as shown in the example.
No need to worry about the format now. Let's at first just make sure that the fields have the right type and all required ones are filled.
If you can't find the necessary information in the stage description, it can probably be found in the attached documentation.

Note that the type Char is present among the data types.

Example

Input:

[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": 8.12
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "",
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
        "stop_id": "7",
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": "",
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": ""
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
        "next_stop": "0",
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
        "bus_id": "512",
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 0,
        "stop_type": 5,
        "a_time": "08:16"
    }
]
Output:

Type and required field validation: 8 errors
bus_id: 2
stop_id: 1
stop_name: 1
next_stop: 1
stop_type: 1
a_time: 2
"""