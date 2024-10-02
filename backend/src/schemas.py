from pydantic import BaseModel


class ExpenseBase(BaseModel):
    user_tg_id: int
    amount: float
    category: str | None = None
    comment: str | None = None
    payment_type: str


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    tg_id: int
    tg_username: str
    tg_first_name: str | None = None
    tg_language_code: str | None = None


class UserCreate(BaseModel):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
