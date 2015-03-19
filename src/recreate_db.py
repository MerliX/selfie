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

    # Requirement.add('Основное 1а', 1, True)
    # Requirement.add('Основное 1b', 1, True)
    # Requirement.add('Основное 2а', 2, True)
    # Requirement.add('Основное 2b', 2, True)
    # Requirement.add('Основное 3а', 3, True)
    # Requirement.add('Основное 3b', 3, True)
    # Requirement.add('Основное 4а', 4, True)
    # Requirement.add('Основное 4b', 4, True)
    #
    # Requirement.add('Доп 1а', 1, False)
    # Requirement.add('Доп 1b', 1, False)
    # Requirement.add('Доп 1c', 1, False)
    # Requirement.add('Доп 2а', 2, False)
    # Requirement.add('Доп 2b', 2, False)
    # Requirement.add('Доп 2c', 2, False)
    # Requirement.add('Доп 3а', 3, False)
    # Requirement.add('Доп 3b', 3, False)
    # Requirement.add('Доп 3c', 3, False)
    # Requirement.add('Доп 4а', 4, False)
    # Requirement.add('Доп 4b', 4, False)
    # Requirement.add('Доп 4c', 4, False)

    User.add('Александр Абрамович', '', False)
    User.add('Борис Бурда', 'Яндекс', False)
    User.add('Василий Венедиктов', 'JetStyle', False)
    User.add('Дмитрий Дыров', 'СКБ Контур', False)
    User.add('Валерий Порча', 'Наумен', False)
    User.add('Николая Комаров', 'Наумен', False)
    User.add('Елена Куравлёва', 'Экстенсив', False)
    User.add('Иван Водопьянов', 'Предприниматель', False)
    User.add('Илья Мурманский', 'Сбербанк', False)
    User.add('Лёха Кофман', 'Дойче', True)
    User.add('Лёха Кирпичников', 'СКБ Контур', True)
    User.add('Таня Кирпичникова', 'JetStyle', True)

    db.close()


if __name__ == '__main__':
    recreate_database()
