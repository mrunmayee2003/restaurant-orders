from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def save_fig(fig, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)

def plot_top_items(df, fig_path, top_n=10):
    """
    Horizontal bar chart of top N items by order count.
    df: cleaned orders DataFrame
    """
    counts = (df.groupby(['item_name'])
                .size()
                .reset_index(name='order_count')
                .sort_values('order_count', ascending=False)
                .head(top_n))
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(counts['item_name'][::-1], counts['order_count'][::-1])
    ax.set_xlabel('Order count')
    ax.set_title(f'Top {top_n} items by order count')
    save_fig(fig, fig_path)
    return counts

def plot_orders_by_hour(df, fig_path):
    """
    Line plot: unique orders by hour (0-23)
    """
    hourly = (df.groupby('order_hour')
                .agg(unique_orders=('order_id', 'nunique'))
                .reset_index()
                .sort_values('order_hour'))
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(hourly['order_hour'], hourly['unique_orders'], marker='o')
    ax.set_xlabel('Hour of day')
    ax.set_ylabel('Unique orders')
    ax.set_title('Orders by hour')
    ax.set_xticks(np.arange(0,24))
    save_fig(fig, fig_path)
    return hourly

def plot_avg_order_value_by_hour(order_summary_df, fig_path):
    """
    Line plot: average order value by hour.
    order_summary_df: DataFrame with columns ['order_id','order_hour','total_spend']
    """
    aov = (order_summary_df.groupby('order_hour')
                           .agg(avg_order_value=('total_spend', 'mean'),
                                order_count=('order_id', 'count'))
                           .reset_index()
                           .sort_values('order_hour'))
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(aov['order_hour'], aov['avg_order_value'], marker='o')
    ax.set_xlabel('Hour of day')
    ax.set_ylabel('Average order value ($)')
    ax.set_title('Average order value by hour')
    ax.set_xticks(np.arange(0,24))
    save_fig(fig, fig_path)
    return aov

def plot_order_spend_distribution(order_summary_df, fig_path):
    """
    Histogram of order total spend.
    """
    spends = order_summary_df['total_spend'].dropna()
    fig, ax = plt.subplots(figsize=(8,4))
    ax.hist(spends, bins=40)
    ax.set_xlabel('Order total ($)')
    ax.set_ylabel('Number of orders')
    ax.set_title('Distribution of order spend')
    save_fig(fig, fig_path)
    return spends.describe()

def plot_revenue_by_cuisine(df, fig_path):
    """
    Bar chart of total revenue by cuisine category.
    """
    cs = (df.groupby('category')
            .agg(total_revenue=('price','sum'))
            .reset_index()
            .sort_values('total_revenue', ascending=False))
    fig, ax = plt.subplots(figsize=(8,5))
    ax.bar(cs['category'], cs['total_revenue'])
    ax.set_xlabel('Cuisine category')
    ax.set_ylabel('Total revenue ($)')
    ax.set_title('Revenue by cuisine')
    save_fig(fig, fig_path)
    return cs
