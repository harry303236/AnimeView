# -*- coding: utf-8 -*-
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import pandas as pd
import os
import json
import sys
import io
import re
import urllib.parse

# 設定編碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)

# 設定路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "..", "list.xlsx")
CACHE_FILE = os.path.join(BASE_DIR, "data_cache.json")

def load_excel_data():
    """讀取 Excel 檔案並返回結構化資料（不含 URL）"""
    try:
        # 檢查快取
        if os.path.exists(CACHE_FILE):
            print("Loading from cache...")
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print("Reading Excel file...")
        print(f"Excel path: {EXCEL_FILE}")
        print(f"File exists: {os.path.exists(EXCEL_FILE)}")
        
        if not os.path.exists(EXCEL_FILE):
            print(f"Error: Excel file not found: {EXCEL_FILE}")
            return {}
        
        excel_file = pd.ExcelFile(EXCEL_FILE)
        data = {}
        
        for sheet_name in excel_file.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            if len(df.columns) < 2:
                print(f"  Sheet has less than 2 columns, skipping")
                continue
            
            # 取得 B 欄資料（索引 1）
            b_column = df.iloc[:, 1]
            
            items = []
            for idx, value in enumerate(b_column):
                if pd.notna(value) and str(value).strip():
                    name = str(value).strip()
                    # 只儲存名稱，不生成 URL
                    items.append({'name': name})
                    print(f"  [{idx+1}] {name[:50]}...")
            
            data[sheet_name] = items
            print(f"  Total items: {len(items)}")
        
        # 儲存快取
        print("Saving cache...")
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Data loaded successfully! Total sheets: {len(data)}")
        return data
        
    except Exception as e:
        print(f"Error loading Excel: {str(e)}")
        import traceback
        traceback.print_exc()
        return {}

def extract_keywords(text):
    """從商品名稱提取關鍵詞"""
    # 移除括號內容（通常是數量、規格等）
    text = re.sub(r'[（(【\[].*?[）)\]】]', '', text)
    
    # 移除常見的無用詞
    remove_words = ['盲盒', '再版', '再贩', '普通扭蛋', '手办', '比例手办', 
                   '一般品', '谷子', '限定', '套装', '系列']
    for word in remove_words:
        text = text.replace(word, '')
    
    # 移除多餘空格和特殊字符
    text = re.sub(r'[/\-~～·]', ' ', text)
    text = ' '.join(text.split())
    
    # 只取前面的關鍵部分（通常是系列名+角色名）
    parts = text.split()
    if len(parts) > 5:
        text = ' '.join(parts[:5])
    
    return text.strip()

def generate_search_url(query):
    """為查詢生成 Bing 圖片搜尋 URL"""
    # 提取關鍵詞
    keywords = extract_keywords(query)
    
    # 如果提取後太短，使用原始查詢的前半部分
    if len(keywords) < 3:
        keywords = query[:min(20, len(query))]
    
    # 加上"手辦"或"figure"關鍵字以提高搜尋準確度
    search_query = f"{keywords} 手辦 figure"
    encoded_query = urllib.parse.quote(search_query)
    
    # 使用 Bing 圖片搜尋（無 CAPTCHA 問題，更易瀏覽）
    return f"https://www.bing.com/images/search?q={encoded_query}"

@app.route('/api/data')
def get_data():
    """返回所有資料（不含 URL，快速載入）"""
    data = load_excel_data()
    return jsonify(data)

@app.route('/api/search')
def search_item():
    """為單個項目生成搜尋 URL"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    
    try:
        # 生成搜尋 URL
        search_url = generate_search_url(query)
        keywords = extract_keywords(query)
        
        return jsonify({
            'url': search_url,
            'keywords': keywords,
            'original': query
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh')
def refresh_data():
    """清除快取並重新載入資料"""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print("Cache cleared")
    data = load_excel_data()
    return jsonify(data)

@app.route('/')
def serve_frontend():
    """提供前端頁面"""
    return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    print("=" * 60)
    print("Starting server...")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
