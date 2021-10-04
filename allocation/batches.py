#  Direitos Autorais (c) 2021 Edson César.
#
#  Proibida a cópia parcial ou total de qualquer dos arquivos de código fonte
#  deste projeto. Proibido o uso comercial ou com finalidades lucrativas em
#  qualquer hipótese. Esta licença está baseada em estudos sobre a Lei
#  Brasileira de Direitos Autorais (Lei 9.610/1998) e Tratados Internacionais
#  sobre Propriedade Intelectual.

#
from dataclasses import dataclass
from datetime import date
from typing import List
from typing import Optional
from typing import Set


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int


class OutOfStock(Exception):
    pass


class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.quantity = qty
        self._allocations: Set[OrderLine] = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line not in self._allocations:
            return
        self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self.quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    def __lt__(self, other):
        if self.eta is None:
            return True  # False?
        if other.eta is None:
            return False
        return self.eta < other.eta

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)


def allocate(line: OrderLine, batches: List[Batch]):
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')
