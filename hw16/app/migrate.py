import os
import json
from app import db, models
# from sqlalchemy.sql import exists
import re
from datetime import datetime

DATE_PATTERN = re.compile(r'\d{2}/\d{2}/\d{4}')

def load_fixture(file_path):
    """
    Загружает содержимое фикстур
    :param file_path: Путь до файла с фикстурой.
    :return: Данные из фикстуры, либо пустой список если не найдено.
    """
    content = []
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf-8') as file:
            content = json.load(file)
    return content


def migrate_user_roles(fixture_path):
    fixture_content = load_fixture(fixture_path)

    for role in fixture_content:

        # if db.session.query(exists().where(models.UserRole.id == role['id'] )) is False:
        # можно отсортировать этим вариантом (+ нужно подключить from sqlalchemy.sql import exists (см. 4 строка)

        if db.session.query(models.UserRole).filter(models.UserRole.id == role['id']).first() is None:
            new_role = models.UserRole(**role)
            db.session.add(new_role)

    db.session.commit()


def migrate_users(fixture_path):
    fixture_content = load_fixture(fixture_path)

    for user in fixture_content:
        if db.session.query(models.User).filter(models.User.id == user['id']).first() is None:
            db.session.add(models.User(**user))

    db.session.commit()


def migrate_orders(fixture_path):
    fixture_content = load_fixture(fixture_path)

    for order in fixture_content:

        for field_name, field_value in order.items():

            # if isinstance(field_value, str) and re.search(DATE_PATTERN, field_value):
            #     order[field_name] = datetime.strptime(field_value, '%m/%d/%').date()
            # проверка через регулярное выражение

            if isinstance(field_value, str) and field_value.count('/') == 2:
                order[field_name] = datetime.strptime(field_value, '%m/%d/%Y').date()

        if db.session.query(models.Order).filter(models.Order.id == order['id']).first() is None:
            db.session.add(models.Order(**order))

    db.session.commit()


def migrate_offers(fixture_path):
    fixture_content = load_fixture(fixture_path)

    for offer in fixture_content:
        if db.session.query(models.Offer).filter(models.Offer.id == offer['id']).first() is None:
            db.session.add(models.Offer(**offer))

    db.session.commit()