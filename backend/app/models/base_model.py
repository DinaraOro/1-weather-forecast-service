from abc import ABC
from abc import abstractmethod


class BaseWeatherModel(ABC):

    @abstractmethod
    def train(self, df):
        pass

    @abstractmethod
    def predict(self, df):
        pass

    @abstractmethod
    def evaluate(self, df):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass