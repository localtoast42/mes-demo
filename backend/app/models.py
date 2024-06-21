from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=255)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class Part(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    part_number: str = Field(default=None, max_length=255)
    name: str = Field(default=None, max_length=255)
    revision: str = Field(default=None, max_length=255)


class WorkOrder(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: str
    part_id: int | None = Field(default=None, foreign_key="part.id")
    material_list: "MaterialList"


class OperationLink(SQLModel, table=True):
    predecessor_id: int | None = Field(default=None, foreign_key="operation.id", primary_key=True)
    successor_id: int | None = Field(default=None, foreign_key="operation.id", primary_key=True)


class Operation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    status: str
    description: str | None
    work_order_id: int | None = Field(default=None, foreign_key="workorder.id")
    work_order: WorkOrder | None = Relationship()
    predecessors: list["Operation"] = Relationship(link_model=OperationLink)
    successors: list["Operation"] = Relationship(link_model=OperationLink)


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