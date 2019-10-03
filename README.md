raspi-fiap
==

## Raspbianのダウンロード
http://ftp.jaist.ac.jp/pub/raspberrypi/raspbian_lite/images/
から最新のliteイメージをダウンロード（2019/10/3現在最新2019-09-26-raspbian-buster-lite.zip）

## イメージの書き込み
[Rufus](https://rufus.ie/)を利用してダウンロードしたzipファイルを書き込み


## シリアルコンソールの有効化
書き込んだbootドライブのconfig.txtの最終行に追記
`dtoverlay=pi3-miniuart-bt`

https://www.usagi1975.com/201907061439/


