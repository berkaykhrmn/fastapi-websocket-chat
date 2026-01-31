from pydantic import BaseModel, EmailStr, field_validator, ValidationError

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str

    @field_validator("password_confirm")
    @classmethod
    def passwords_match(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValidationError("Passwords do not match")
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'