# -*- coding: utf-8 -*-

import logging
from src.models import Task, User

logger = logging.getLogger('peewee')
logger.setLevel(logging.ERROR)

t = Task()
u = User()
t.assignee = u

for i in range(15):
    for j in range(5):
        t.difficulty = i
        t.generate_description()
        print t.description
