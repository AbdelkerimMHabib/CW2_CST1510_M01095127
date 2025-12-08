class Dataset:
    """Represents a data science dataset in the platform."""
    
    def __init__(self, dataset_id: int, name: str, source: str, category: str, size_mb: int):
        self.__id = dataset_id
        self.__name = name
        self.__source = source
        self.__category = category
        self.__size_mb = size_mb
    
    def get_id(self) -> int:
        return self.__id
    
    def get_name(self) -> str:
        return self.__name
    
    def get_source(self) -> str:
        return self.__source
    
    def get_category(self) -> str:
        return self.__category
    
    def get_size_mb(self) -> int:
        return self.__size_mb
    
    def get_size_gb(self) -> float:
        return self.__size_mb / 1024.0
    
    def get_size_formatted(self) -> str:
        if self.__size_mb >= 1024:
            return f"{self.get_size_gb():.1f} GB"
        return f"{self.__size_mb} MB"
    
    def is_large_dataset(self) -> bool:
        return self.__size_mb > 500
    
    def __str__(self) -> str:
        return f"Dataset(id={self.__id}, name='{self.__name}', category={self.__category}, size={self.get_size_formatted()})"