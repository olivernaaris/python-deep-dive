# project1
In this project our goal is to validate one dictionary structure against a template dictionary.
A typical example of this might be working with JSON data inputs in an API. You are trying to validate this received JSON against some kind of template to make sure the received JSON conforms to that template (i.e. all the keys and structure are identical - value types being important, but not the value itself - so just the structure, and the data type of the values).
To keep things simple we'll assume that values can be either single values (like an integer, string, etc), or a dictionary, itself only containing single values or other dictionaries, recursively. In other words, we're not going to deal with lists as possible values. Also, to keep things simple, we'll assume that all keys are required, and that no extra keys are permitted.
In practice, we would not have these simplifying assumptions, and although we could definitely write this ourselves, there are many 3rd party libraries that already exist to do this (such as jsonschema, marshmallow, and many more, some of which I'll cover lightly in some later videos.)
For example, you might have this template:

template = {
    'user_id': int,
    'name': {
        'first': str,
        'last': str
    },
    'bio': {
        'dob': {
            'year': int,
            'month': int,
            'day': int
        },
        'birthplace': {
            'country': str,
            'city': str
        }
    }
}

So, a JSON document such as this would match the template:
john = {
    'user_id': 100,
    'name': {
        'first': 'John',
        'last': 'Cleese'
    },
    'bio': {
        'dob': {
            'year': 1939,
            'month': 11,
            'day': 27
        },
        'birthplace': {
            'country': 'United Kingdom',
            'city': 'Weston-super-Mare'
        }
    }
}

But this one would not match the template (missing key):
eric = {
    'user_id': 101,
    'name': {
        'first': 'Eric',
        'last': 'Idle'
    },
    'bio': {
        'dob': {
            'year': 1943,
            'month': 3,
            'day': 29
        },
        'birthplace': {
            'country': 'United Kingdom'
        }
    }
}

And neither would this one (wrong data type):
michael = {
    'user_id': 102,
    'name': {
        'first': 'Michael',
        'last': 'Palin'
    },
    'bio': {
        'dob': {
            'year': 1943,
            'month': 'May',
            'day': 5
        },
        'birthplace': {
            'country': 'United Kingdom',
            'city': 'Sheffield'
        }
    }
}

Write a function such this:
def validate(data, template):
    # implement
    # and return True/False
    # in the case of False, return a string describing 
    # the first error encountered
    # in the case of True, string can be empty
    return state, error

That should return this:
- validate(john, template) --> True, ''
- validate(eric, template) --> False, 'mismatched keys: bio.birthplace.city'
- validate(michael, template) --> False, 'bad type: bio.dob.month'
Better yet, use exceptions instead of return codes and strings!
