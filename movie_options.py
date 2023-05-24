import os
from models import Movie, Actor

"""complete but testing still to be done"""

movies = [
    Movie(title="Harry Potter and the Philosopher's Stone", release_year="2001"),
    Movie(title="Harry Potter and the Chamber of Secrets", release_year="2002"),
    Movie(title="Harry Potter and the Prisoner of Azkaban", release_year="2004"),
    Movie(title="Harry Potter and the Philosopher's Stone", release_year="2001"),
    Movie(title="Harry Potter and the Goblet of Fire", release_year="2005"),
    Movie(title="Harry Potter and the Order of the Phoenix", release_year="2007"),
    Movie(title="Harry Potter and the Half Blood Prince", release_year="2009"),
    Movie(title="Harry Potter and the Deathly Hallows - Part 1", release_year="2010"),
    Movie(title="Harry Potter and the Deathly Hallows - Part 2", release_year="2011")
]

actors = [
    Actor(name="Daniel Radcliffe", age=33, gender="male"),
    Actor(name="Emma Watson", age=33, gender="female"),
    Actor(name="Rupert Grint", age=34, gender="male"),
    Actor(name="Maggie Smith", age=88, gender="female"),
    Actor(name="Ralph Fiennes", age=60, gender="male"),
    Actor(name="Bonnie Wright", age=32, gender="female"),
    Actor(name="Jim Broadbent", age=73, gender="male"),
    Actor(name="Miriam Margolyes", age=82, gender="female")

]
