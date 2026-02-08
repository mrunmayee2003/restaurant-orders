from pathlib import Path
import pandas as pd

def load_menu(menu_path):
    menu_path = Path(menu_path)
    if not menu_path.exists():
        raise FileNotFoundError(menu_path)

    menu = pd.read_csv(menu_path)
    menu.columns = [c.strip() for c in menu.columns]

    expected = {'menu_item_id', 'item_name', 'category', 'price'}
    if not expected.issubset(menu.columns):
        raise ValueError(f"Menu missing columns: {expected}")

    menu['menu_item_id'] = pd.to_numeric(menu['menu_item_id'], errors='coerce').astype('Int64')
    menu['price'] = pd.to_numeric(menu['price'], errors='coerce')

    return menu


def load_orders(order_path):
    order_path = Path(order_path)
    if not order_path.exists():
        raise FileNotFoundError(order_path)

    orders = pd.read_csv(order_path)
    orders.columns = [c.strip() for c in orders.columns]

    expected = {'order_details_id', 'order_id', 'order_date', 'order_time', 'item_id'}
    if not expected.issubset(orders.columns):
        raise ValueError(f"Orders missing columns: {expected}")

    orders['order_details_id'] = pd.to_numeric(orders['order_details_id'], errors='coerce').astype('Int64')
    orders['order_id'] = pd.to_numeric(orders['order_id'], errors='coerce').astype('Int64')
    orders['item_id'] = pd.to_numeric(orders['item_id'], errors='coerce').astype('Int64')

    # Explicit datetime parsing
    orders['order_datetime'] = pd.to_datetime(
        orders['order_date'].astype(str) + ' ' + orders['order_time'].astype(str),
        format='%m/%d/%y %I:%M:%S %p',
        errors='coerce'
    )

    orders['order_date'] = pd.to_datetime(
        orders['order_date'],
        format='%m/%d/%y',
        errors='coerce'
    ).dt.date

    orders['order_hour'] = orders['order_datetime'].dt.hour
    orders['order_weekday'] = orders['order_datetime'].dt.day_name()

    return orders


def build_cleaned_orders(orders_path, menu_path):
    menu = load_menu(menu_path)
    orders = load_orders(orders_path)

    # Drop rows with missing item_id (documented decision)
    orders = orders.dropna(subset=['item_id']).copy()

    merged = orders.merge(
        menu,
        left_on='item_id',
        right_on='menu_item_id',
        how='left',
        indicator=True
    )

    unmatched = (merged['_merge'] != 'both').sum()
    if unmatched:
        print(f"Warning: {unmatched} order rows did not match menu items")

    merged['price'] = pd.to_numeric(merged['price'], errors='coerce')

    return merged
