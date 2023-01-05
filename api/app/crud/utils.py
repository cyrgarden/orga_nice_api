from sqlalchemy import desc, func
from sqlalchemy.orm import Session, Query  # type: ignore
from app.schemas.utils import OrderBy, Search


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
    criteria: Search | None,
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

