from src.models import *
from src.users.models import *

class Message(BaseORM):
	__tablename__ = "messages"
	
	id: Mapped[intpk]
	sender: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
	reciever: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
	text: Mapped[str]