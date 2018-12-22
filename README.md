
## YOLP(Yahoo Open Local Platform)からデータを取得するために
利用しているapiは下記urlのもです。
アプリケーション開発のページからappidを取得してください。
https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/weather.html

## slackのurlについて
slackのwebhook urlを取得してください。
https://qiita.com/vmmhypervisor/items/18c99624a84df8b31008

## 位置情報について
下記のサイトから目的の場所の座標を取得してください。
http://www.geocoding.jp

## 設定ファイルについて
settings.ymlに下記の内容を記入してください。
```yaml
slack:
  url: https://xxxxxxxxxxxxxxxxxxx
YOLP:
  appid: xxxxxxxxxxxxxxxxxxxxxxxxx
coordinates:
- 経度 (longitude)
- 緯度 (latitude) 
```