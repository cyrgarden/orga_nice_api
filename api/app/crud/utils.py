from sqlalchemy import desc, func
from sqlalchemy.orm import Session, Query  # type: ignore
from app.schemas.utils import OrderBy, Search
from typing import Union
import requests
import random
from math import sin, cos, sqrt, atan2, radians
import re
import smtplib
import os



def criteria_to_query(query: Query, model: object, criteria: object):
    """
    Convert a criteria object to a query.

    A criteria object is a dictionary with the following type of keys:
    - "<property>_min": search for every element with a value greater or equal to the given value
    - "<property>_max": search for every element with a value lower or equal to the given value
    - "<property>": search for every element with a value like the given value if the value is a string
    and for every element with a value equal to the given value if the value is a number.
    """
    if criteria is not None:
        for attr, value in dict(criteria).items():  # type: ignore
            if value is None:
                continue
            if "_min" in attr:
                attr = attr.replace("_min", "")
                query = query.filter(getattr(model, attr) >= value)
            elif "_max" in attr:
                attr = attr.replace("_max", "")
                query = query.filter(getattr(model, attr) <= value)
            elif "_like" in attr and type(value) is str:
                attr = attr.replace("_like", "")
                query = query.filter(getattr(model, attr).like(f"%{value}%"))
            else:
                query = query.filter(getattr(model, attr) == value)
    return query


def get_all(
    db: Session,
    model: object,
    limit: int,
    offset: int,
    orderby: OrderBy,
    reverse: bool,
    criteria: Union[Search, None] = None
):
    print("FOR UTILS GET_ALL FUNCTION: \n ")
    print(f"model : {model}")
    print(f"limit: {limit}")
    print(f"offset: {offset}")
    print(f"orderby: {orderby}")
    print(f"reverse: {reverse}")
    print(f"criteria: {criteria}")
    """
    Find all elements of a given model with search criteria.
    """
    order_by_field = getattr(model, orderby.value)
    print("check 1 ")
    if reverse:
        order_by_field = desc(order_by_field)
    query = db.query(model)
    print("check 2 ")
    query = criteria_to_query(query, model, criteria)
    print("check 3 ")

    return query.order_by(order_by_field).offset(offset).limit(limit).all()


def count_all(db:Session, component_model):
    rows = db.query(func.count(component_model.id)).scalar()
    print(f"TOTAL COUNT: {rows}")
    return rows

#Function to email format validity
def is_mail_valid(email: str):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):
        print("Valid Email")
        return True
    else:
        print("Invalid Email")
        return False


def send_mail(db:Session, receiver_email:str, subject:str, body :str):

    #Load the .env variables

    smtp_server = os.getenv('SMTP_SERVER')
    port = os.getenv('SMTP_PORT')

    username = os.getenv('SENDER_USERNAME')
    password = os.getenv('SENDER_PASSWORD')
    sender_email = os.getenv('SENDER_MAIL')
    
    message = f"""From: {sender_email} To: {receiver_email} Subject: {subject}\n\n{body} """

    # Connexion au serveur SMTP
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(username, password)

    # Envoi de l'email
    server.sendmail(sender_email, receiver_email, message)

    # Fermeture de la connexion
    server.quit()



def compute_distance(lat1, lon1, lat2, lon2) -> float :

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    #print("Result:", distance)
    return distance

def get_coordinates(city_name, country_code):
    api_key = '25d7c5abdb7b1ffbabe8cb99ccc3afc7'
    #res = requests.get(url=f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}', headers=headers, auth=auth)
    res = requests.get(url=f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=1&appid={api_key}')
    return (res.json()[0]['lat'], res.json()[0]['lon'])


