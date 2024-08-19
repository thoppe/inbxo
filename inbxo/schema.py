from .query import Query
from typing import List
from pydantic import BaseModel

Questions = {}


class EmailDomain(BaseModel):
    domain_name: str
    expanded_name: str
    is_academic: bool
    country_of_origin_ISO_3166_alpha2: str


Questions["email"] = Query("You help identify email domain names", EmailDomain)


class AcademicInstitution(BaseModel):
    expanded_name: str
    is_university: bool
    is_R1: bool
    is_minority_serving_institution: bool
    State: str
    enrollment: int
    known_for: List[str]


Questions["academic"] = Query(
    "You add more information to a given academic institution", AcademicInstitution
)
