# Restaurant Orders - Script-based EDA

Run Python scripts from the command line or VS Code. Place CSVs in `data/`:
- menu_items.csv: menu_item_id, item_name, category, price
- order_details.csv: order_details_id, order_id, order_date, order_time, item_id

Main script:
- `python src/analysis.py --data_dir data --output_dir outputs --fig_dir figures`

Requirements:
- Create and activate a virtual environment
- `pip install -r requirements.txt`

Outputs:
- CSV summary tables in `outputs/`
- Figures in `figures/`
