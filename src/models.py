# -*- coding: utf-8 -*-

import os
from peewee import SqliteDatabase, Model, TextField, IntegerField, BooleanField, CharField, fn, \
                   ForeignKeyField, DateTimeField, JOIN_LEFT_OUTER
from settings import PHOTO_PATH, DB_PATH, SELFIE_REWARD

db = SqliteDatabase(DB_PATH)


class Requirement(Model):
    description = TextField()
    difficulty = IntegerField()
    is_basic = BooleanField(default=True)

    class Meta(object):
        database = db


class User(Model):
    name = CharField(unique=True)
    access_code = CharField(unique=True)
    score = IntegerField(default=0)

    @property
    def needs_more_selfie_tasks(self):
        # make first selfie before you get any new tasks
        if self.tasks.where(
                (Task.is_selfie_game == True) & (Task.is_approved == True)
                ).count() < 1:
            return False

        # you should always have 3 open tasks
        if self.tasks.where(
                (Task.is_selfie_game == True) & (Task.is_approved == False)
                ).count() < 3:
            return True

        return False

    @property
    def current_difficulty(self):
        return (self
            .tasks
            .select(fn.Max(Task.difficulty))
            .where(Task.is_selfie_game == True)
            .scalar()
        )

    @property
    def photo_url(self):
        try:
            first_selfie = self.tasks.where(
                (Task.is_selfie_game == True)
                & (Task.partner >> None)
                & (Task.is_complete == True)
            ).get()
        except Task.DoesNotExist:
            return '/selfies/unknown.jpg'
        return first_selfie.photo_url    

    class Meta(object):
        database = db


class Task(Model):
    assignee = ForeignKeyField(User, related_name='tasks')
    partner = ForeignKeyField(User, related_name='mentions', null=True)
    is_complete = BooleanField(default=False)
    is_photo_required = BooleanField(default=True)
    is_selfie_game = BooleanField(default=True)
    is_approved = BooleanField(default=False)
    is_rejected = BooleanField(default=False)
    approved_time = DateTimeField(null=True)
    description = TextField(null=True)
    reward = IntegerField(default=SELFIE_REWARD)
    difficulty = IntegerField()
    basic_requirement = ForeignKeyField(Requirement, null=True)

    @property
    def photo_path(self):
        return os.path.join(PHOTO_PATH, '%s.jpg' % self.id)

    @property
    def photo_url(self):
        return '/selfies/%s.jpg' % self.id

    def find_partner(self):
        try:
            self.partner = (User
                .select(User.id)
                .join(Task, JOIN_LEFT_OUTER, Task.partner)
                .where(
                    ~(User.id << self.assignee
                                     .tasks
                                     .select(Task.partner)
                                     .where(
                                        ~(Task.partner >> None) 
                                        & (Task.is_selfie_game == True)
                                     )
                    )
                    & (User.id != self.assignee.id)
                )
                .group_by(User.id)
                .order_by(fn.Count(Task.id), fn.Random())
                .get()
            )
        except User.DoesNotExist:
            pass

    def generate_description(self):
        difficulty_left = self.difficulty
        basic_requirement = None
        used_requirements = []
        exclude_requirements = [
            r.basic_requirement 
            for r in self.assignee.tasks.where(~(Task.basic_requirement >> None))
        ]

        try:
            while difficulty_left > 0:
                requirement = (Requirement
                    .select()
                    .where(
                        (Requirement.is_basic == (basic_requirement is None))
                        & (Requirement.difficulty <= difficulty_left)
                        & ~(Requirement.id << exclude_requirements)
                        & ~(Requirement.id << used_requirements)
                    )
                    .order_by(fn.Random())
                    .get()
                )

                difficulty_left -= requirement.difficulty
                used_requirements.append(requirement)
                if basic_requirement is None:
                    basic_requirement = requirement
        except Requirement.DoesNotExist:
            pass

        if used_requirements:
            self.description = ' '.join([r.description for r in used_requirements])
            self.basic_requirement = basic_requirement


    def delete_photo(self):
        os.remove(self.photo_path)

    class Meta(object):
        database = db
