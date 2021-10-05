#  Direitos Autorais (c) 2021 Edson César.
#
#  Proibida a cópia parcial ou total de qualquer dos arquivos de código fonte
#  deste projeto. Proibido o uso comercial ou com finalidades lucrativas em
#  qualquer hipótese. Esta licença está baseada em estudos sobre a Lei
#  Brasileira de Direitos Autorais (Lei 9.610/1998) e Tratados Internacionais
#  sobre Propriedade Intelectual.
#

#
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
