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

class User(BaseORM):
	__tablename__ = "users"

	id: Mapped[intpk]
	name: Mapped[str_100]
	rel_msgs_sent: Mapped[List["Message"]] = relationship("Message", back_populates="sender", foreign_keys="[Message.sender]", lazy="selectin")
	rel_msgs_recv: Mapped[List["Message"]] = relationship("Message", back_populates="reciever", foreign_keys="[Message.reciever]", lazy="selectin")
	# rel_posts: Mapped[List["Post"]] = relationship(back_populates="rel_author")
	# rel_channels: Mapped[List["Channel"]] = relationship(back_populates="rel_subs")

class Message(BaseORM):
	__tablename__ = "messages"
	
	id: Mapped[intpk]
	sender: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
	reciever: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
	text: Mapped[str]
'''
class Post(BaseORM):
	__tablename__ = "posts"

	id: Mapped[intpk]
	title: Mapped[str_100]
	text: Mapped[str]
	author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"))

	# rel_author: Mapped["User"] = relationship(back_populates="rel_posts", foreign_keys=[author_id])
	# rel_channel: Mapped["User"] = relationship(back_populates="rel_posts", foreign_keys=[channel_id])

class Channel(BaseORM):
	__tablename__ = "channels"

	id: Mapped[intpk]
	name: Mapped[str]

	rel_subs: Mapped[int] = relationship(back_populates="rel_channels")

class Chunk(BaseORM):
	__tablename__ = "chunks"

	id: Mapped[intpk]
	name: Mapped[str]
# '''