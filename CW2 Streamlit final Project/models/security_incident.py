"""Security Incident entity class"""

class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""
    
    def __init__(self, incident_id: int, title: str, severity: str, 
                 status: str, date: str, description: str = ""):
        """Initialize SecurityIncident instance."""
        self.__id = incident_id
        self.__title = title
        self.__severity = severity
        self.__status = status
        self.__date = date
        self.__description = description
    
    #Getters
    def get_id(self) -> int:
        """Returns the incident ID"""
        return self.__id
    
    def get_title(self) -> str:
        """Returns the incident title"""
        return self.__title
    
    def get_severity(self) -> str:
        """Returns the incident severity"""
        return self.__severity
    
    def get_status(self) -> str:
        """Returns the incident status"""
        return self.__status
    
    def get_date(self) -> str:
        """Returns the incident date"""
        return self.__date
    
    def get_description(self) -> str:
        """Returns the incident description"""
        return self.__description
    
    #Action methods
    def update_status(self, new_status: str) -> None:
        """Updates the incident status"""
        self.__status = new_status
    
    def get_severity_level(self) -> int:
        """Return an integer severity level ."""
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__severity.lower(), 0)
    
    #String representation
    def __str__(self) -> str:
        """Returns string representation of the incident"""
        return f"Incident {self.__id} [{self.__severity.upper()}] {self.__title}"