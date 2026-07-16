print("init msg-models")
from typing import TYPE_CHECKING
from models import BaseORM, Mapped, mapped_column, ForeignKey, intpk, relationship
if TYPE_CHECKING:
	from users.models import User

class Message(BaseORM):
	__tablename__ = "messages"
	
	id: Mapped[intpk]
	sender: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
	receiver: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
	text: Mapped[str]
# """
	# rel_usr_sndr: Mapped["User"] = relationship(
	rel_usr_sndr = relationship(
		"User",
		# argument=lambda: User,
		back_populates="rel_msgs_sent",
		# back_populates=lambda: User.rel_msgs_recv,
		foreign_keys=[sender],
		# foreign_keys=["Message.sender"],
		lazy="selectin"
		# lazy="joined"
	)
# """
# """
	rel_usr_recv: Mapped["User"] = relationship(
		"User",
		# argument=lambda: User,
		back_populates="rel_msgs_recv",
		# back_populates=lambda: User.rel_msgs_recv,
		foreign_keys=[receiver],
		# foreign_keys=["Message.receiver"],
		lazy="selectin"
	)
# """
# from users.models import User