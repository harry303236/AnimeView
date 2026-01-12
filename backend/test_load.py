# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from app import load_excel_data
import json

print("Testing load_excel_data...")
data = load_excel_data()

print(f"\n=== Results ===")
print(f"Total sheets: {len(data)}")
for sheet_name, items in data.items():
    print(f"\n{sheet_name}: {len(items)} items")
    if items:
        print(f"  First item: {items[0]}")
