from dataclasses import dataclass, asdict
from typing import Dict

@dataclass
class CessionResult:
    risk_id: str
    risk_amount: float
    currency: str
    retention: float
    reinsurer_a_cession: float
    global_re_group_cession: float

    def to_dict(self) -> Dict:
        return asdict(self)