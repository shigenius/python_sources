### rename_mov_to_unixtime.sh

* 

### convert_to_images.sh
dependence : ffmpeg
* 動画を画像に変換する

### associateGPSLogwithImages.py

* GPSロガーから吐いたGPSのログが記述してあるjsonファイルと，convert_to_images.shで出力した系列画像郡を対応付けて，GT.txtとして出力する．
* 用いたGPSロガー : ZweiteGPS https://itunes.apple.com/jp/app/zweitegps-gpsロガー-ビューア/id635080232?mt=8
* 動画をひとつのディレクトリにまとめて，その下にjsonfileをまとめたディレクトリを作る．
* 補足
  * 磁北の向きはカメラの向きと90°ズレている(iphoneを横にして撮影した場合)．
~~~
% python jsontest.py <latest_jsonfile_dir>
~~~
