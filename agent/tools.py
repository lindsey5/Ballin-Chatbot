from datetime import datetime
import json
from zoneinfo import ZoneInfo
from langchain.tools import tool
from sqlalchemy import desc, func, literal
from sqlalchemy.orm import joinedload
from config.db import SessionLocal
from models.OrderAddress import OrderAddress
from models.Order import Order
from models.OrderItem import OrderItem
from models.Product import Product
from models.Thumbnail import Thumbnail
from models.Variant import Variant

@tool
def products_tool() -> str:
    """Search products by name, stock, prices from the inventory."""
    db = SessionLocal()
    try:
        products = db.query(Product).filter(Product.status == "Available").options(joinedload(Product.variants), joinedload(Product.thumbnail)).all()

        result = []
        for product in products:
            result.append({
                "product_name": product.product_name,
                "category": product.category,
                "variants": [
                    {
                        "price": v.price,
                        "stock": v.stock,
                        "size": v.size,
                        "color": v.color
                    }
                    for v in product.variants
                ],
                "thumbnail": {
                    "thumbnailUrl": product.thumbnail.thumbnailUrl,
                    "thumbnailPublicId": product.thumbnail.thumbnailPublicId
                } if product.thumbnail else None
            })
        return json.dumps(result, indent=2)
    except Exception as e:
        print(e)
        return json.dumps({"error": str(e)}, indent=2)
    
@tool
def get_top_products(filter: str = "all") -> str:
    """
    Get top selling products with optional date filter.
    filter: "all", "thisMonth", "lastMonth", "thisYear"
    """
    limit = 10
    db = SessionLocal()
    try:
        now = datetime.now(ZoneInfo("Asia/Manila"))
        year = now.year
        month = now.month

        date_conditions = []
        if filter == "thisMonth":
            # Get first day of next month, then subtract 1 second to get end of current month
            if month == 12:
                next_month_start = datetime(year + 1, 1, 1)
            else:
                next_month_start = datetime(year, month + 1, 1)
            
            date_conditions = [
                Order.order_date >= datetime(year, month, 1),
                Order.order_date < next_month_start
            ]
        elif filter == "lastMonth":
            last_month = month - 1 if month > 1 else 12
            last_month_year = year if month > 1 else year - 1
            
            # Get first day of current month for upper bound
            date_conditions = [
                Order.order_date >= datetime(last_month_year, last_month, 1),
                Order.order_date < datetime(year, month, 1)
            ]
        elif filter == "thisYear":
            date_conditions = [
                Order.order_date >= datetime(year, 1, 1),
                Order.order_date < datetime(year + 1, 1, 1)
            ]

        top_products_query = (
            db.query(
                OrderItem.product_id,
                Product,
                func.sum(OrderItem.quantity).label("total_sold")
            )
            .join(Order, Order.order_id == OrderItem.order_id)
            .join(Product, Product.id == OrderItem.product_id)
            .outerjoin(Variant, Variant.product_id == Product.id)
            .outerjoin(Thumbnail, Thumbnail.product_id == Product.id)
            .filter(Order.status.in_(["Delivered", "Received"]))
            .filter(Product.status == "Available")
        )

        for condition in date_conditions:
            top_products_query = top_products_query.filter(condition)

        top_products = (
            top_products_query
            .group_by(OrderItem.product_id, Product.id)  # Include Product.id in GROUP BY
            .order_by(desc("total_sold"))  # Use desc() instead of literal
            .limit(limit)
            .all()
        )
        
        result_str = "\n\n".join([
            f"Product: {row.Product.product_name}\n"
            f"Image: {row.Product.thumbnail.thumbnailUrl if row.Product.thumbnail else 'No image available'}\n"
            f"Quantity Sold: {int(row.total_sold)}"
            for row in top_products
        ])
        return result_str
    except Exception as e:
        print(e)
        return json.dumps({"error": str(e)}, indent=2)
    finally:
        db.close()

@tool
def get_order_details(order_id: str) -> str:
    """
    Get order details by order_id.

    Args:
        order_id: Order ID to retrieve
    """
    db = SessionLocal()
    try:
        # Eager loading (like Sequelize include)
        order = (
            db.query(Order)
            .options(
                joinedload(Order.customer),
                joinedload(Order.order_items)
                    .joinedload(OrderItem.product)
                    .joinedload(Product.thumbnail),  # optional thumbnail
                joinedload(Order.order_address)
            )
            .filter(Order.order_id == order_id)
            .first()
        )

        if not order:
            return f"No order found with ID: {order_id}"

        # Format enums and order date
        status = order.status.value if order.status else "N/A"
        payment_method = order.payment_method.value if order.payment_method else "N/A"
        customer_name = f"{order.customer.firstname} {order.customer.lastname}" if order.customer else "N/A"
        utc_date = order.order_date.replace(tzinfo=ZoneInfo("UTC"))
        manila_date = utc_date.astimezone(ZoneInfo("Asia/Manila"))
        formatted = manila_date.strftime("%B %d, %Y %I:%M %p")
        
        # Summary
        summary = f"""
Order ID: {order.order_id}
Customer ID: {order.customer_id}
Customer Name: {customer_name}
Status: {status}
Payment Method: {payment_method}
Subtotal: ₱{order.subtotal}
Shipping Fee: Free
Total: ₱{order.total}
Order Date: {formatted}
"""

        # Cancellation reason
        cancellation_reason = order.cancellation_reason or "No cancellation reason."

        # Address
        if order.order_address:
            addr = order.order_address
            address = f"""
Shipping Address:
  Name: {addr.fullname}
  {addr.address_line_1}
  {addr.address_line_2}
  {addr.admin_area_2}, {addr.admin_area_1}
  {addr.postal_code}
  Phone: {addr.phone}
"""
        else:
            address = "No shipping address found.\n"

        # Items (always process items, outside of address if/else)
        items_list = []
        if order.order_items:
            for i, item in enumerate(order.order_items, 1):
                product_name = item.product.product_name if item.product else "N/A"
                thumbnail_url = (
                    item.product.thumbnail.thumbnailUrl
                    if item.product and item.product.thumbnail
                    else "No image available"
                )
                item_str = f"""
Item {i}:
- Image: {thumbnail_url}
- Product Name: {product_name}
- Size: {item.size}
- Color: {item.color}
- Price: ₱{item.price}
- Quantity: {item.quantity}
- Total: ₱{item.total}
"""
                items_list.append(item_str)
        items = "\n".join(items_list) if items_list else "No items found for this order."

        return f"Order summary:{summary}\n{address}\nOrder items:\n{items}\nCancellation Reason: {cancellation_reason}\n"

    except Exception as e:
        print(f"Error fetching order details: {e}")
        return "Failed to fetch order details."
    finally:
        db.close()


def getChatbotTools():
    return [products_tool, get_top_products, get_order_details]
