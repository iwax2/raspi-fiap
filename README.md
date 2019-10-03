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

## シリアル接続
USBシリアルモジュールのTX、RX、GNDを写真のようにpi0wと接続する。
シリアルモジュールのTXとpi0wのRX（10ピン）、シリアルモジュールのRXとpi0wのTX（8ピン）を接続することに注意。
doiboardとFT231Xを接続する場合は自動で接続されます。

![シリアル接続](https://github.com/iwax2/raspi-fiap/blob/master/pi0w-serial.jpg "pi0w-serial")

TeraTermなどでシリアル接続、シリアル設定のうちボーレートを115200に設定する。

## pi0wの設定
電源を入れて、pi / raspberryでログインする。

~~~
pi@raspberrypi:~$ sudo raspi-config
> 2 Network Options      Configure network settings
> N2 Wi-fi                   Enter SSID and passphrase
> JP Japan
> Ok
> Please enter SSID -> WiFi アクセスポイントのSSIDを入力
> Please enter passphrase. Leave it empty if none. -> パスワードを入力
> Finish
pi@raspberrypi:~$ ip a
2: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether b8:27:eb:d8:02:ea brd ff:ff:ff:ff:ff:ff
    inet 192.168.7.189/24 brd 192.168.7.255 scope global noprefixroute wlan0
pi@raspberrypi:~$ sudo apt update
pi@raspberrypi:~$ sudo apt upgrade -y
pi@raspberrypi:~$ sudo reboot
~~~
