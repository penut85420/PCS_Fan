# PCS 小粉絲素材

## 說明
+ 這是 [PCS 小粉絲觀戰頻道](https://twitch.tv/pcs_fan/)用的素材，如果哪天我不幹了，歡迎全部拿去用

## 用法
+ `players.html` 將觀戰中的選手按照紅藍邊上色
+ `rank.html` 列出 PSG 戰隊成員的牌位
+ `timer.html` 冰島時間
+ `LetsGoPCS.png` 是頻道頭像
+ `Overlay_Final.png` 轉播用介面
+ `TrackingThePCS.json` 是 OBS 的場景檔案
+ `crawler.py` 查詢可觀戰選手的爬蟲程式
    + 會產生 `spec.txt`，每一行包含了 Game ID、遊戲時間與選手列表
    + 將想要關注的選手名稱當作參數傳入可以獲得觀戰指令
        + Ex: `python crawler.py Hanabi`
+ `crawler.sh` 執行爬蟲程式的範例指令
+ `manual.py` 將 Game ID 做為參數輸入可以獲得觀戰指令
    + Ex: `python manual.py 5247073787`

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

## 聯絡資訊
+ PTT 可以私信我 penut85420
+ Discord 也可以聯絡我 PenutChen#2135

## 授權
+ MIT License
