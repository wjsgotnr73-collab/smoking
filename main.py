import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("MY_API_KEY")

def get_busan_smoking_areas():
    print("🚬 부산광역시 흡연구역 통합 탐색을 시작합니다...\n")
    print("=" * 50)

    districts = [
        {
            "name": "서구", 
            "url": "https://api.odcloud.kr/api/15029124/v1/uddi:0a174c18-7056-460d-97d4-91abae89f6a3" 
        },
        {
            "name": "연제구", 
            "url": "https://api.odcloud.kr/api/15029124/v1/uddi:0a174c18-7056-460d-97d4-91abae89f6a3" 
        }
    ]
    
    for district in districts:
        print(f"🔎 [{district['name']}] 데이터를 서버에 요청합니다...\n")
        
        params = {
            'page': 1,
            'perPage': 5,          
            'serviceKey': API_KEY,
            'returnType': 'JSON'
        }
        
        try:
            response = requests.get(district['url'], params=params)
            
            if response.status_code == 200:
                data = response.json()
                areas = data.get('data', [])
                
                if not areas:
                    print(f"  -> 텅 비었네요... {district['name']} URL을 다시 확인해주세요.\n")
                    continue 

                print(f"  ✅  성공! {district['name']}에서 {len(areas)}개의 흡연구역 발견!\n")
                
            
                for index, area in enumerate(areas, start=1):
                    print(f"원본 데이터 확인: {area}\n") 
                    
                    location = area.get('시설명', area.get('설치위치', area.get('장소명', '위치 정보 없음')))
                    address = area.get('주소', area.get('소재지도로명주소', area.get('소재지지번주소', '주소 정보 없음')))
                    
                    print(f"  [{district['name']} {index}] 🏢 {location}")
                    print(f"      → {address}\n")
                
                print("-" * 50)
                    
            else:
                print(f"  ❌ [{district['name']}] 호출 실패! 에러 코드: {response.status_code}\n")
                
        except Exception as e:
            print(f"  🚨 [{district['name']}] 데이터 처리 중 오류 발생: {e}\n")

if __name__ == "__main__":
    get_busan_smoking_areas()