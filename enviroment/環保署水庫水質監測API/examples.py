"""
環保署水庫水質監測 API 使用範例
Taiwan EPA Reservoir Water Quality Monitoring API Examples
"""

import requests
from typing import Optional, List, Dict, Any

# API 設定
API_KEY = "e0a736f5-a240-4a28-8ca1-d8ae7604334d"
BASE_URL = "https://data.moenv.gov.tw/api/v2"


class ReservoirWaterQualityAPI:
    """水庫水質監測 API 客戶端"""
    
    def __init__(self, api_key: str = API_KEY):
        self.api_key = api_key
        self.base_url = BASE_URL
    
    def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """發送 API 請求"""
        url = f"{self.base_url}/{endpoint}"
        
        request_params = {
            "api_key": self.api_key,
            "format": "json"
        }
        
        if params:
            request_params.update(params)
        
        response = requests.get(url, params=request_params, timeout=30)
        response.raise_for_status()
        
        return response.json()
    
    def get_water_quality(
        self, 
        limit: int = 1000,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        獲取水庫水質監測資料 (單頁)
        
        Args:
            limit: 回傳筆數限制 (最大 1000)
            offset: 資料偏移量
        
        Returns:
            API 回應資料列表
        """
        params = {
            "limit": min(limit, 1000),
            "offset": offset
        }
        return self._make_request("wqx_p_03", params)
    
    def get_reservoir_data(
        self,
        reservoir_keyword: str,
        year: Optional[str] = None,
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        獲取特定水庫的水質監測資料 (自動分頁遍歷)
        
        Args:
            reservoir_keyword: 水庫英文關鍵字 (如 "A-Kung-Tien", "Fei-Tsui")
            year: 年份篩選 (如 "2024"), 可選
            progress_callback: 進度回調函數 (可選)
        
        Returns:
            符合條件的水質監測資料列表
        """
        all_records = []
        offset = 0
        
        while True:
            data = self.get_water_quality(limit=1000, offset=offset)
            
            if not data:
                break
            
            for record in data:
                site = record.get('siteengname', '') or ''
                date = record.get('sampledate', '') or ''
                
                if reservoir_keyword in site:
                    if year is None or date.startswith(year):
                        all_records.append(record)
            
            if progress_callback:
                progress_callback(offset, len(all_records))
            
            if len(data) < 1000:
                break
            offset += 1000
        
        return all_records
    
    def get_monitoring_stations(
        self, 
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        獲取水庫水質監測站基本資料
        
        Args:
            limit: 回傳筆數限制
        
        Returns:
            API 回應資料列表
        """
        params = {"limit": min(limit, 1000)}
        return self._make_request("wqx_p_08", params)
    
    def get_monthly_data(
        self, 
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        獲取水庫水質月監測資料
        
        Args:
            limit: 回傳筆數限制
        
        Returns:
            API 回應資料列表
        """
        params = {"limit": min(limit, 1000)}
        return self._make_request("wqx_p_117", params)
    
    def list_reservoirs(self) -> List[str]:
        """
        列出所有有監測資料的水庫名稱
        
        Returns:
            水庫英文名稱列表
        """
        data = self.get_monitoring_stations(limit=1000)
        records = data if isinstance(data, list) else []
        
        reservoirs = set()
        for record in records:
            dame = record.get("damename")
            if dame:
                reservoirs.add(dame)
        
        return sorted(list(reservoirs))
    
    def get_latest_quality(self, reservoir_keyword: str) -> Dict[str, Any]:
        """
        獲取指定水庫的最新水質資料
        
        Args:
            reservoir_keyword: 水庫英文關鍵字 (如 "Fei-Tsui", "A-Kung-Tien")
        
        Returns:
            最新水質資料
        """
        print(f"正在查詢 {reservoir_keyword} 資料...（需要幾分鐘）")
        records = self.get_reservoir_data(reservoir_keyword)
        
        if not records:
            return {"error": f"找不到 {reservoir_keyword} 的水質資料"}
        
        latest_date = max(r.get("sampledate", "") for r in records)
        latest_records = [
            r for r in records 
            if r.get("sampledate") == latest_date
        ]
        
        return {
            "reservoir": reservoir_keyword,
            "sample_date": latest_date,
            "record_count": len(latest_records),
            "measurements": latest_records
        }


def main():
    """主程式示範"""
    api = ReservoirWaterQualityAPI()
    
    # 示範 1: 列出所有水庫
    print("=== 可用水庫列表 ===")
    reservoirs = api.list_reservoirs()
    for r in reservoirs[:10]:
        print(f"  - {r}")
    print(f"  ... 共 {len(reservoirs)} 個水庫")
    print()
    
    # 示範 2: 獲取阿公店水庫2024年資料
    print("=== 阿公店水庫 2024年資料 ===")
    
    def progress(offset, count):
        print(f"  已掃描: offset={offset}, 找到 {count} 筆")
    
    data = api.get_reservoir_data("A-Kung-Tien", "2024", progress)
    print(f"\n總計找到 {len(data)} 筆 2024年資料")
    
    # 分析採樣日期
    dates = sorted(set(r.get('sampledate', '')[:10] for r in data))
    print(f"採樣日期: {dates}")
    
    # 顯示優養化指標
    eutro_items = ['Carlson Trophic State Index', 'Chlorophyl-A', 'Total-Phosphate']
    for item in eutro_items:
        values = [r.get('itemvalue') for r in data if r.get('itemengname') == item]
        values = [v for v in values if v and v != '-']
        if values:
            print(f"  {item}: {values[:5]}...")
    print()
    
    # 示範 3: 列出監測站
    print("=== 監測站資訊 ===")
    stations = api.get_monitoring_stations()
    for s in stations[:5]:
        print(f"  {s.get('siteengname')} - {s.get('damename')}")
    print()


if __name__ == "__main__":
    main()
