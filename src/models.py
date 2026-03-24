from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from typing import Annotated, List

intpk = Annotated[int, mapped_column(primary_key=True)]
str_100 = Annotated[str, mapped_column(String(100))]

class BaseORM(DeclarativeBase):
	...
	# type_annotation_map = {
	# 	str_200: String(str_200.__metadata__[0])
	# }
