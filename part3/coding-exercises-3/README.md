# Exercises
## Exercise #1
Let's revisit an exercise we did right after the section on dictionaries.

You have text data spread across multiple servers. Each server is able to analyze this data and return a dictionary that contains words and their frequency.

Your job is to combine this data to create a single dictionary that contains all the words and their combined frequencies from all these data sources. Bonus points if you can make your dictionary sorted by frequency (highest to lowest).

For example, you may have three servers that each return these dictionaries:

d1 = {'python': 10, 'java': 3, 'c#': 8, 'javascript': 15}
d2 = {'java': 10, 'c++': 10, 'c#': 4, 'go': 9, 'python': 6}
d3 = {'erlang': 5, 'haskell': 2, 'python': 1, 'pascal': 1}
Your resulting dictionary should look like this:

d = {'python': 17,
     'javascript': 15,
     'java': 13,
     'c#': 12,
     'c++': 10,
     'go': 9,
     'erlang': 5,
     'haskell': 2,
     'pascal': 1}
If only servers 1 and 2 return data (so d1 and d2), your results would look like:

d = {'python': 16,
     'javascript': 15,
     'java': 13,
     'c#': 12,
     'c++': 10, 
     'go': 9}
This was one solution to the problem:

def merge(*dicts):
    unsorted = {}
    for d in dicts:
        for k, v in d.items():
            unsorted[k] = unsorted.get(k, 0) + v
            
    # create a dictionary sorted by value
    return dict(sorted(unsorted.items(), key=lambda e: e[1], reverse=True))
Implement two different solutions to this problem:

a: Using defaultdict objects

b: Using Counter objects

## Exercise #2
Suppose you have a list of all possible eye colors:

eye_colors = ("amber", "blue", "brown", "gray", "green", "hazel", "red", "violet")
Some other collection (say recovered from a database, or an external API) contains a list of Person objects that have an eye color property.

Your goal is to create a dictionary that contains the number of people that have the eye color as specified in eye_colors. The wrinkle here is that even if no one matches some eye color, say amber, your dictionary should still contain an entry "amber": 0.

Here is some sample data:

class Person:
    def __init__(self, eye_color):
        self.eye_color = eye_color
from random import seed, choices
seed(0)
persons = [Person(color) for color in choices(eye_colors[2:], k = 50)]
As you can see we built up a list of Person objects, none of which should have amber or blue eye colors

Write a function that returns a dictionary with the correct counts for each eye color listed in eye_colors.

## Exercise #3
You are given three JSON files, representing a default set of settings, and environment specific settings. The files are included in the downloads, and are named:

common.json
dev.json
prod.json
Your goal is to write a function that has a single argument (the environment name) and returns the "combined" dictionary that merges the two dictionaries together, with the environment specific settings overriding any common settings already defined.

For simplicity, assume that the argument values are going to be the same as the file names, without the .json extension. So for example, dev or prod.

The wrinkle: We don't want to duplicate data for the "merged" dictionary - use ChainMap to implement this instead.