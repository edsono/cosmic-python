# Allocations

## Problem Domain

**Product** - A product is identified by a SKU, pronounced “skew,” which is short for
stock-keeping unit.

**Order** - An order is identified by an order reference and comprises multiple order
lines

**Order Line** - An order line has a SKU and a quantity. For example:

* 10 units of RED-CHAIR
* 1 unit of TASTELESS-LAMP

**Batch** - A batch of stock has a unique ID called a reference, a SKU, and a quantity.

## User stories

* As a Customer, I want to place orders so that I can buy products that I want.

* As a purchasing department's worker, I want to order small batches of stock.

## Constraints

* The system must allocate order lines to batches.
    - When we’ve allocated an order line to a batch, we will send stock from that
      specific batch to the customer’s delivery address.
    - When we allocate x units of stock to a batch, the available quantity is reduced by
      x. For example:
        * We have a batch of 20 SMALL-TABLE, and we allocate an order line for 2
          SMALL-TABLE.
        * The batch should have 18 SMALL-TABLE remaining.

* The system must not allocate to a batch if the available quantity is less than the
  quantity of the order line. For example:
    - We have a batch of 1 BLUE-CUSHION, and an order line for 2 BLUE-CUSHION.
    - We should not be able to allocate the line to the batch.

* The system must not allocate the same line twice. For example:
    - We have a batch of 10 BLUE-VASE, and we allocate an order line for 2 BLUE-VASE.
    - If we allocate the order line again to the same batch, the batch should still have
      an available quantity of 8.

* The system must allocate to warehouse stock in preference to shipment batches.

* The system must allocate to shipment batches in order of which has the earliest ETA.

* Batches have an ETA if they are currently shipping, or they may be in warehouse stock.
