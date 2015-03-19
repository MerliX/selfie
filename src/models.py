# -*- coding: utf-8 -*-

import os
import logging
import random
from itertools import chain
from peewee import SqliteDatabase, Model, TextField, IntegerField, BooleanField, CharField, fn, \
                   ForeignKeyField, DateTimeField, JOIN_LEFT_OUTER, PostgresqlDatabase
from settings import PHOTO_PATH, SQLITE_DB_PATH, USE_POSTGRES, POSTGRES_DB_NAME, SELFIE_REWARD, \
                     POSTGRES_USER, POSTGRES_HOST


if USE_POSTGRES:
    db = PostgresqlDatabase(
        database=POSTGRES_DB_NAME,
        user=POSTGRES_USER,
        host=POSTGRES_HOST,
        client_encoding='UTF8'
    )
else:
    db = SqliteDatabase(SQLITE_DB_PATH)

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class Requirement(Model):
    description = TextField()
    difficulty = IntegerField()
    is_basic = BooleanField(default=True)

    @staticmethod
    def add(requirement_description, requirement_difficulty, requirement_is_basic):
        if requirement_description and requirement_difficulty:
            return Requirement(
                description=requirement_description,
                difficulty=requirement_difficulty,
                is_basic=requirement_is_basic
            ).save()
        else:
            return None

    class Meta(object):
        database = db

class User(Model):
    name = CharField(unique=True)
    access_code = CharField(unique=True)
    score = IntegerField(default=0)
    company = CharField(default='')
    is_active = BooleanField(default=False)
    is_easy = BooleanField(default=False)

    @property
    def needs_more_selfie_tasks(self):
        # make first selfie before you get any new tasks
        if self.tasks.where(
                (Task.is_approved == True)
                ).count() < 1:
            return False

        # you should always have 3 open tasks
        if self.tasks.where(
                (Task.is_approved == False)
                ).count() < 3:
            return True

        return False

    @property
    def current_difficulty(self):
        return (self
            .tasks
            .select(fn.Max(Task.difficulty))
            .scalar())

    @property
    def photo_url(self):
        try:
            first_selfie = self.tasks.where(
                (Task.partner >> None)
                & (Task.is_complete == True)
            ).get()
        except Task.DoesNotExist:
            return '/selfies/unknown.jpg'
        return first_selfie.photo_url

    def ensure_tasks_generated(self):
        while self.needs_more_selfie_tasks:
            selfie = Task(assignee=self, difficulty=self.current_difficulty + 1)
            selfie.find_partner()
            if selfie.partner is None:
                return False
            selfie.generate_description()
            if selfie.description is None:
                return False
            selfie.save()
        return True


    @staticmethod
    def add(user_name, user_company, user_is_easy):
        try:
            user = User.get(User.name == user_name)
        except User.DoesNotExist:
            user = User(
                name=user_name,
                company=user_company,
                is_easy = user_is_easy
            )
            user.generate_access_code()
            user.save()
            task = Task(
                assignee=user,
                description=u'Сделай селфи, чтобы хорошо было видно лицо.',
                difficulty=0
            )
            task.save()
        return user

    def generate_access_code(self):
        self.access_code = ''.join(
            chain(*zip(
                random.sample('bcdfghjklmnpqrstvwxz', 3),
                random.sample('aeiouy', 3)
            ))
        )

    class Meta(object):
        database = db

class Task(Model):
    assignee = ForeignKeyField(User, related_name='tasks', on_delete='CASCADE')
    partner = ForeignKeyField(User, related_name='mentions', null=True, on_delete='CASCADE')
    is_complete = BooleanField(default=False)
    is_approved = BooleanField(default=False)
    is_rejected = BooleanField(default=False)
    approved_time = DateTimeField(null=True)
    description = TextField(null=True)
    reward = IntegerField(default=SELFIE_REWARD)
    difficulty = IntegerField()

    @property
    def photo_path(self):
        return os.path.join(PHOTO_PATH, '%s.jpg' % self.id)

    @property
    def photo_url(self):
        return '/selfies/%s.jpg' % self.id

    def get_participants_for_user(self, user):
        result = u'Ты' if self.assignee == user else self.assignee.name
        if (self.partner):
            result = result + u' и ' + (u'Ты' if self.partner == user else self.partner.name)
        return result

    def find_partner(self):
        try:
            query = (User
                .select(User.id)
                .join(Task, JOIN_LEFT_OUTER, Task.partner)
                .where(
                    ~(User.id << self.assignee
                                     .tasks
                                     .select(Task.partner)
                                     .where(~(Task.partner >> None)))
                    & (User.is_easy == (self.difficulty == 1))
                    & (User.id != self.assignee.id)
                    & (User.is_active == True)
                )
                .group_by(User.id))

            # Difficulty 3 always with the user from the same company
            if self.difficulty == 3:
                query = query.order_by((User.company == self.assignee.company).desc(), fn.Count(Task.id), fn.Random())
            else:
                query = query.order_by(fn.Count(Task.id), fn.Random())

            self.partner = query.get()
        except User.DoesNotExist:
            pass

    def generate_description(self):
        difficulty_left = self.difficulty
        used_requirements = []
        found_basic = False

        try:
            while difficulty_left > 0:

                condition = (Requirement.difficulty <= difficulty_left) \
                    & (Requirement.difficulty > difficulty_left / 3)

                if found_basic or self.difficulty == 1:
                    condition &= (Requirement.is_basic != True)

                if len(used_requirements) > 0:
                    condition &= ~(Requirement.id << used_requirements)

                requirement = (Requirement
                    .select()
                    .where(condition)
                    .order_by(
                        RequirementUsage
                            .select(fn.count(RequirementUsage.id))
                            .where((RequirementUsage.user == self.assignee) & (RequirementUsage.requirement == Requirement.id)),
                        fn.Random())
                    .get()
                )

                difficulty_left -= requirement.difficulty
                used_requirements.append(requirement)
                if requirement.is_basic:
                    found_basic = True

        except Requirement.DoesNotExist:
            return

        self.description = ' '.join([r.description for r in sorted(used_requirements, key=lambda req: -req.is_basic)])

        for req in used_requirements:
            RequirementUsage(user=self.assignee, requirement = req).save()

    def delete_photo(self):
        os.remove(self.photo_path)

    class Meta(object):
        database = db

class RequirementUsage(Model):
    user = ForeignKeyField(User, null=False, index=True, on_delete='CASCADE')
    requirement = ForeignKeyField(Requirement, null=False, index=True, on_delete='CASCADE')

    class Meta(object):
        database = db