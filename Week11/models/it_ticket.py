class ITTicket:
    """Represents an IT support ticket."""
    
    def __init__(self, ticket_id: int, title: str, priority: str, status: str, assigned_to: str = "Unassigned"):
        self.__id = ticket_id
        self.__title = title
        self.__priority = priority
        self.__status = status
        self.__assigned_to = assigned_to
    
    def assign_to(self, staff: str) -> None:
        """Assign the ticket to a staff member."""
        self.__assigned_to = staff
    
    def close_ticket(self) -> None:
        """Close the ticket."""
        self.__status = "Closed"
    
    def get_id(self) -> int:
        """Get the ticket ID."""
        return self.__id
    
    def get_title(self) -> str:
        """Get the ticket title."""
        return self.__title
    
    def get_priority(self) -> str:
        """Get the ticket priority."""
        return self.__priority
    
    def get_status(self) -> str:
        """Get the ticket status."""
        return self.__status
    
    def get_assigned_to(self) -> str:
        """Get who the ticket is assigned to."""
        return self.__assigned_to
    
    def __str__(self) -> str:
        """String representation of the ticket."""
        return (
            f"Ticket {self.__id}: {self.__title} "
            f"[{self.__priority}] - {self.__status} (assigned to: {self.__assigned_to})"
        )