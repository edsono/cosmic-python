from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.ext.instrumentation import InstrumentationManager
from sqlalchemy.orm import mapper
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

from allocation.domain import models

mapper_registry = registry()
metadata = mapper_registry.metadata

DEL_ATTR = object()


# https://github.com/cosmicpython/code/issues/17
class FrozenDataclassInstrumentationManager(InstrumentationManager):
    # noinspection PyAttributeOutsideInit
    def manage(self, class_, manager):
        self.originals = {}
        setattr(class_, "_sa_class_manager", manager)

    # noinspection PyUnusedLocal
    def unregister(self, class_, manager):
        del self.originals
        delattr(class_, "_sa_class_manager")

    def dispose(self, class_, **kwargs):
        del self.originals
        delattr(class_, "_sa_class_manager")

    def manager_getter(self, class_):
        def get(cls):
            return cls.__dict__["_sa_class_manager"]

        return get

    def install_member(self, class_, key, implementation):
        self.originals.setdefault(key, class_.__dict__.get(key, DEL_ATTR))
        setattr(class_, key, implementation)

    def uninstall_member(self, class_, key):
        original = self.originals.pop(key, None)
        if original is not DEL_ATTR:
            setattr(class_, key, original)
        else:
            delattr(class_, key)

    def get_instance_dict(self, class_, instance):
        return instance.__dict__

    def install_state(self, class_, instance, state):
        instance.__dict__["state"] = state

    def remove_state(self, class_, instance):
        del instance.__dict__["state"]

    def state_getter(self, class_):
        def find(instance):
            return instance.__dict__["state"]

        return find


# noinspection Mypy
models.OrderLine.__sa_instrumentation_manager__ = FrozenDataclassInstrumentationManager  # type: ignore

order_lines = Table(
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('order_id', String(255)),
)

batches = Table(
    "batches", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    lines_mapper = mapper_registry.map_imperatively(models.OrderLine, order_lines)
    mapper(
        models.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper, secondary=allocations, collection_class=set,
            )
        },
    )
