class ITTicket:
    """Represents an IT support ticket."""
    
    def __init__(self, ticket_id: int, title: str, priority: str, status: str, created_date: str):
        self.__id = ticket_id
        self.__title = title
        self.__priority = priority
        self.__status = status
        self.__created_date = created_date
    
    def get_id(self) -> int:
        return self.__id
    
    def get_title(self) -> str:
        return self.__title
    
    def get_priority(self) -> str:
        return self.__priority
    
    def get_status(self) -> str:
        return self.__status
    
    def get_created_date(self) -> str:
        return self.__created_date
    
    def assign_to(self, staff: str) -> None:
        self.__assigned_to = staff
    
    def close_ticket(self) -> None:
        self.__status = "closed"
    
    def reopen_ticket(self) -> None:
        self.__status = "open"
    
    def get_priority_level(self) -> int:
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__priority.lower(), 0)
    
    def is_open(self) -> bool:
        return self.__status.lower() in ["open", "in progress"]
    
    def is_high_priority(self) -> bool:
        return self.__priority.lower() in ["high", "critical"]
    
    def __str__(self) -> str:
        return f"ITTicket(id={self.__id}, title='{self.__title}', priority={self.__priority}, status={self.__status})"