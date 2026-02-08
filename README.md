
# 🍽️ Restaurant Orders — End-to-End Data Analysis Project

## Project Overview

This project analyzes a quarter’s worth of transactional order data from a fictitious restaurant serving international cuisine. The goal is to understand **customer ordering behavior**, **revenue drivers**, and **time-based demand patterns**, and to translate those insights into **actionable menu and operational recommendations**.

The analysis follows a **full data analytics lifecycle**:

* raw data inspection and validation
* data cleaning and feature engineering
* exploratory analysis
* business insight generation
* reproducible scripting and visualization

All analysis is fully reproducible using Python scripts.

---

## Business Questions

This project answers the following questions:

1. What are the **most and least ordered menu items**, and which cuisines do they belong to?
2. What do the **highest spend orders** look like?

   * Are they driven by quantity or premium pricing?
3. How does **order volume and revenue vary by time of day and day of week**?
4. Which **cuisines should be expanded, optimized, or re-evaluated** based on demand and revenue efficiency?

---

## Dataset Description

### `menu_items.csv`

Menu reference table containing:

* `menu_item_id`
* `item_name`
* `category` (cuisine)
* `price`

Each row represents one unique menu item.

### `order_details.csv`

Transactional table containing:

* `order_details_id`
* `order_id`
* `order_date`
* `order_time`
* `item_id`

Each row represents **one item within an order** (orders may contain multiple rows).

---

## Data Validation & Cleaning

Key validation steps:

* Verified schema consistency and data types
* Confirmed all non-null `item_id`s in orders map to menu items
* Identified and inspected rows with missing `item_id`
* Found ~1% of rows missing item identifiers and removed them (documented decision)

Feature engineering:

* Combined date and time into `order_datetime`
* Derived:

  * `order_hour`
  * `order_weekday`

The result is a clean, analysis-ready dataset where:

* every row maps to a menu item
* every row has a valid price
* all time-based analyses are reliable

---

## Analysis Summary

### 1️. Item Popularity

* A small subset of menu items drives a large share of demand
* American and Asian dishes dominate the most-ordered items
* Least-ordered items are still ordered hundreds of times, suggesting no completely “dead” items

 **Plot:** `figures/top10_items.png`

---

### 2️. Order Value & Basket Behavior

* High-spend orders are **not driven by premium pricing**
* Instead, they are driven by **large basket sizes** (13–14 items per order)
* High-value orders tend to include:

  * multiple cuisines
  * repeated mid-priced items
  * side dishes that expand basket size

 **Plots:**

* `figures/order_spend_distribution.png`
* `figures/avg_order_value_by_hour.png`

---

### 3️. Time-Based Demand Patterns

* Two clear daily peaks:

  * **Lunch:** 12–1 PM
  * **Dinner:** 5–6 PM
* Lunch hours generate:

  * highest order volume
  * highest revenue
  * highest average order value
* High-spend (top 5%) orders cluster overwhelmingly during lunch

Demand is consistent across weekdays, not concentrated only on weekends.

 **Plots:**

* `figures/orders_by_hour.png`
* `figures/avg_order_value_by_hour.png`

---

### 4. Cuisine Strategy Insights

Cuisine performance was evaluated using:

* total orders
* total revenue
* menu depth
* revenue per menu item

Key findings:

* **Asian cuisine**

  * highest demand
  * highest revenue efficiency
  * relatively limited menu depth
* **Italian cuisine**

  * highest total revenue
  * higher average price
  * strong presence in group orders
* **American cuisine**

  * small menu
  * strong volume and consistency
* **Mexican cuisine**

  * solid demand
  * lower revenue efficiency
  * already broad menu

 **Plot:** `figures/revenue_by_cuisine.png`

---

## Recommendations

###  Expand

**Asian cuisine**

* High demand and efficiency
* Opportunity to introduce additional lunch-friendly items or shareables

### 🔧 Optimize

**Italian cuisine**

* Focus on bundles or group-oriented offerings
* Leverage premium positioning rather than adding many new items

### Maintain

**American cuisine**

* Reliable volume drivers
* Consider limited-time offers rather than permanent expansion

###  Re-evaluate

**Mexican cuisine**

* Review pricing, portions, or differentiation before adding new items

---

## Visual Summary

This project includes five key visualizations:

1. Top 10 items by order count
2. Orders by hour of day
3. Average order value by hour
4. Distribution of order spend
5. Revenue by cuisine

All figures are saved in the `figures/` directory with captions provided in `figures/CAPTIONS.md`.

---

## Reproducibility

### Requirements

* Python 3.9+
* pandas
* numpy
* matplotlib

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Analysis

From the project root:

```bash
python -m src.analysis --data_dir data --output_dir outputs --fig_dir figures
```

This will:

* clean and merge the data
* generate analysis CSVs in `outputs/`
* generate plots in `figures/`

---

## Project Structure

```
restaurant-orders/
├── data/
│   ├── menu_items.csv
│   └── order_details.csv
├── src/
│   ├── analysis.py
│   ├── data_utils.py
│   └── plots.py
├── outputs/
├── figures/
│   └── CAPTIONS.md
├── requirements.txt
└── README.md
```

---
---

## Notes

This dataset is fictitious and used solely for analytical demonstration. Results and recommendations are illustrative and intended to showcase analytical thinking and methodology.

---
