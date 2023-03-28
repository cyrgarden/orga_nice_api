from sqlalchemy import desc, func
from sqlalchemy.orm import Session, Query  # type: ignore
from app.schemas.utils import OrderBy, Search
from typing import Union
import requests
from math import sin, cos, sqrt, atan2, radians
import re
import smtplib
from email.message import EmailMessage


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
    
    """
    Find all elements of a given model with search criteria.
    """
    order_by_field = getattr(model, orderby.value)
    if reverse:
        order_by_field = desc(order_by_field)
    query = db.query(model)
    query = criteria_to_query(query, model, criteria)

    return query.order_by(order_by_field).offset(offset).limit(limit).all()


def count_all(db:Session, component_model):
    rows = db.query(func.count(component_model.id)).scalar()
    print(f"TOTAL COUNT: {rows}")
    return rows

#Function to email format validity
def is_mail_valid(email: str):
    regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if(re.search(regex,email)):
        return True
    else:
        return False

def is_password_valid(password : str ) -> bool :
    if (len(password)<= 8 ):
        return False
    if not re.search("[a-z]", password):
        return False
    return True


def send_mail(db:Session, receiver_email:str, subject:str, body :str):

    # Load the .env variables

    sender_email = 'organice.staff@gmail.com'
    password = 'gkapybirkslhnouu'

    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    message.set_content(body) 


    # Connexion au serveur SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    # Envoi de l'email
    server.send_message(message)

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
    return distance

def get_coordinates(city_name, country_code):
    api_key = '25d7c5abdb7b1ffbabe8cb99ccc3afc7'
    res = requests.get(url=f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=1&appid={api_key}')
    return (res.json()[0]['lat'], res.json()[0]['lon'])


