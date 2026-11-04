from datetime import date

from pydantic import BaseModel
class Variable(BaseModel):
    date : date
    store_nbr : int
    family : str
    onpromotion : int 