from datetime import datetime
from pydantic import BaseModel


class SessionBase(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
