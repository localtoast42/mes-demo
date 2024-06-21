from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=255)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    username: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)


class UserUpdate(UserBase):
    username: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class PartBase(SQLModel):
    part_number: str = Field(default=None, max_length=255)
    name: str = Field(default=None, max_length=255)
    revision: str = Field(default=None, max_length=255)


class PartCreate(PartBase):
    pass


class Part(PartBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class PartPublic(PartBase):
    id: int


class WorkOrderBase(SQLModel):
    status: str | None = Field(default="Unreleased")
    part_id: int | None = Field(default=None, foreign_key="part.id")


class WorkOrderCreate(WorkOrderBase):
    pass


class WorkOrder(WorkOrderBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class WorkOrderPublic(WorkOrderBase):
    id: int


class OperationLink(SQLModel, table=True):
    predecessor_id: int | None = Field(default=None, foreign_key="operation.id", primary_key=True)
    successor_id: int | None = Field(default=None, foreign_key="operation.id", primary_key=True)


class OperationBase(SQLModel):
    name: str = Field(max_length=255)
    number: int = Field(default=0, ge=0)
    status: str | None = Field(default="Unreleased")


class OperationCreate(OperationBase):
    pass


class Operation(OperationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    work_order_id: int | None = Field(default=None, foreign_key="workorder.id")
    work_order: WorkOrder | None = Relationship()
    predecessors: list["Operation"] = Relationship(link_model=OperationLink)
    successors: list["Operation"] = Relationship(link_model=OperationLink)


class OperationPublic(OperationBase):
    id: int


class MaterialList(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    items: list["MaterialLine"] = Relationship()
    work_order_id: int | None = Field(default=None, foreign_key="workorder.id")
    work_order: WorkOrder | None = Relationship()


class MaterialLine(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quantity_required: int = Field(default=0)
    part_id: int | None = Field(default=None, foreign_key="part.id")
    material_list_id: int | None = Field(default=None, foreign_key="materiallist.id")


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None