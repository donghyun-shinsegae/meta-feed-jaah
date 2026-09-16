import csv
import io
import urllib.request

FEED_URL = "https://feed.shinsegaev.com/upload/C00001/feed/basic_feed_brief.csv"
OUTPUT_FILE = "jaah_feed.csv"

def run_filter():
    print("1. 신세계V 피드 다운로드 시작...")
    req = urllib.request.Request(
        FEED_URL, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    
    with urllib.request.urlopen(req, timeout=180) as response, \
         open(OUTPUT_FILE, mode="w", encoding="utf-8-sig", newline="") as outfile:
        
        # 파이프(|) 구분자 지정 파싱
        text_stream = io.TextIOWrapper(response, encoding="utf-8-sig", errors="ignore")
        reader = csv.reader(text_stream, delimiter='|')
        writer = csv.writer(outfile, delimiter='|')
        
        # 1. 헤더 행 읽기 및 작성
        header = next(reader)
        writer.writerow(header)
        
        # 2. 'brand' 컬럼 인덱스 찾기
        brand_idx = None
        for i, col in enumerate(header):
            if col.strip().lower() == "brand":
                brand_idx = i
                break
        
        count = 0
        for row in reader:
            if not row or len(row) != len(header):
                continue
            
            # brand 컬럼이 정확히 'JAAH'인 행만 엄격하게 수집 (구찌 JAAH3 등 배제)
            is_target = False
            if brand_idx is not None and len(row) > brand_idx:
                if row[brand_idx].strip().upper() == "JAAH":
                    is_target = True
            else:
                # brand 컬럼이 없을 경우 title 앞자리 [JAAH] 기준 필터
                if len(row) > 1 and row[1].strip().startswith("[JAAH]"):
                    is_target = True
            
            if is_target:
                writer.writerow(row)
                count += 1
                
        print(f"2. 필터링 완료! 총 {count}개의 순수 JAAH 상품만 정상 저장되었습니다.")

if __name__ == "__main__":
    run_filter()
