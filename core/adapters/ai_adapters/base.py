from abc import ABC, abstractmethod


class AIAgentAdapter(ABC):
    @abstractmethod
    def answer(self, prompt: str) -> str:
        raise NotImplementedError('Subclasses must implement this method')
