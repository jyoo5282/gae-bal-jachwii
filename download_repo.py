import requests
import zipfile
import io
import os
import shutil

print("GitHub 저장소 다운로드를 시작합니다...")

# GitHub 저장소 ZIP 다운로드 URL
url = "https://github.com/kleosr/cursorkleosr/archive/refs/heads/main.zip"

try:
    print("1. ZIP 파일 다운로드 중...")
    response = requests.get(url)
    
    if response.status_code == 200:
        print("2. 다운로드 성공! 압축 해제 중...")
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall()
        print("3. 압축 해제 완료!")
        
        # 기존 폴더가 있다면 삭제
        if os.path.exists("cursorkleosr"):
            shutil.rmtree("cursorkleosr")
        
        # 폴더 이름 변경
        os.rename("cursorkleosr-main", "cursorkleosr")
        print("4. 모든 작업이 완료되었습니다!")
        print("저장소가 'cursorkleosr' 폴더에 다운로드되었습니다.")
    else:
        print(f"다운로드 실패: HTTP 상태 코드 {response.status_code}")
except Exception as e:
    print(f"오류가 발생했습니다: {str(e)}") 