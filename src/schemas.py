from pydantic import BaseModel as PdBaseModel, ConfigDict
from typing import List

class PdBase(PdBaseModel):
	model_config = ConfigDict(from_attributes=True)

# class pd_UserOut(pd_UserPost):
# 	owned_channels: List[pd_ChannelPost] = []
# 	subscriptions: List[pd_ChannelPost] = []