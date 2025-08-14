from enum import Enum

class UrgencyLevel(Enum):
    CRITICAL = "Critical Emergency"
    URGENT = "Urgent"
    SEMI_URGENT = "Semi-Urgent"
    STANDARD = "Standard"
    NON_URGENT = "Non-Urgent"