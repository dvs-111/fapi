print("init users-models")
from typing import TYPE_CHECKING
from models import BaseORM, Mapped, mapped_column, List, intpk, str_100, relationship
if TYPE_CHECKING:
	from messages.models import Message

class User(BaseORM):
	__tablename__ = "users"

	id: Mapped[intpk]
	name: Mapped[str_100]

	# rel_msgs_sent: Mapped[List["Message"]] = relationship(
	rel_msgs_sent = relationship(
		"Message",
		# argument=lambda: Message,
		back_populates="rel_usr_sndr",
		# foreign_keys=["Message.sender"],
		foreign_keys="[Message.sender]",
		# foreign_keys="Message.sender",
		# foreign_keys=lambda: [Message.sender],
		lazy="selectin"
		# lazy="joined"
	)
# """
	rel_msgs_recv: Mapped[List["Message"]] = relationship(
		"Message",
		# argument=lambda: Message,
		back_populates="rel_usr_recv",
		# foreign_keys=["Message.receiver"],
		foreign_keys="[Message.receiver]",
		# foreign_keys="Message.receiver",
		# foreign_keys=lambda: [Message.receiver],
		lazy="selectin"
	)
# """
	# rel_posts: Mapped[List["Post"]] = relationship(back_populates="rel_author")
	# rel_channels: Mapped[List["Channel"]] = relationship(back_populates="rel_subs")
# from messages.models import Message