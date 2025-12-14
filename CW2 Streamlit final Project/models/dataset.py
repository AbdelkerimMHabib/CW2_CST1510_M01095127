"""Dataset entity class"""

class Dataset:
    """Represents a data science dataset in the platform."""
    
    def __init__(self, dataset_id: int, name: str, source: str, 
                 category: str, size: int):
        self.__id = dataset_id
        self.__name = name
        self.__source = source
        self.__category = category
        self.__size = size
    
    #Getters
    def get_id(self) -> int:
        """Returns the dataset ID"""
        return self.__id
    
    def get_name(self) -> str:
        """Returns the dataset name"""
        return self.__name
    
    def get_source(self) -> str:
        """Returns the dataset source"""
        return self.__source
    
    def get_category(self) -> str:
        """Returns the dataset category"""
        return self.__category
    
    def get_size(self) -> int:
        """Returns the dataset size in MB"""
        return self.__size
    
    #Utility methods

    def calculate_size_mb(self) -> float:
        """Return dataset size in MB as float"""
        return self.__size
    
    def __str__(self) -> str:
        """Returns string representation of the dataset"""
        return f"Dataset {self.__id}: {self.__name} ({self.__size} MB, source={self.__source})"