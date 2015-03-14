# -*- coding: utf-8 -*-

from models import db, User, Requirement, Task


def recreate_database():
    db.connect()

    try:
        db.drop_tables([User, Requirement, Task])
    except:
        db.rollback()

    db.create_tables([User, Requirement, Task])

    Requirement.add("Вы у входа.", 1, True)
    Requirement.add("Вы у сцены.", 1, True)
    Requirement.add("Вы в столовой.", 2, True)
    Requirement.add("Вы на сцене.", 2, True)
    Requirement.add("Вы на улице.", 3, True)
    Requirement.add("Вы жонглируете тремя или более невидимыми предметами.", 1, False)
    Requirement.add("Вы обмениваетесь визитками.", 2, False)
    Requirement.add("Вы довольны докладом.", 2, False)
    Requirement.add("Вы решаете кто из вас более agile.", 3, False)

    User.add("Александр Абрамович")
    User.add("Борис Бурда")
    User.add("Василий Венедиктов")
    User.add("Дмитрий Дыров")

    db.close()

if __name__ == "__main__":
	recreate_database()
