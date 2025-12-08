from typing import List, Dict, Optional
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident
from models.dataset import Dataset
from models.it_ticket import ITTicket

class DataService:
    def __init__(self, db_manager: DatabaseManager):
        self._db = db_manager
    
    def get_all_incidents(self) -> List[SecurityIncident]:
        rows = self._db.fetch_all("SELECT * FROM cyber_incidents ORDER BY id DESC")
        incidents = []
        for row in rows:
            incidents.append(SecurityIncident(
                incident_id=row['id'],
                title=row['title'],
                severity=row['severity'],
                status=row['status'],
                date=row['date']
            ))
        return incidents
    
    def get_incident_by_id(self, incident_id: int) -> Optional[SecurityIncident]:
        row = self._db.fetch_one("SELECT * FROM cyber_incidents WHERE id = ?", (incident_id,))
        if row:
            return SecurityIncident(
                incident_id=row['id'],
                title=row['title'],
                severity=row['severity'],
                status=row['status'],
                date=row['date']
            )
        return None
    
    def add_incident(self, title: str, severity: str, status: str, date: str) -> bool:
        try:
            self._db.execute_query(
                "INSERT INTO cyber_incidents (title, severity, status, date) VALUES (?, ?, ?, ?)",
                (title, severity, status, date)
            )
            return True
        except Exception:
            return False
    
    def get_all_datasets(self) -> List[Dataset]:
        rows = self._db.fetch_all("SELECT * FROM datasets_metadata ORDER BY id DESC")
        datasets = []
        for row in rows:
            datasets.append(Dataset(
                dataset_id=row['id'],
                name=row['name'],
                source=row['source'],
                category=row['category'],
                size_mb=row['size']
            ))
        return datasets
    
    def add_dataset(self, name: str, source: str, category: str, size: int) -> bool:
        try:
            self._db.execute_query(
                "INSERT INTO datasets_metadata (name, source, category, size) VALUES (?, ?, ?, ?)",
                (name, source, category, size)
            )
            return True
        except Exception:
            return False
    
    def get_all_tickets(self) -> List[ITTicket]:
        rows = self._db.fetch_all("SELECT * FROM it_tickets ORDER BY id DESC")
        tickets = []
        for row in rows:
            tickets.append(ITTicket(
                ticket_id=row['id'],
                title=row['title'],
                priority=row['priority'],
                status=row['status'],
                created_date=row['created_date']
            ))
        return tickets
    
    def add_ticket(self, title: str, priority: str, status: str, created_date: str) -> bool:
        try:
            self._db.execute_query(
                "INSERT INTO it_tickets (title, priority, status, created_date) VALUES (?, ?, ?, ?)",
                (title, priority, status, created_date)
            )
            return True
        except Exception:
            return False
    
    def get_statistics(self) -> Dict:
        return {
            "incidents": {
                "total": self._db.get_table_count("cyber_incidents"),
                "open": len(self._db.fetch_all(
                    "SELECT id FROM cyber_incidents WHERE status IN ('open', 'in progress')"
                ))
            },
            "datasets": {
                "total": self._db.get_table_count("datasets_metadata"),
                "total_size": self._get_total_dataset_size()
            },
            "tickets": {
                "total": self._db.get_table_count("it_tickets"),
                "open": len(self._db.fetch_all(
                    "SELECT id FROM it_tickets WHERE status IN ('open', 'in progress')"
                ))
            },
            "users": {
                "total": self._db.get_table_count("users")
            }
        }
    
    def _get_total_dataset_size(self) -> int:
        result = self._db.fetch_one("SELECT SUM(size) as total FROM datasets_metadata")
        return result['total'] if result and result['total'] else 0