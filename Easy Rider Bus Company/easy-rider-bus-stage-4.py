import json
import re
from collections import Counter


json_data = input()

test_data = """[
{"bus_id" : 128, "stop_id" : 1, "stop_name" : "Fifth Avenue", "next_stop" : 4, "stop_type" : "S", "a_time" : "08:12"},
{"bus_id" : 128, "stop_id" : 4, "stop_name" : "Abbey Road", "next_stop" : 5, "stop_type" : "", "a_time" : "08:19"},
{"bus_id" : 128, "stop_id" : 5, "stop_name" : "Santa Monica Boulevard", "next_stop" : 8, "stop_type" : "O", "a_time" : "08:25"},
{"bus_id" : 128, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : 11, "stop_type" : "", "a_time" : "08:37"},
{"bus_id" : 128, "stop_id" : 11, "stop_name" : "Beale Street", "next_stop" : 12, "stop_type" : "", "a_time" : "09:20"},
{"bus_id" : 128, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 14, "stop_type" : "", "a_time" : "09:45"},
{"bus_id" : 128, "stop_id" : 14, "stop_name" : "Bourbon Street", "next_stop" : 19, "stop_type" : "O", "a_time" : "09:59"},
{"bus_id" : 128, "stop_id" : 19, "stop_name" : "Prospekt Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "10:12"},
{"bus_id" : 256, "stop_id" : 2, "stop_name" : "Pilotow Street", "next_stop" : 3, "stop_type" : "S", "a_time" : "08:13"},
{"bus_id" : 256, "stop_id" : 3, "stop_name" : "Startowa Street", "next_stop" : 8, "stop_type" : "", "a_time" : "08:16"},
{"bus_id" : 256, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : 10, "stop_type" : "", "a_time" : "08:29"},
{"bus_id" : 256, "stop_id" : 10, "stop_name" : "Lombard Street", "next_stop" : 12, "stop_type" : "", "a_time" : "08:44"},
{"bus_id" : 256, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 13, "stop_type" : "O", "a_time" : "08:46"},
{"bus_id" : 256, "stop_id" : 13, "stop_name" : "Orchard Road", "next_stop" : 16, "stop_type" : "", "a_time" : "09:13"},
{"bus_id" : 256, "stop_id" : 16, "stop_name" : "Sunset Boulevard", "next_stop" : 17, "stop_type" : "", "a_time" : "09:26"},
{"bus_id" : 256, "stop_id" : 17, "stop_name" : "Khao San Road", "next_stop" : 20, "stop_type" : "O", "a_time" : "10:25"},
{"bus_id" : 256, "stop_id" : 20, "stop_name" : "Michigan Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "11:26"},
{"bus_id" : 512, "stop_id" : 6, "stop_name" : "Arlington Road", "next_stop" : 7, "stop_type" : "S", "a_time" : "11:06"},
{"bus_id" : 512, "stop_id" : 7, "stop_name" : "Parizska Street", "next_stop" : 8, "stop_type" : "", "a_time" : "11:15"},
{"bus_id" : 512, "stop_id" : 8, "stop_name" : "Elm Street", "next_stop" : 9, "stop_type" : "", "a_time" : "11:56"},
{"bus_id" : 512, "stop_id" : 9, "stop_name" : "Niebajka Avenue", "next_stop" : 15, "stop_type" : "", "a_time" : "12:20"},
{"bus_id" : 512, "stop_id" : 15, "stop_name" : "Jakis Street", "next_stop" : 16, "stop_type" : "", "a_time" : "12:44"},
{"bus_id" : 512, "stop_id" : 16, "stop_name" : "Sunset Boulevard", "next_stop" : 18, "stop_type" : "", "a_time" : "13:01"},
{"bus_id" : 512, "stop_id" : 18, "stop_name" : "Jakas Avenue", "next_stop" : 19, "stop_type" : "", "a_time" : "14:00"},
{"bus_id" : 1024, "stop_id" : 21, "stop_name" : "Karlikowska Avenue", "next_stop" : 12, "stop_type" : "S", "a_time" : "13:01"},
{"bus_id" : 1024, "stop_id" : 12, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "14:00"},
{"bus_id" : 512, "stop_id" : 19, "stop_name" : "Prospekt Avenue", "next_stop" : 0, "stop_type" : "F", "a_time" : "14:11"}
]
"""


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


def parse_stops(js_obj):
    bus_parsed = {}
    for obj in js_obj:
        obj = list(obj.values())
        if obj[0] not in bus_parsed:
            bus_parsed[obj[0]] = [[obj[2], ], {obj[4], }]
        else:
            bus_parsed[obj[0]][0].append(obj[2])
            bus_parsed[obj[0]][1].add(obj[4])
    return bus_parsed


def check_spec_stops(js_obj):
    bus_parsed = parse_stops(js_obj)
    all_stops_tmp = [x[0] for x in bus_parsed.values()]
    all2 = [j for i in all_stops_tmp for j in i]
    cross_stops_sets = [set(x[0]) for x in bus_parsed.values()]
    cross_stops_names = [name_stop for name_stop in set.union(*cross_stops_sets) if all2.count(name_stop) > 1]
    for key, val in bus_parsed.items():
        if ('S' not in val[1]) or ('F' not in val[1]):
            print(f'There is no start or end stop for the line: {key}.')
            break
    else:
        stops_parsed = {'S': set(), 'F': set(), '': set(), 'O': set()}
        for obj in js_obj:
            obj = list(obj.values())
            stops_parsed[obj[4]].add(obj[2])
        print(f"Start stops: {len(stops_parsed['S'])} {sorted(stops_parsed['S'])}")
        print(f"Transfer stops: {len(cross_stops_names)} {sorted(cross_stops_names)}")
        print(f"Finish stops: {len(stops_parsed['F'])} {sorted(stops_parsed['F'])}")


def main():
    json_obj = json.loads(json_data)
    check_spec_stops(json_obj)


if __name__ == '__main__':
    main()


"""
Stage 4/6: Special stops
Description
The missing part of the specification is nowhere to be found. You need to recover and update the data contained in the second part of the documentation.

The company is growing, the number of bus lines is ever-increasing, and logically, more bus stops appear. You need to prepare an appropriate function that calculates this data so that it doesn't have to be checked manually in the future.

Here are the documents that you have: documentation and diagram of the bus lines.

Objectives
The string containing the data in JSON format is passed to standard input.
Make sure each bus line has exactly one starting point (S) and one final stop (F).
If a bus line does not meet this condition, stop checking and print a message about it. Do not continue checking the other bus lines.
If all bus lines meet the condition, count how many starting points and final stops there are. Print their unique names in alphabetical order.
Count the transfer stops and print their unique names in alphabetical order. A transfer stop is a stop shared by at least two bus lines.
The output should have the same formatting as shown in the example.
If you cannot find the necessary information in the stage description, it can probably be found in the attached documentation.

Examples
Example 1

Input 1:

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
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "Bourbon Street",
        "next_stop": 6,
        "stop_type": "",
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
Output 1:

There is no start or end stop for the line: 512.
Example 2

Input 2:

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
Output 2:

Start stops: 3 ['Bourbon Street', 'Pilotow Street', 'Prospekt Avenue']
Transfer stops: 3 ['Elm Street', 'Sesame Street', 'Sunset Boulevard']
Finish stops: 2 ['Sesame Street', 'Sunset Boulevard']
"""