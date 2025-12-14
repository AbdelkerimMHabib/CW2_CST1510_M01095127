"""IT Ticket entity class"""

class ITTicket:
    """Represents an IT support ticket."""
    
    def __init__(self, ticket_id: int, title: str, priority: str, 
                 status: str, created_date: str, assigned_to: str = ""):
        
        """Initialize ITTicket instance."""
        self.__id = ticket_id
        self.__title = title
        self.__priority = priority
        self.__status = status
        self.__created_date = created_date
        self.__assigned_to = assigned_to
    
    #Getters

    def get_id(self) -> int:
        """Returns the ticket ID"""
        return self.__id
    
    def get_title(self) -> str:
        """Returns the ticket title"""
        return self.__title
    
    def get_priority(self) -> str:
        """Returns the ticket priority"""
        return self.__priority
    
    def get_status(self) -> str:
        """Returns the ticket status"""
        return self.__status
    
    def get_created_date(self) -> str:
        """Returns the ticket creation date"""
        return self.__created_date
    
    def get_assigned_to(self) -> str:
        """Returns the staff member assigned to the ticket"""
        return self.__assigned_to
    
    #Action methods
    
    def assign_to(self, staff: str) -> None:
        """Assigns the ticket to a staff member"""
        self.__assigned_to = staff
    
    def close_ticket(self) -> None:
        """Closes the ticket"""
        self.__status = "Closed"
    
    #string representation
    def __str__(self) -> str:
        """Returns string representation of the ticket"""
        assigned_info = f" (assigned to: {self.__assigned_to})" if self.__assigned_to else ""
        return (
            f"Ticket {self.__id}: {self.__title} "
            f"[{self.__priority}] – {self.__status}{assigned_info}"
        )