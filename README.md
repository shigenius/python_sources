# python_sources

### opencv_tracking.py

* 物体のトラッキング+トラッキングしている点を中心として矩形を抜き出す 

~~~
% opencv_tracking.py <movie_path> <output_dir_path> -s <skipflame_value>
~~~

* 実行後，最初のフレームでマウスクリックしたところに一番近い特徴点をトラッキングする．(Rキーでrun，Sキーでstop，spaceキーで1f進む)
* 30fpsの動画のみ対応. 他はガバ

### convert_to_image_each_labels.sh
* 動画を画像に変換する(ffmpegが必要)
* [makeDataset_forSpecificObjRecog.py](https://github.com/shigenius/tensorflow_works/blob/master/README.md#makedataset_forspecificobjrecogpy) のディレクトリ構造を作成する．
* 使う前のディレクトリ構造

~~~
dataset/
 + class1/
    + class1_video1.mp4
    + class1_video2.mov
 + class2/
    + class2_video1.mp4
    + class2_video2.mov
~~~

* 使い方
~~~
% sh convert_to_image_each_labels.sh
~~~

* そのあと`opencv_tracking.py`を適用する．

### camera_pos_regression/
環境 : python3.5 ffmpeg3.2.2

* カメラの位置姿勢を回帰推定するタスクのためのあれこれ
* 一番重要な回帰推定のコードはまだ書いていない．
* GT.txtに動画の各フレーム毎のカメラの座標(laとlo)と磁北が格納される
* 使用したカメラ : iPhone6s 720p HD/30 fps
* 使用したGPSロガー : ZweiteGPS https://itunes.apple.com/jp/app/zweitegps-gpsロガー-ビューア/id635080232?mt=8
* GPSロガーを起動し，記録開始してから動画を撮影する．
* 動画をひとつのディレクトリにまとめて，その下にjsonfileをまとめたディレクトリを作る
* 環境 : python3.5 ffmpeg3.2.2

~~~
% cd <movie_dir>
% sh rename_mov_to_unixtime.sh
% sh convert_to_images.sh
% python jsontest.py <latest_jsonfile_dir>
~~~

* 補足
  * convert_to_images.sh では1秒に2フレーム毎にサンプリングしていますが，ここを変更する場合は，4行目を変更し，同時にjsontest.pyの35行目 phototimeもいい感じに定義してください．
  * 磁北の向きはカメラの向きと90°ズレています．
