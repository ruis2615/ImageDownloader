import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 各種変数
saveDirPath: str = str(os.environ.get("SAVE_DIR").rstrip("/"))
logFileName: str = str(os.environ.get("SAVE_LOG_FILE_NAME"))
targetUrl: str = str(os.environ.get("TARGET_URL"))
pageQuery: str = str(os.environ.get("PAGE_QUERY"))
startPageNumber: int = int(os.environ.get("START_PAGE_NUMBER"))
stopPageNumber: int = int(os.environ.get("STOP_PAGE_NUMBER"))
excludeFiles: list = os.environ.get("EXCLUDE_FILES").split(",")

savedCount: int = 0
passedCount: int = 0

logFile = open(f"{saveDirPath}/{logFileName}.txt", mode="a", encoding="utf-8")


def findImageTags(url: str):
    """
    指定されたURLのページからimg要素を抽出し、画像URLとファイル名を取得する

    Args:
        url (str): スクレイピング対象のURL

    Returns:
        list: 画像情報の辞書（fileName, imageUrl）のリスト
    """
    responseResult = requests.get(url)
    imgTagsList = BeautifulSoup(responseResult.text, "html.parser").find_all("img")
    pendingImageUrls: list = []
    
    for imgTag in imgTagsList:
        imageUrl = imgTag.get("src")
        fileName = imageUrl.split("/")[-1]
        
        if fileName in excludeFiles:
            pass
        else:
            pendingImageUrls.append({"fileName": fileName, "imageUrl": imageUrl})
            
    return pendingImageUrls


def downloadImage(url: str, fileName: str):
    """
    指定されたURLから画像をダウンロードし、指定されたファイル名で保存する

    Args:
        url (str): ダウンロードする画像のURL
        fileName (str): 保存するファイル名
    """
    savedPath: str = f"{saveDirPath}/{fileName}"
    
    request = requests.get(url, stream=True)
    
    if request.status_code == 200:
        with open(savedPath, "wb") as imageFile:
            imageFile.write(request.content)
            
        print(f"{fileName}を保存しました。")
        logFile.write(f"\n{fileName}を保存しました")
    else:
        print(f"""
            何らかのエラーが発生し、保存されませんでした。
            ファイル名：{fileName}
            エラーコード：{request.status_code}
            """)
        logFile.write(f"\n{fileName}は、エラーコード{request.status_code}により保存できませんでした。")
    
    
def main():
    """
    メイン処理を実行する
    指定されたページ範囲で画像を検索し、ダウンロードを行う
    処理の開始・終了時刻やダウンロード状況をログファイルに記録する
    """
    logFile.write(f"────────────────────────────────────────\n{datetime.now().strftime('%Y年%m月%d日 - %H時%M分%S秒')} 開始")
    for pageNumber in range(startPageNumber, stopPageNumber):
        print(f"処理中のページ：{pageNumber}")
        logFile.write(f"\n{pageNumber}ページ目の処理を開始({datetime.now().strftime('%H時%M分%S秒')})")
        
        pendingImageUrls: list = findImageTags(f"{targetUrl}?{pageQuery}={pageNumber}")
        logFile.write(f"\n{pageNumber}ページ目で認識した画像枚数：{len(pendingImageUrls)}")
        
        for pendingImage in pendingImageUrls:
            downloadImage(pendingImage.get("imageUrl"), pendingImage.get("fileName"))
    
    print("すべての処理が完了しました。")
    logFile.write(f"\n{datetime.now().strftime('%Y年%m月%d日 - %H時%M分%S秒')} 終了\n────────────────────────────────────────")
    logFile.close()
            
            
if __name__ == "__main__":
    main()