# -*- coding: utf-8 -*-

import logging
from src.models import Task, User

logger = logging.getLogger('peewee')
logger.setLevel(logging.ERROR)

t = Task()
u = User()
t.assignee = u

for i in range(15):
    t.difficulty = i+1
    t.generate_description()
    print '%d: %s\n' % (i+1, t.description)
