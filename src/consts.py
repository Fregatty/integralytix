import enum


class StorageType(enum.Enum):
    S3 = "S3"


class ModuleType(enum.Enum):
    PEOPLE_COUNTER = "PEOPLE_COUNTER"
    STT = "STT"


class EventPriority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
