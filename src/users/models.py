from src.models import *

class User(BaseORM):
	__tablename__ = "users"

	id: Mapped[intpk]
	name: Mapped[str_100]
	rel_msgs_sent: Mapped[List["Message"]] = relationship("Message", back_populates="sender", foreign_keys="[Message.sender]", lazy="selectin")
	rel_msgs_recv: Mapped[List["Message"]] = relationship("Message", back_populates="reciever", foreign_keys="[Message.reciever]", lazy="selectin")
	# rel_posts: Mapped[List["Post"]] = relationship(back_populates="rel_author")
	# rel_channels: Mapped[List["Channel"]] = relationship(back_populates="rel_subs")
