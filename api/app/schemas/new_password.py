from pydantic import BaseModel


class NewPasswordBase(BaseModel):
    user_id: str
    old_password: str
    new_password: str
    confirm_new_password: str
