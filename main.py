# -*- coding: utf-8 -*-
"""
玩具資料瀏覽器 - 一鍵啟動腳本

執行此檔案將會：
1. 啟動 Flask 後端伺服器
2. 自動開啟瀏覽器
3. 提供優雅的關閉機制
"""

import os
import sys
import time
import subprocess
import webbrowser
import signal
from pathlib import Path

# 設定編碼
if sys.platform == 'win32':
    os.system('color')
    # Windows 編碼設定
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

class Colors:
    """終端機顏色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """顯示歡迎橫幅"""
    banner = f"""
{Colors.CYAN}{'=' * 60}
{Colors.BOLD}玩具資料瀏覽器{Colors.END}
{Colors.CYAN}{'=' * 60}{Colors.END}
"""
    print(banner)

def check_requirements():
    """檢查必要檔案和套件"""
    print(f"{Colors.YELLOW}[檢查] 系統需求...{Colors.END}")
    
    # 檢查 Excel 檔案
    excel_file = "list.xlsx"
    if not os.path.exists(excel_file):
        print(f"{Colors.RED}[X] 找不到 {excel_file}，請先準備 Excel 檔案{Colors.END}")
        return False
    print(f"{Colors.GREEN}[OK] Excel 檔案: {excel_file}{Colors.END}")
    
    # 檢查 backend 目錄
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print(f"{Colors.RED}[X] 找不到 backend 資料夾{Colors.END}")
        return False
    print(f"{Colors.GREEN}[OK] 後端目錄: backend/{Colors.END}")
    
    # 檢查 app.py
    app_file = backend_dir / "app.py"
    if not app_file.exists():
        print(f"{Colors.RED}[X] 找不到 backend/app.py{Colors.END}")
        return False
    print(f"{Colors.GREEN}[OK] 後端程式: backend/app.py{Colors.END}")
    
    # 檢查 frontend 目錄
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print(f"{Colors.RED}[X] 找不到 frontend 資料夾{Colors.END}")
        return False
    print(f"{Colors.GREEN}[OK] 前端目錄: frontend/{Colors.END}")
    
    # 檢查 index.html
    index_file = frontend_dir / "index.html"
    if not index_file.exists():
        print(f"{Colors.RED}[X] 找不到 frontend/index.html{Colors.END}")
        return False
    print(f"{Colors.GREEN}[OK] 前端頁面: frontend/index.html{Colors.END}")
    
    # 檢查必要的 Python 套件
    print(f"\n{Colors.YELLOW}[檢查] Python 套件...{Colors.END}")
    required_packages = ['flask', 'flask_cors', 'pandas', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"{Colors.GREEN}[OK] {package}{Colors.END}")
        except ImportError:
            print(f"{Colors.RED}[X] {package} (未安裝){Colors.END}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n{Colors.YELLOW}[警告] 發現缺少套件，正在安裝...{Colors.END}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'
            ])
            print(f"{Colors.GREEN}[OK] 套件安裝完成{Colors.END}")
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}[X] 套件安裝失敗，請手動執行: pip install -r backend/requirements.txt{Colors.END}")
            return False
    
    print(f"\n{Colors.GREEN}[完成] 所有檢查通過！{Colors.END}\n")
    return True

def start_backend():
    """啟動後端伺服器"""
    print(f"{Colors.BLUE}[啟動] 後端伺服器...{Colors.END}")
    
    # 切換到 backend 目錄並啟動
    backend_script = os.path.join("backend", "app.py")
    
    if sys.platform == 'win32':
        # Windows: 使用 CREATE_NEW_PROCESS_GROUP
        process = subprocess.Popen(
            [sys.executable, backend_script],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
    else:
        # Linux/Mac
        process = subprocess.Popen(
            [sys.executable, backend_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
    
    # 等待伺服器啟動
    print(f"{Colors.YELLOW}[等待] 伺服器啟動...{Colors.END}")
    time.sleep(3)
    
    # 檢查伺服器是否啟動成功
    if process.poll() is not None:
        print(f"{Colors.RED}[X] 後端伺服器啟動失敗{Colors.END}")
        return None
    
    print(f"{Colors.GREEN}[OK] 後端伺服器已啟動 (PID: {process.pid}){Colors.END}")
    return process

def open_browser(url="http://localhost:5000", delay=2):
    """開啟瀏覽器"""
    print(f"\n{Colors.BLUE}[瀏覽器] 準備開啟...{Colors.END}")
    time.sleep(delay)
    
    try:
        webbrowser.open(url)
        print(f"{Colors.GREEN}[OK] 瀏覽器已開啟: {url}{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.YELLOW}[警告] 無法自動開啟瀏覽器: {e}{Colors.END}")
        print(f"{Colors.YELLOW}  請手動開啟: {url}{Colors.END}")
        return False

def show_instructions():
    """顯示使用說明"""
    instructions = f"""
{Colors.CYAN}{'=' * 60}
{Colors.BOLD}使用說明{Colors.END}
{Colors.CYAN}{'=' * 60}{Colors.END}

