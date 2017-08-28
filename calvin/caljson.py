#!/usr/bin/env python

import json
import logging
import traceback

def add_line_numbers(lines, start, width):
    added_lines = []
    for i in range(len(lines)):
        lno = i + start
        added_lines.append(str(lno).zfill(width) + ": " + lines[i])
    return added_lines

def get_json_error(exc, context_lines=5):
    if hasattr(exc, "lineno") and hasattr(exc, "colno") and hasattr(exc, "doc"):
        template = exc.doc
        lines = template.split("\n")
        max_line_number = len(lines)
        max_line_length = max(*[len(l) for l in lines])
        max_line_number_length = len(str(max_line_number))
        added_width = max_line_number_length + 2

        line_number = exc.lineno - 1 # it's 1-indexed                                                                                                                                                                                                                        \
                                                                                                                                                                                                                                                                              
        column_number = exc.colno
        preceding_line_start = max(0, line_number - context_lines)
        following_line_end = min(max_line_number, line_number + context_lines + 1)
        exc_message = str(exc)
        line_length = max(*[len(l) for l in lines[preceding_line_start:following_line_end]]) + added_width
        line_length = max(len(exc_message), line_length)
        preceding_block = "\n".join(add_line_numbers(lines[preceding_line_start:line_number], preceding_line_start, max_line_number_length))
        problematic_line = add_line_numbers([lines[line_number]], line_number, max_line_number_length)[0]
        following_block = "\n".join(add_line_numbers(lines[line_number+1:following_line_end], line_number+1, max_line_number_length))
        pointer_format = "-"*(max(0, column_number + added_width - 1)) + "{pointer}" + "-"*(line_length - column_number - added_width)
        separator_line = "="*line_length
        error_lines = []
        error_lines.append(separator_line)
        error_lines.append(exc_message)
        error_lines.append(separator_line)
        error_lines.append(preceding_block)
        error_lines.append(pointer_format.format(pointer="v"))
        error_lines.append(problematic_line)
        error_lines.append(pointer_format.format(pointer="^"))
        error_lines.append(following_block)
        error_lines.append(separator_line)
        return "\n".join(error_lines)
    return None

class blob(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__predefined_attributes__ = [a for a in dir(self)]
        self.__predefined_attributes__.append("__predefined_attributes__")
        for key in self.keys():
            if not key in self.__predefined_attributes__:
                setattr(self, key, self[key])
                pass
            pass
        pass

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if not key in self.__predefined_attributes__:
            setattr(self, key, self[key])
            pass
        pass

    def __delitem__(self, key):
        super().__delitem__(key)
        if not key in self.__predefined_attributes__:
            delattr(self, key)
            pass
        pass

class CalvinEncoder(json.JSONEncoder):
    def default(self, obj):
        # Let the base class default method raise the TypeError
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return "<unserializable object of type {}>".format(type(obj))

def dump(*args, **kwargs):
    return json.dump(cls=CalvinEncoder, *args, **kwargs)

def dumps(*args, **kwargs):
    return json.dumps(cls=CalvinEncoder, *args, **kwargs)

def dumpf(obj, filename, *args, **kwargs):
    with open(filename, "w") as f:
        return dump(obj, f, *args, **kwargs)

def load(*args, **kwargs):
    try:
        return json.load(*args, **kwargs)
    except json.decoder.JSONDecodeError as e:
        msg = get_json_error(e)
        if msg:
            logging.warn(e)
        raise e
    
def loads(*args, **kwargs):
    try:
        return json.loads(*args, **kwargs)
    except json.decoder.JSONDecodeError as e:
        msg = get_json_error(e)
        if msg:
            logging.warn(e)
        raise e

def loadf(filename, *args, **kwargs):
    with open(filename, "r") as f:
        return load(f, *args, **kwargs)
