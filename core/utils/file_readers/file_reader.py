from abc import ABC, abstractmethod


class FileReader(ABC):
    @abstractmethod
    def read(self, file_path: str) -> list[dict]:
        raise NotImplementedError('This method must be implemented')
