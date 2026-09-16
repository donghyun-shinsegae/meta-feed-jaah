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

        # 메모리 폭발을 방지하기 위해 스트리밍(한 줄씩) 디코딩 처리
        text_stream = io.TextIOWrapper(response, encoding="utf-8-sig", errors="ignore")
        reader = csv.reader(text_stream)
        writer = csv.writer(outfile)

        # 헤더 읽기 및 작성
        header = next(reader)
        writer.writerow(header)

        # 'brand' 컬럼 인덱스 찾기
        brand_idx = None
        for i, col in enumerate(header):
            if "brand" in col.lower():
                brand_idx = i
                break

        count = 0
        for row in reader:
            if not row:
                continue

            # 브랜드 컬럼이 특정되면 해당 위치 체크, 없으면 전체 셀에서 탐색
            is_jaah = False
            if brand_idx is not None and len(row) > brand_idx:
                if "jaah" in str(row[brand_idx]).strip().lower():
                    is_jaah = True
            else:
                if any("jaah" in str(cell).strip().lower() for cell in row):
                    is_jaah = True

            if is_jaah:
                writer.writerow(row)
                count += 1

        print(f"2. 필터링 완료! 총 {count}개 JAAH 상품이 {OUTPUT_FILE}에 저장되었습니다.")

if __name__ == "__main__":
    run_filter()
