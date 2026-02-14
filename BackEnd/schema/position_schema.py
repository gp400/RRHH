from pydantic import BaseModel
from enums.position_risk_level import PositionRiskLevel

class PositionSchema(BaseModel):

    id: int | None
    name: str
    risk_level: PositionRiskLevel
    min_wage: int
    max_wage: int
    state: bool