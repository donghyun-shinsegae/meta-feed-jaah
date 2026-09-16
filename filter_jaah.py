import csv
import io
import urllib.request

FEED_URL = "https://feed.shinsegaev.com/upload/C00001/feed/basic_feed_brief.csv"
OUTPUT_FILE = "jaah_feed.csv"

def run_filter():
    print("1. 신세계V 피드 스트리밍 다운로드 및 필터링 시작...")
    req = urllib.request.Request(
        FEED_URL, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    
    # 파이프(|) 구분자 및 에러 방어 로직
    with urllib.request.urlopen(req, timeout=300) as response, \
         open(OUTPUT_FILE, mode="w", encoding="utf-8-sig", newline="") as outfile:
        
        text_stream = io.TextIOWrapper(response, encoding="utf-8-sig", errors="replace")
        reader = csv.reader(text_stream, delimiter='|')
        writer = csv.writer(outfile, delimiter='|')
        
        try:
            header = next(reader)
        except Exception as e:
            print(f"헤더 읽기 실패: {e}")
            return

        writer.writerow(header)
        
        # brand 컬럼 인덱스 찾기
        brand_idx = None
        for i, col in enumerate(header):
            if col.strip().lower() == "brand":
                brand_idx = i
                break
        
        count = 0
        while True:
            try:
                row = next(reader)
            except StopIteration:
                break
            except Exception:
                # 32만 행 중 비정상 포맷 행은 무시하고 통과
                continue
                
            if not row:
                continue
            
            # brand 컬럼이 정확히 JAAH인 경우만 수집 (구찌 품번 등 배제)
            is_jaah = False
            if brand_idx is not None and len(row) > brand_idx:
                if row[brand_idx].strip().upper() == "JAAH":
                    is_jaah = True
            else:
                if len(row) > 1 and row[1].strip().startswith("[JAAH]"):
                    is_jaah = True
            
            if is_jaah:
                writer.writerow(row)
                count += 1
                
        print(f"2. 완료! 총 {count}개의 JAAH 상품이 {OUTPUT_FILE}에 저장되었습니다.")

if __name__ == "__main__":
    run_filter()
