from allocation import Batch
from allocation import OrderLine
from allocation import repository


def test_repository_can_save_a_batch(session):
    batch = Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)
    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()
    # noinspection SqlNoDataSourceInspection
    rows = list(session.execute(
        "SELECT reference, sku, _purchased_quantity, eta FROM batches"
    ))
    assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]


def insert_order_line(session):
    # noinspection SqlNoDataSourceInspection
    session.execute(
        "INSERT INTO order_lines (order_id, sku, qty)"
        " VALUES ('order1', 'GENERIC-SOFA', 12)"
    )
    # noinspection SqlNoDataSourceInspection
    [[orderline_id]] = session.execute(
        "SELECT id FROM order_lines WHERE order_id=:order_id AND sku=:sku",
        dict(order_id="order1", sku="GENERIC-SOFA")
    )
    return orderline_id


def insert_batch(session, batch_id):
    # noinspection SqlNoDataSourceInspection
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        " VALUES (:batch_id, 'GENERIC-SOFA', 100, NULL)",
        dict(batch_id=batch_id),
    )
    # noinspection SqlNoDataSourceInspection
    [[batch_id]] = session.execute(
        "SELECT id FROM batches WHERE reference=:batch_id AND sku='GENERIC-SOFA'",
        dict(batch_id=batch_id),
    )
    return batch_id


def insert_allocation(session, orderline_id, batch_id):
    # noinspection SqlNoDataSourceInspection
    session.execute(
        "INSERT INTO allocations (orderline_id, batch_id)"
        " VALUES (:orderline_id, :batch_id)",
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )


def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)
    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")
    expected = Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected  # Batch.__eq__ only compares reference
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        OrderLine("order1", "GENERIC-SOFA", 12),
    }
