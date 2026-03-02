from typing import List

from pydantic import BaseModel


class EmailSchema(BaseModel):
    email: List[str]
