import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .data_utils import build_cleaned_orders
from .plots import (
    plot_top_items,
    plot_orders_by_hour,
    plot_avg_order_value_by_hour,
    plot_order_spend_distribution,
    plot_revenue_by_cuisine
)

def item_popularity(df, out_dir):
    counts = (df.groupby(['item_name','category'])
                .size()
                .reset_index(name='order_count')
                .sort_values('order_count', ascending=False))
    counts.to_csv(out_dir/'item_counts.csv', index=False)
    # simple bar for top 10
    top10 = counts.head(10)
    fig, ax = plt.subplots(figsize=(8,5))
    ax.barh(top10['item_name'][::-1], top10['order_count'][::-1])
    ax.set_xlabel('Order count')
    ax.set_title('Top 10 items by order count')
    fig.tight_layout()
    fig.savefig(out_dir.parent/'figures'/'top10_items.png')
    plt.close(fig)
    return counts

def order_level_summary(df, out_dir):
    order_summary = (df.groupby('order_id')
                       .agg(total_spend=('price','sum'),
                            item_count=('item_id','count'),
                            avg_item_price=('price','mean'))
                       .reset_index()
                       .sort_values('total_spend', ascending=False))
    order_summary.to_csv(out_dir/'order_totals.csv', index=False)
    return order_summary

def hourly_analysis(df, out_dir):
    hourly = (df.groupby('order_hour')
                .agg(unique_orders=('order_id','nunique'),
                     total_revenue=('price','sum'))
                .reset_index()
                .sort_values('order_hour'))
    hourly.to_csv(out_dir/'orders_by_hour.csv', index=False)
    # plot
    fig, ax = plt.subplots(figsize=(9,4))
    ax.plot(hourly['order_hour'], hourly['unique_orders'], marker='o')
    ax.set_xlabel('Hour of day')
    ax.set_ylabel('Unique orders')
    ax.set_title('Orders by hour')
    fig.tight_layout()
    fig.savefig(out_dir.parent/'figures'/'orders_by_hour.png')
    plt.close(fig)
    return hourly

def cuisine_summary(df, out_dir):
    cs = (df.groupby('category')
          .agg(total_items_ordered=('item_id','count'),
               unique_orders=('order_id','nunique'),
               total_revenue=('price','sum'),
               avg_item_price=('price','mean'),
               menu_items=('item_id','nunique'))
          .reset_index())
    cs['orders_per_item'] = cs['total_items_ordered'] / cs['menu_items']
    cs['revenue_per_item'] = cs['total_revenue'] / cs['menu_items']
    cs.to_csv(out_dir/'cuisine_summary.csv', index=False)
    return cs

def high_spend_by_hour(df, out_dir):
    order_summary = (df.groupby(['order_id','order_hour'])
                       .agg(total_spend=('price','sum'))
                       .reset_index())
    threshold = order_summary['total_spend'].quantile(0.95)
    high = order_summary[order_summary['total_spend'] >= threshold]
    hourly_high = (high.groupby('order_hour')
                        .agg(high_value_orders=('order_id','count'),
                             avg_high_order_value=('total_spend','mean'))
                        .reset_index()
                        .sort_values('order_hour'))
    hourly_high.to_csv(out_dir/'high_spend_by_hour.csv', index=False)
    return hourly_high

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--data_dir', default='data')
    p.add_argument('--output_dir', default='outputs')
    p.add_argument('--fig_dir', default='figures')
    return p.parse_args()

def main():
    args = parse_args()
    data_dir = Path(args.data_dir)
    out_dir = Path(args.output_dir)
    fig_dir = Path(args.fig_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    df = build_cleaned_orders(data_dir/'order_details.csv', data_dir/'menu_items.csv')
    # also save the cleaned table
    df.to_csv(out_dir/'orders_cleaned_from_script.csv', index=False)

    # --- Generate plots ---
    plot_top_items(df, fig_dir / 'top10_items.png')
    plot_orders_by_hour(df, fig_dir / 'orders_by_hour.png')

    order_summary = (
        df.groupby(['order_id', 'order_hour'])
        .agg(total_spend=('price', 'sum'))
        .reset_index()
    )

    plot_avg_order_value_by_hour(order_summary, fig_dir / 'avg_order_value_by_hour.png')
    plot_order_spend_distribution(order_summary, fig_dir / 'order_spend_distribution.png')
    plot_revenue_by_cuisine(df, fig_dir / 'revenue_by_cuisine.png')


    print("Running item popularity...")
    item_popularity(df, out_dir)

    print("Running order-level summary...")
    order_level_summary(df, out_dir)

    print("Running hourly analysis...")
    hourly_analysis(df, out_dir)

    print("Running cuisine summary...")
    cuisine_summary(df, out_dir)

    print("Running high-spend by hour analysis...")
    high_spend_by_hour(df, out_dir)

    print("All done. CSV outputs are in", out_dir.resolve())
    print("Figures are in", fig_dir.resolve())

if __name__ == '__main__':
    main()