{Colors.GREEN}[OK]{Colors.END} 伺服器正在運行於: {Colors.BOLD}http://localhost:5000{Colors.END}

{Colors.YELLOW}[功能]{Colors.END}
  - 點擊頂部頁籤切換分類
  - 點擊「預覽」按鈕搜尋商品圖片
  - 點擊「重新載入」更新 Excel 資料

{Colors.YELLOW}[更新資料]{Colors.END}
  1. 替換專案根目錄的 list.xlsx 檔案
  2. 在網頁右上角點擊「重新載入」按鈕

{Colors.YELLOW}[關閉程式]{Colors.END}
  按 {Colors.BOLD}Ctrl+C{Colors.END} 或直接關閉此視窗

{Colors.CYAN}{'=' * 60}{Colors.END}
"""
    print(instructions)

def cleanup(backend_process):
    """清理資源並關閉伺服器"""
    print(f"\n{Colors.YELLOW}[關閉] 正在關閉伺服器...{Colors.END}")
    
    if backend_process and backend_process.poll() is None:
        try:
            if sys.platform == 'win32':
                # Windows: 使用 taskkill
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(backend_process.pid)], 
                             capture_output=True)
            else:
                # Linux/Mac: 使用 SIGTERM
                backend_process.terminate()
                backend_process.wait(timeout=5)
            
            print(f"{Colors.GREEN}[OK] 伺服器已關閉{Colors.END}")
        except Exception as e:
            print(f"{Colors.YELLOW}[警告] 關閉伺服器時發生錯誤: {e}{Colors.END}")
    
    print(f"\n{Colors.BLUE}感謝使用！再見！{Colors.END}\n")

def main():
    """主程式"""
    backend_process = None
    
    try:
        # 顯示歡迎訊息
        print_banner()
        
        # 檢查系統需求
        if not check_requirements():
            print(f"\n{Colors.RED}[X] 系統檢查失敗，程式結束{Colors.END}\n")
            sys.exit(1)
        
        # 啟動後端伺服器
        backend_process = start_backend()
        if backend_process is None:
            print(f"\n{Colors.RED}[X] 無法啟動後端伺服器{Colors.END}\n")
            sys.exit(1)
        
        # 開啟瀏覽器
        open_browser()
        
        # 顯示使用說明
        show_instructions()
        
        # 保持程式運行
        print(f"{Colors.GREEN}[運行中] 系統運行中...{Colors.END} (按 Ctrl+C 停止)\n")
        
        # 監控後端進程
        while True:
            time.sleep(1)
            
            # 檢查後端是否還在運行
            if backend_process.poll() is not None:
                print(f"\n{Colors.RED}[X] 後端伺服器意外停止{Colors.END}")
                break
    
    except KeyboardInterrupt:
        # 用戶按下 Ctrl+C
        print(f"\n{Colors.YELLOW}[停止] 收到停止信號{Colors.END}")
    
    except Exception as e:
        print(f"\n{Colors.RED}[X] 發生錯誤: {e}{Colors.END}")
    
    finally:
        # 清理資源
        cleanup(backend_process)

if __name__ == "__main__":
    main()
