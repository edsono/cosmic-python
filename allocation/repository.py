from typing import List
from typing import Protocol

from .batches import Batch


class BatchRepository(Protocol):
    def add(self, batch: Batch):
        """to put a new item in the repository"""

    def get(self, reference) -> Batch:
        """to get a item from the repository"""


# class FakeRepository:
#     def __init__(self, batches: List[Batch]):
#         self._batches = set(batches)
#
#     def add(self, batch: Batch):
#         self._batches.add(batch)
#
#     def get(self, reference) -> Batch:
#         return next(b for b in self._batches if b.reference == reference)
#
#     def list(self) -> List[Batch]:
#         return list(self._batches)
#

class SqlAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def add(self, batch: Batch):
        self.session.add(batch)

    def get(self, reference) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> List[Batch]:
        return self.session.query(Batch).all()
