from enum import Enum


class TransferType(Enum):
    Deposit = "Deposit"
    Withdrawal = "Withdrawal"


class Status(Enum):
    Pending = "Pending"
    Completed = "Completed"
    Cancelled = "Cancelled"
