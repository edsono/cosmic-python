from datetime import date
from datetime import timedelta

import pytest

from allocation.domain import models

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = models.Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = models.Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = models.OrderLine("oref", "RETRO-CLOCK", 10)
    models.allocate(line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = models.Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = models.Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = models.Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = models.OrderLine("order1", "MINIMALIST-SPOON", 10)
    models.allocate(line, [medium, earliest, latest])
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = models.Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100,
                                  eta=None)
    shipment_batch = models.Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100,
                                  eta=tomorrow)
    line = models.OrderLine("oref", "HIGHBROW-POSTER", 10)
    allocation = models.allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = models.Batch('batch1', 'SMALL-FORK', 10, eta=today)
    models.allocate(models.OrderLine('order1', 'SMALL-FORK', 10), [batch])
    with pytest.raises(models.OutOfStock, match='SMALL-FORK'):
        models.allocate(models.OrderLine('order2', 'SMALL-FORK', 1), [batch])
