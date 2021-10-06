from typing import List

from allocation.domain import models


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

    def add(self, batch: models.Batch):
        self.session.add(batch)

    def get(self, reference) -> models.Batch:
        return self.session.query(models.Batch).filter_by(reference=reference).one()

    def list(self) -> List[models.Batch]:
        return self.session.query(models.Batch).all()
