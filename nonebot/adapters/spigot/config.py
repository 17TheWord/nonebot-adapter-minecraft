from pydantic import Extra, BaseModel


class Config(BaseModel):
    class Config:
        extra = Extra.ignore
        allow_population_by_field_name = True
