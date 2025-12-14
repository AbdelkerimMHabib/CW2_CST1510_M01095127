class Dataset:
    """Represents a data science dataset in the platform."""
    
    def __init__(self, dataset_id: int, name: str, size_bytes: int, rows: int, source: str):
        self.__id = dataset_id
        self.__name = name
        self.__size_bytes = size_bytes
        self.__rows = rows
        self.__source = source
    
    def calculate_size_mb(self) -> float:
        """Convert size from bytes to megabytes."""
        return self.__size_bytes / (1024 * 1024)
    
    def get_id(self) -> int:
        """Get the dataset ID."""
        return self.__id
    
    def get_name(self) -> str:
        """Get the dataset name."""
        return self.__name
    
    def get_size_bytes(self) -> int:
        """Get the dataset size in bytes."""
        return self.__size_bytes
    
    def get_rows(self) -> int:
        """Get the number of rows in the dataset."""
        return self.__rows
    
    def get_source(self) -> str:
        """Get the dataset source."""
        return self.__source
    
    def __str__(self) -> str:
        """String representation of the dataset."""
        size_mb = self.calculate_size_mb()
        return f"Dataset {self.__id}: {self.__name} ({size_mb:.2f} MB, {self.__rows} rows)"