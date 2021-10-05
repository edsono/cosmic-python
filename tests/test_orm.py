import allocation


def test_orderline_mapper_can_load_lines(session):
    # noinspection SqlNoDataSourceInspection
    session.execute("""
        INSERT INTO order_lines (order_id, sku, qty) VALUES
        ('order1', 'RED-CHAIR', 12),
        ('order1', 'RED-TABLE', 13),
        ('order2', 'BLUE-LIPSTICK', 14)
        """)

    expected = [
        allocation.OrderLine("order1", "RED-CHAIR", 12),
        allocation.OrderLine("order1", "RED-TABLE", 13),
        allocation.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(allocation.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = allocation.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()
    # noinspection SqlNoDataSourceInspection
    rows = list(session.execute('SELECT order_id, sku, qty FROM "order_lines"'))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]
