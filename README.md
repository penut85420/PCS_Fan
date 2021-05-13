# PCS 小粉絲素材

## 說明
+ 這是 [PCS 小粉絲觀戰頻道](https://twitch.tv/pcs_fan/)用的素材，如果哪天我不幹了，歡迎全部拿去用

## 用法
+ 檔案說明文件尚未補齊

### 實況介面
+ `obs/players.html` 將觀戰中的選手按照紅藍邊上色
+ `obs/rank.html` 列出 PSG 戰隊成員的牌位
+ `obs/timer.html` 冰島時間
+ `imgs/Overlay_Final.png` 轉播用介面
+ `imgs/LetsGoPCS.png` 是頻道頭像
+ `obs/TrackingThePCS.json` 是 OBS 的場景檔案

### 程式碼
+ `tracking/champions.py` 取得英雄名稱列表
    + `get_en_zh_champs()` 為中英對照的版本
    + `get_id2champs()` 為 ID 與英雄名稱對應的版本
+ `tracking/riots.py` 使用 Riots API 取得對戰資訊
+ `tracking/trackingthepros.py` 使用 TrackingThePros API 取得選手資訊
    + `get_rnsn_idx()` 取得選手 ID 與遊戲 ID 的對應表
    + `get_player_list()` 取得選手列表
    + `get_spec_list()` 取得觀戰資訊
    + `get_spec_cmd()` 取得觀戰指令
    + `get_game_id()` 取得對局的 ID
+ `tracking/query` 下為取得各種資訊的主程式
    + `game_id.py` 根據選手名稱取得對局的 ID
    + `match.py` 根據選手名稱產生該場對局的場上選手資訊
    + `opgg.py` 取得 PSG 成員的西歐伺服器積分狀況
    + `players.py` 從 TrackingThePros 官網取得完整的選手資訊
        + 包含隊伍、位置與遊戲中的 ID
    + `spec_cmd.py` 取得觀戰指令
    + `spec.py` 取得現在選手的當前積分對戰列表

### 資料
+ `data/champions_enzh.json` 英雄的英中全名，協助減少字卡的錯字
+ `data/champs.json` 為 ID 與英雄名的對應列表
+ `data/players.json` 包含隊名與位置的選手資訊
+ `rn2sn.json` 是選手名稱與遊戲 ID 的對應表
+ `sn2rn.json` 是遊戲 ID 與選手名稱的對應表
+ `role_map.json` 是位置的縮寫對應

### 腳本
+ 筆者主要使用 WSL 部屬後台，所以使用了大量的 `.sh` 檔

## 配置
### 實況設定
+ 位元率控制：CBR
+ 位元速率：5000 Kbps
+ 編碼器：NVIDIA NVENC H.264
+ 輸出大小：1920x1080 60 FPS

### Nightbot
+ 指令
    + `!id` - `MSI 選手 ID 對照表，感謝魚丸 https://reurl.cc/L0Gnjx`
    + `!rank` - `MSI 選手西歐服牌位查詢 https://www.trackingthepros.com/bootcamp`
+ Spam Protection 全部 Disable

### Banner LOGO
+ [LOGO 產生器](https://cooltext.com/Edit-Logo?LogoId=3831589600)
+ 產生出來的 LOGO 長寬會不同，要用其他圖片編輯器微調
    + [Photopea](https://www.photopea.com/)

## 聯絡資訊
+ PTT 可以私信我 penut85420
+ Discord 也可以聯絡我 PenutChen#2135

## 授權
+ MIT License
