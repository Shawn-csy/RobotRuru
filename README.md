# 專案說明

這是一個使用 Python Flask 框架構建的 LINE Bot 專案，該專案整合了 LINE Bot API 以提供多種功能。後端資料儲存在 Plurk API 2.0 中，並透過 Google Cloud Run 進行部署。

## 功能列表

- **星座運勢**
  - 輸入`星座名稱`以獲取當天運勢。
  - 使用 `-w` 選項以獲得該星座的週運勢。
  - 輸入`本週國師`以獲取當週運勢

- **籤詩**
  - 使用 `-抽籤` 可以抽取非淺草簽。
  - 使用 `抽淺草寺` 獲得籤詩和解籤。
  - 使用 `抽快樂淺草寺` 可獲得只有吉的籤詩。

- **天氣雷達**
  - 輸入`雷達`獲取即時天氣雲圖。

- **食物推薦**
  - 當使用者輸入`好餓`時，讀取資料庫推薦隨機店家。

- **隨機箱**
  - 輸入`-隨機 [ 物件 物件 物件 ]` 從物件中隨機挑選一個輸出, 可使用空格或,分隔

## 指令說明
`

- `--help`: 顯示說明文件。
- `--update [Google Map 連結]`: 更新推薦資料庫，連結至 Google Map。
- `--showfoodlist`: 顯示目前所有的食物推薦資料庫。

## 技術架構

- **框架**: Python Flask
- **LINE Bot API**: 提供 LINE Bot 功能。
- **後端資料庫**: Plurk API 2.0，用於儲存資料。
- **後端資料庫**: Google Cloud Storage，用於儲存圖片。
- **部署**: Google Cloud Run，透過 Google 的雲端基礎設施進行部署和執行。

## 如何使用

1. 註冊 LINE Bot 帳號並取得 API 金鑰。
2. 在 Google Cloud Platform 上建立項目，設定 Cloud Run 服務。
3. 將程式碼部署至 Cloud Run。
4. 將 Plurk API 金鑰設定至程式碼中，以存取後端資料庫。
5. 設定 LINE Bot API 金鑰。
6. 開始使用 LINE Bot！

## Update
  240422 : 增加國師統整 & 修復抽籤無顯示內容
