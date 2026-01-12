# 玩具資料瀏覽器

一個基於 Web 的玩具資料查詢工具，可以瀏覽 Excel 中的玩具資訊並在嵌入的瀏覽器中預覽相關網頁。

## 功能特色

- ��讀 Excel 檔案的多個頁籤（如：火影、航海王）
- 顯示每個頁籤中 B 欄的商品資訊
- 點擊眼睛圖示可以在右側預覽相關網頁
- 使用 iframe 嵌入方式，無需跳轉頁面
- 美觀的現代化 UI 設計

## 使用方式

### 方法一：純 HTML 版本（當前版本）

1. 確保前端資料已正確配置在 `index.html` 中

2. 啟動 Python HTTP 伺服器：
```bash
cd frontend
python -m http.server 3000
```

3. 在瀏覽器中打開：http://localhost:3000

### 方法二：使用後端 API（需要配置）

如果要從 Excel 讀取並使用 Google 搜尋，需要啟動後端：

1. 安裝後端依賴：
```bash
cd backend
pip install -r requirements.txt
```

2. 啟動 Flask 後端：
```bash
cd backend
python app.py
```

3. 後端會自動讀取 `list.xlsx` 並透過 Google 搜尋找到相關連結

4. 在瀏覽器中打開：http://localhost:5000

## 檔案結構

```
frontend/
├── index.html          # 主頁面（包含 HTML、CSS、JavaScript）
└── README.md           # 說明文件

backend/
├── app.py              # Flask API 伺服器
├── requirements.txt    # Python 依賴
└── data_cache.json     # 資料快取檔案
```

## UI 說明

- **頂部頁籤**：切換不同的 Excel 頁籤（火影、航海王等）
- **左側列表**：顯示 B 欄的商品名稱
- **眼睛圖示**：點擊後在右側預覽該商品的相關網頁
- **右側區域**：嵌入式瀏覽器顯示網頁內容
- **在新分頁開啟**：在新的瀏覽器分頁中開啟網頁
- **重新載入按鈕**：重新載入資料（會清除快取並重新搜尋）

## 注意事項

- Google 搜尋可能會被限制，建議使用快取檔案
- 某些網站可能不允許在 iframe 中顯示
- 搜尋過程可能需要較長時間（每個項目約 2 秒）

## 技術棧

- **前端**：純 HTML + CSS + JavaScript（無需編譯）
- **後端**：Python + Flask + pandas + BeautifulSoup
- **樣式**：現代化 CSS，帶動畫效果

## 開發說明

如需修改資料，有兩種方式：

1. **直接修改 frontend/index.html**：在 `loadData()` 函數中修改 `testData`
2. **使用後端 API**：修改 `backend/data_cache.json` 或重新從 Excel 載入
