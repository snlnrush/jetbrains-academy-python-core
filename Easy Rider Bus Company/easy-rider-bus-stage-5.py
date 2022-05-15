import json
import re
from datetime import datetime
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
        "a_time": "08:17"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:07"
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
        "a_time": "09:44"
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


def check_unlost_time(js_obj):
    obj_start = js_obj[0]
    check_time = datetime.strptime(obj_start['a_time'], '%H:%M')
    check_stop = obj_start['bus_id']
    error_bus_stops = {}
    for obj in js_obj[1:]:
        if datetime.strptime(obj['a_time'], '%H:%M') <= check_time and check_stop == obj['bus_id']:
            if obj['bus_id'] not in error_bus_stops:
                error_bus_stops[obj['bus_id']] = obj['stop_name']
        check_time = datetime.strptime(obj['a_time'], '%H:%M')
        check_stop = obj['bus_id']
    if error_bus_stops:
        print('Arrival time test:')
        for key, val in error_bus_stops.items():
            print(f'bus_id line {key}: wrong time on station {val}')
    else:
        print('Arrival time test:')
        print('OK')


def main():
    json_obj = json.loads(json_data)
    check_unlost_time(json_obj)


if __name__ == '__main__':
    main()


"""
Stage 5/6: Unlost in time

Description

It is now time to move on to a more detailed analysis. First, check that arrival times for the upcoming stops make sense: they are supposed to be increasing, that is, going forward in time.
After all, there is no information in the documentation that your company offers time travel.

Here are the documents that you have: documentation and diagram of the bus lines.

Objectives

The string containing the data in JSON format is passed to standard input.
Check that the arrival time for the upcoming stops for a given bus line is increasing.
If the arrival time for the next stop is earlier than or equal to the time of the current stop, stop checking that bus line and remember the name of the incorrect stop.
Display the information for those bus lines that have time anomalies. For the correct stops, do not display anything.
If all the lines are correct timewise, print OK.

The output should have the same formatting as shown in the example.

If you can't find the necessary information in the stage description, it can probably be found in the attached documentation.

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
        "a_time": "08:17"
    },
    {
        "bus_id": 128,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:07"
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
        "a_time": "09:44"
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
Output 1:

Arrival time test:
bus_id line 128: wrong time on station Fifth Avenue
bus_id line 256: wrong time on station Sunset Boulevard
Example 2

Input 2:

[
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

Arrival time test:
OK
"""