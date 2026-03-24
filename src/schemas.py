
from pydantic import BaseModel as pd_BaseModel, ConfigDict
from typing import List

class pd_Base(pd_BaseModel):
	model_config = ConfigDict(from_attributes=True)

# class pd_UserOut(pd_UserPost):
# 	owned_channels: List[pd_ChannelPost] = []
# 	subscriptions: List[pd_ChannelPost] = []