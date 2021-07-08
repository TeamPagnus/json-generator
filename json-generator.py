#!/usr/bin/env python
# -*- coding: utf8 -*-

import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, help='set seed for generation')
args = parser.parse_args()

if args.seed != None:
    random.seed(args.seed)

JsonWhiteSpaceTypes = {
    'HORIZONTAL_TAB': chr(9),
    'LINEFEED': chr(10),
    'CARRIAGE_RETURN': chr(13),
    'SPACE': chr(32)
}

# https://www.crockford.com/mckeeman.html
def get_random_character():
    # from 0x20 to 0x10fff
    char = '"'
    while char in ['"', '\\']:
        char = chr(random.randrange(0x10ffff - 0x20) + 0x20)
    return char

def get_random_hex():
    # ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    hex_values = [chr(i + ord('0')) for i in range(10)]
    
    # ['a', 'b', 'c', 'd', 'e', 'f']
    hex_values += [chr(i + ord('a')) for i in range(6)]

    # ['A', 'B', 'C', 'D', 'E', 'F']
    hex_values += [chr(i + ord('A')) for i in range(6)]

    return random.choice(hex_values)

def generate_random_string():
    result = '"'
    while random.randrange(2):
        if random.randrange(2):
            result += get_random_character()
        else:
            result += '\\'
            result += random.choice(['"', '\\', '/', 'b', 'f', 'n', 't', 'r', 'u'])
            if result[:-1] == 'u':
                result += get_random_hex()
                result += get_random_hex()
                result += get_random_hex()
                result += get_random_hex()
    result += '"'
    return result

def generate_random_number():
    result = ""
    if random.randrange(2):
        result += '-'
    if random.randrange(2):
        result += '0'
    else:
        result += chr(ord('1') + random.randrange(9))
        while random.randrange(2):
            result += chr(ord('0') + random.randrange(10))
    # fraction
    if  random.randrange(2):
        result += '.'
        result += chr(ord('0') + random.randrange(10))
        while random.randrange(2):
            result += chr(ord('0') + random.randrange(10))
    # exponent
    if  random.randrange(2):
        if random.randrange(2):
            result += 'e'
        else:
            result += 'E'
        if random.randrange(2):
            result += '+'
        else:
            result += '-'
        result += chr(ord('0') + random.randrange(10))
        while random.randrange(2):
            result += chr(ord('0') + random.randrange(10))
    return result

def generate_random_object():
    result = "{"
    if random.randrange(2):
        result += generate_random_whitespace()
    else:
        result += generate_random_whitespace()
        result += generate_random_string()
        result += generate_random_whitespace()
        result += ':'
        result += generate_random_whitespace()
        result += generate_random_value()
        while random.randrange(2):
            result += ','
            result += generate_random_whitespace()
            result += generate_random_string()
            result += generate_random_whitespace()
            result += ':'
            result += generate_random_whitespace()
            result += generate_random_value()
    result += '}'
    return result

def generate_random_array():
    result = "["
    if random.randrange(2):
        result += generate_random_whitespace()
    else:
        result += generate_random_value()
        while random.randrange(2):
            result += ","
            result += generate_random_value()
    result += "]"
    return result

JsonCleanValueGenerators = {
    'STRING': generate_random_string,
    'NUMBER': generate_random_number,
    'OBJECT': generate_random_object,
    'ARRAY': generate_random_array,
    'TRUE': lambda: "true",
    'FALSE': lambda: "false",
    'NULL': lambda: "null"
}

def generate_random_whitespace():
    result = ""
    while random.randrange(2):
        result += random.choice(list(JsonWhiteSpaceTypes.values()))
    return result

def generate_random_value():
    result = ""
    result += generate_random_whitespace()
    result += random.choice(list(JsonCleanValueGenerators.values()))()
    result += generate_random_whitespace()
    return result

print(generate_random_value())
