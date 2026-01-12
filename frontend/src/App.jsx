import React, { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('火影')
  const [selectedItem, setSelectedItem] = useState(null)
  const [data, setData] = useState({})

  useEffect(() => {
    // 載入資料
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const response = await fetch('/data.json')
      const jsonData = await response.json()
      setData(jsonData)
      
      // 設定預設選中第一個項目
      if (jsonData[activeTab] && jsonData[activeTab].length > 0) {
        setSelectedItem(jsonData[activeTab][0])
      }
    } catch (error) {
      console.error('載入資料失敗:', error)
      // 使用範例資料
      const sampleData = {
        '火影': [
          { name: '漩渦鳴人', url: 'https://zh.wikipedia.org/wiki/%E6%BC%A9%E6%B8%A6%E9%B3%B4%E4%BA%BA' },
          { name: '宇智波佐助', url: 'https://zh.wikipedia.org/wiki/%E5%AE%87%E6%99%BA%E6%B3%A2%E4%BD%90%E5%8A%A9' },
          { name: '春野櫻', url: 'https://zh.wikipedia.org/wiki/%E6%98%A5%E9%87%8E%E6%AB%BB' },
          { name: '旗木卡卡西', url: 'https://zh.wikipedia.org/wiki/%E6%97%97%E6%9C%A8%E5%8D%A1%E5%8D%A1%E8%A5%BF' },
        ],
        '航海王': [
          { name: '魯夫', url: 'https://zh.wikipedia.org/wiki/%E8%92%99%E5%A5%87%C2%B7D%C2%B7%E9%AD%AF%E5%A4%AB' },
          { name: '索隆', url: 'https://zh.wikipedia.org/wiki/%E7%BE%85%E7%BE%85%E4%BA%9E%C2%B7%E7%B4%A2%E9%9A%86' },
          { name: '娜美', url: 'https://zh.wikipedia.org/wiki/%E5%A8%9C%E7%BE%8E_(%E8%88%AA%E6%B5%B7%E7%8E%8B)' },
          { name: '騙人布', url: 'https://zh.wikipedia.org/wiki/%E9%A8%99%E4%BA%BA%E5%B8%83' },
          { name: '香吉士', url: 'https://zh.wikipedia.org/wiki/%E9%A6%99%E5%90%89%E5%A3%AB' },
        ]
      }
      setData(sampleData)
      setSelectedItem(sampleData[activeTab][0])
    }
  }

  const handleTabChange = (tab) => {
    setActiveTab(tab)
    if (data[tab] && data[tab].length > 0) {
      setSelectedItem(data[tab][0])
    }
  }

  const handleItemClick = (item) => {
    setSelectedItem(item)
  }

  const tabs = Object.keys(data)
  const currentItems = data[activeTab] || []

  return (
    <div className="app">
      {/* 頁籤列 */}
      <div className="tabs-container">
        {tabs.map(tab => (
          <button
            key={tab}
            className={`tab ${activeTab === tab ? 'active' : ''}`}
            onClick={() => handleTabChange(tab)}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* 主要內容區 */}
      <div className="content">
        {/* 左側列表 */}
        <div className="sidebar">
          <div className="sidebar-header">
            <h2>{activeTab}</h2>
            <span className="count">{currentItems.length} 項</span>
          </div>
          <div className="items-list">
            {currentItems.map((item, index) => (
              <div
                key={index}
                className={`item ${selectedItem?.name === item.name ? 'selected' : ''}`}
                onClick={() => handleItemClick(item)}
              >
                <span className="item-name">{item.name}</span>
                <svg 
                  className="item-icon" 
                  width="20" 
                  height="20" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2"
                >
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </div>
            ))}
          </div>
        </div>

        {/* 右側嵌入頁面 */}
        <div className="viewer">
          {selectedItem ? (
            <>
              <div className="viewer-header">
                <div className="viewer-title">
                  <h3>{selectedItem.name}</h3>
                  <a 
                    href={selectedItem.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="external-link"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                      <polyline points="15 3 21 3 21 9"></polyline>
                      <line x1="10" y1="14" x2="21" y2="3"></line>
                    </svg>
                    在新分頁開啟
                  </a>
                </div>
                <div className="url-bar">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                  </svg>
                  <span>{selectedItem.url}</span>
                </div>
              </div>
              <iframe
                src={selectedItem.url}
                className="iframe"
                title={selectedItem.name}
                sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
              />
            </>
          ) : (
            <div className="empty-state">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="9" y1="9" x2="15" y2="9"></line>
                <line x1="9" y1="15" x2="15" y2="15"></line>
              </svg>
              <p>請從左側選擇項目</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
