# -*- coding: utf-8 -*-

from models import db, User, Requirement, Task, RequirementUsage


def recreate_database():
    db.connect()

    for table in [RequirementUsage, Task, User, Requirement]:
        try:
            db.drop_table(table)
        except:
            db.rollback()

    db.create_tables([User, Requirement, Task, RequirementUsage])

    db.close()


if __name__ == '__main__':
    recreate_database()
