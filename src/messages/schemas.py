from src.schemas import *

class pd_MessagePost(pd_Base):
	sender: int
	reciever: int
	text: str

class pd_MessageOut(pd_Base):
	id: int
	income: bool
	text: str