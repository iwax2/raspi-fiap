raspi-fiap
==

## 必要なもの
+ Raspberry Zero WH https://www.switch-science.com/catalog/3646/
+ microSDカード（32GBまで） https://www.dospara.co.jp/5shopping/detail_parts.php?bg=7&br=219&sbr=1043&ic=369719&lf=0
+ AE-BME280 (J3をハンダでジャンパする) http://akizukidenshi.com/catalog/g/gK-09421/
+ AE-FT231X http://akizukidenshi.com/catalog/g/gK-06894/
+ microUSBケーブル（2本）
+ DoiBoard
+ 細ピンヘッダ http://akizukidenshi.com/catalog/g/gC-10073/
+ 2列ピンヘッダ http://akizukidenshi.com/catalog/g/gC-00085/

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
![DOIBOARDのサンプル](https://github.com/iwax2/raspi-fiap/blob/master/doiboard-sample.jpg "doiboard-sample")

TeraTermなどでシリアル接続、シリアル設定のうちボーレートを115200に設定する。

## pi0wの設定
電源を入れて、pi / raspberryでログインする。

~~~
pi@raspberrypi:~$ sudo raspi-config
> 1 Change User Password Change password for the current user
> 2 Network Options      Configure network settings
> N2 Wi-fi                   Enter SSID and passphrase
> JP Japan
> Ok
> Please enter SSID -> WiFi アクセスポイントのSSIDを入力
> Please enter passphrase. Leave it empty if none. -> パスワードを入力
> 4 Localisation Options Set up language and regional settings to match your
> I2 Change Timezone        Set up timezone to match your location
> Asia
> Tokyo
> 5 Interfacing Options  Configure connections to peripherals
> P5 I2C         Enable/Disable automatic loading of I2C kernel module
> Would you like the ARM I2C interface to be enabled? <Yes>
> Ok
> Finish
pi@raspberrypi:~$ ip a
2: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether b8:27:eb:d8:02:ea brd ff:ff:ff:ff:ff:ff
    inet 192.168.7.189/24 brd 192.168.7.255 scope global noprefixroute wlan0
pi@raspberrypi:~$ sudo apt update
pi@raspberrypi:~$ sudo apt upgrade -y
pi@raspberrypi:~$ sudo reboot
~~~

## アップローダの設定
~~~
pi@raspberrypi:~$ sudo apt install -y git
pi@raspberrypi:~$ sudo apt install -y python3-pip
pi@raspberrypi:~$ sudo apt install -y python3-smbus i2c-tools
pi@raspberrypi:~$ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- 76 --
pi@raspberrypi:~$ sudo pip3 install RPi.bme280
pi@raspberrypi:~$ sudo pip3 install "git+https://github.com/PlantFactory/pyfiap"
pi@raspberrypi:~$ git clone https://github.com/iwax2/raspi-fiap
pi@raspberrypi:~$ cd raspi-fiap
pi@raspberrypi:~$ vi bme280test.py
> ポイントIDを適宜変更する
pi@raspberrypi:~$ python3 bme280test.py
pi@raspberrypi:~/raspi-fiap$ crontab -e
no crontab for pi - using an empty one

Select an editor.  To change later, run 'select-editor'.
  1. /bin/nano        <---- easiest
  2. /usr/bin/vim.tiny
  3. /bin/ed

Choose 1-3 [1]: 2
> 最終行に追記（毎分アップロード）
# m h  dom mon dow   command
* * * * * python3 /home/pi/raspi-fiap/bme280test.py
~~~

https://iot.info.nara-k.ac.jp/viewer/fiapd/ を確認して指定したポイントIDでアップロードされていることを確認する


## ビューワの設定
http://iot.info.nara-k.ac.jp:3000/ で作成したポイントIDを設定する。

1. Nara Globalに移動
1. エリアにNewで作成
    1. エリア表示名に適当な設置場所を記入
    1. 説明文には日本語も使って何に使っているのかなどを記入
    1. ステータスをenabledに変更
1. グラフ軸にNewで作成
    1. 名前にはグラフ軸の名前
    1. 軸テキストにはグラフの縦軸に表示する名前＋単位などをつける良い
    1. ステータスをenabledに変更
    1. グラフに用いるすべての縦軸を設定する
1. ポイントにNewで作成
    1. ポイント表示名にはグラフへの表示／非表示を切り替えるボタンに記入する文字列を記入
    1. ポイントIDにはアップロードに用いたID ( http://tomato.fukuoka.lab/bme280/temperature ) などを記入
    1. 適切なグラフ軸を選択
    1. ステータスをenabledに変更

https://iot.info.nara-k.ac.jp/viewer/ を確認して作成したエリアを選択、表示されることを確認する。
表示されない場合は設定を適宜修正する。もしくはちゃんと指定した日時にアップロードできているか、
https://iot.info.nara-k.ac.jp/viewer/fiapd/ を確認する。


