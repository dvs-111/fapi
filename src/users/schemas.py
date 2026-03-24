from src.schemas import *


class pd_UserPost(pd_Base):
	name: str

class pd_UserOut(pd_UserPost):
	id: int