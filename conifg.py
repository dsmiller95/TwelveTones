from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Config:
    note_duration: float
    auto_advance_period: float
