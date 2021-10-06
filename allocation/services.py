from typing import Protocol

from domain import model


class BatchRepository(Protocol):
    def add(self, batch: model.Batch):
        """to put a new item in the repository"""

    def get(self, reference) -> model.Batch:
        """to get a item from the repository"""
