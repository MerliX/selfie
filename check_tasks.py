# -*- coding: utf-8 -*-

from src.models import Task


t = Task()

for i in range(15):
    for j in range(5):
        t.difficulty = i
        t.generate_description()
        print t.description
