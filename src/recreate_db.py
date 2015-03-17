# -*- coding: utf-8 -*-

from models import db, User, Requirement, Task


def recreate_database():
    db.connect()

    try:
        db.drop_tables([User, Requirement, Task])
    except:
        db.rollback()

    db.create_tables([User, Requirement, Task])

    Requirement.add('Вы у входа.', 1, True)
    Requirement.add('Вы у сцены.', 1, True)
    Requirement.add('Вы в столовой.', 2, True)
    Requirement.add('Вы на сцене.', 2, True)
    Requirement.add('Вы на улице.', 3, True)

    Requirement.add('Вы жонглируете тремя или более невидимыми предметами.', 1, False)
    Requirement.add('Вы обмениваетесь визитками.', 1, False)
    Requirement.add('По вам видно, что вы довольны докладами.', 1, False)
    Requirement.add('Вы меряетесь кто из вас более agile.', 2, False)
    Requirement.add('Вы оба в очках.', 2, False)
    Requirement.add('Один из вас держит другого на руках.', 2, False)
    Requirement.add('Вы читаете умную книжку.', 2, False)
    Requirement.add('Вы чините баг.', 2, False)
    Requirement.add('Вокруг вас 5 девушек.', 3, False)

    User.add('Александр Абрамович', '')
    User.add('Борис Бурда', 'Яндекс')
    User.add('Василий Венедиктов', 'JetStyle')
    User.add('Дмитрий Дыров', 'СКБ Контур')

    db.close()


if __name__ == '__main__':
    recreate_database()
