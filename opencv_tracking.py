import cv2
import numpy as np

import csv
import argparse

# Esc キー
ESC_KEY = 0x1b
# s キー
S_KEY = 0x73
# r キー
R_KEY = 0x72
# 特徴点の最大数
MAX_FEATURE_NUM = 500
# 反復アルゴリズムの終了条件
CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
# インターバル （1000 / フレームレート）
INTERVAL = 5
# ビデオデータ
# VIDEO_DATA = '/Users/shigetomi/Desktop/place_recognition_10class_0914/wall1/10am_20170820_sunny_wall1_uragawa.MOV'

# rectangle size (x, y)
# RECTANGLE_SIZE_X = 256
# RECTANGLE_SIZE_Y = 256

# OUTPUT_DIRECTORY = '/Users/shigetomi/Desktop/tmp/'

class Motion:
    # コンストラクタ
    def __init__(self, _target, _output, _skipframe, _rectsize_x, _rectsize_y):
        # 表示ウィンドウ
        cv2.namedWindow("motion")
        # マウスイベントのコールバック登録
        cv2.setMouseCallback("motion", self.onMouse)
        # 映像
        self.video = cv2.VideoCapture(_target)
        # インターバル
        #self.interval = INTERVAL
        self.interval = 0 
        # 現在のフレーム（カラー)
        self.frame = None
        # 現在のフレーム（グレー）
        self.gray_next = None
        # 前回のフレーム（グレー）
        self.gray_prev = None
        # 特徴点
        self.features = None
        # 特徴点のステータス
        self.status = None

        self.output = _output
        self.skipframe = _skipframe
        self.rectsize_x = _rectsize_x
        self.rectsize_y = _rectsize_y

        self.targetname = _target
        self.screen_width =  self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.screen_height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.bg = np.zeros((int(self.screen_height+(self.rectsize_y*2)), int(self.screen_width+(self.rectsize_x*2)), 3)) #矩形がはみ出た時用のback ground

        print("original video fps:" + str(self.video.get(cv2.CAP_PROP_FPS)))

    # メインループ
    def run(self):

        # 最初のフレームの処理
        end_flag, self.frame = self.video.read()
        self.video = cv2.VideoCapture(self.targetname) # 再初期化 (1フレーム目でrectを指定するため)
        self.gray_prev = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        log = open(self.output + "/subwindow_log.txt", 'w')
        writer = csv.writer(log, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(("frame","center_x", "center_y", "size_x", "size_y"))

        proc_count = 0 # ループの回数
        frame_count = 1 # jpgのindex 4桁
        while end_flag:
            skipflag = False if (proc_count % self.skipframe == 1) else True
            print(frame_count, proc_count, skipflag)

            # グレースケールに変換
            self.gray_next = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # 特徴点が登録されている場合にOpticalFlowを計算する
            if self.features is not None:
                # オプティカルフローの計算
                features_prev = self.features
                self.features, self.status, err = cv2.calcOpticalFlowPyrLK( \
                                                    self.gray_prev, \
                                                    self.gray_next, \
                                                    features_prev, \
                                                    None, \
                                                    winSize = (10, 10), \
                                                    maxLevel = 3, \
                                                    criteria = CRITERIA, \
                                                    flags = 0)

                # 有効な特徴点のみ残す
                self.refreshFeatures()

                # フレームに有効な特徴点を描画
                if (self.features is not None and skipflag is False):
                    for feature in self.features:
                        rect_x = int(feature[0][0]-self.rectsize_x/2) # 矩形の始点(ひだりうえ)のx座標
                        rect_y = int(feature[0][1]-self.rectsize_y/2)

                        # 矩形が画像からはみ出ても矩形のサイズが固定であることを保障する．
                        if (rect_x < 0 or rect_y < 0 or (rect_x+self.rectsize_x) > self.screen_width or (rect_y+self.rectsize_y) > self.screen_height): # 矩形がscreenからはみ出ている場合
                            print("枠からでたよ") #paddingする処理をかく # 元のフレームをzerosで拡張してそのフレームから矩形を抜き出す
                            self.bg[self.rectsize_y:self.rectsize_y+self.screen_height, self.rectsize_x:self.rectsize_x+self.screen_width] = self.frame # 余白をつける
                            rectangle = self.bg[self.rectsize_y+rect_y:self.rectsize_y*2+rect_y, self.rectsize_x+rect_x:self.rectsize_x*2+rect_x] #
                        else:
                            rectangle = self.frame[rect_y:rect_y+self.rectsize_y, rect_x:rect_x+self.rectsize_x] # そのまま矩形を抜き出す
                        cv2.imwrite(self.output + "image_" + '%04d' % frame_count + ".jpg", rectangle)
                        writer.writerow((frame_count, feature[0][0], feature[0][1], self.rectsize_x, self.rectsize_y))
                        cv2.circle(self.frame, (feature[0][0], feature[0][1]), 4, (15, 241, 255), -1, 8, 0)
                        # 追加
                        cv2.rectangle(self.frame, (rect_x, rect_y), (rect_x + self.rectsize_x, rect_y + self.rectsize_y), (255, 0, 0,), 3 , 4)

            # 表示
            cv2.imshow("motion", self.frame)

            # 次のループ処理の準備
            self.gray_prev = self.gray_next
            end_flag, self.frame = self.video.read()
            if end_flag:
                self.gray_next = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # インターバル
            key = cv2.waitKey(self.interval)
            # "Esc"キー押下で終了
            if key == ESC_KEY:
                break
            # "s"キー押下で一時停止
            elif key == S_KEY:
                self.interval = 0
            elif key == R_KEY:
                self.interval = INTERVAL

            proc_count += 1
            if skipflag is False:
                frame_count += 1


        # 終了処理
        cv2.destroyAllWindows()
        self.video.release()

        log.close

    # マウスクリックで特徴点を指定する
    #     クリックされた近傍に既存の特徴点がある場合は既存の特徴点を削除する
    #     クリックされた近傍に既存の特徴点がない場合は新規に特徴点を追加する
    def onMouse(self, event, x, y, flags, param):
        # 左クリック以外
        if event != cv2.EVENT_LBUTTONDOWN:
            return

        # 最初の特徴点追加
        if self.features is None:
            self.addFeature(x, y)
            return

        # 探索半径（pixel）
        radius = 5
        # 既存の特徴点が近傍にあるか探索
        index = self.getFeatureIndex(x, y, radius)

        # クリックされた近傍に既存の特徴点があるので既存の特徴点を削除する
        if index >= 0:
            self.features = np.delete(self.features, index, 0)
            self.status = np.delete(self.status, index, 0)

        # クリックされた近傍に既存の特徴点がないので新規に特徴点を追加する
        else:
            #self.addFeature(x, y)
            pass
        return


    # 指定した半径内にある既存の特徴点のインデックスを１つ取得する
    #     指定した半径内に特徴点がない場合 index = -1 を応答
    def getFeatureIndex(self, x, y, radius):
        index = -1

        # 特徴点が１つも登録されていない
        if self.features is None:
            return index

        max_r2 = radius ** 2
        index = 0
        for point in self.features:
            dx = x - point[0][0]
            dy = y - point[0][1]
            r2 = dx ** 2 + dy ** 2
            if r2 <= max_r2:
                # この特徴点は指定された半径内
                return index
            else:
                # この特徴点は指定された半径外
                index += 1

        # 全ての特徴点が指定された半径の外側にある
        return -1


    # 特徴点を新規に追加する
    def addFeature(self, x, y):

        # 特徴点が未登録
        if self.features is None:
            # ndarrayの作成し特徴点の座標を登録
            self.features = np.array([[[x, y]]], np.float32)
            self.status = np.array([1])
            # 特徴点を高精度化
            cv2.cornerSubPix(self.gray_next, self.features, (10, 10), (-1, -1), CRITERIA)

        # 特徴点の最大登録個数をオーバー
        elif len(self.features) >= MAX_FEATURE_NUM:
            print("max feature num over: " + str(MAX_FEATURE_NUM))

        # 特徴点を追加登録
        else:
            # 既存のndarrayの最後に特徴点の座標を追加
            self.features = np.append(self.features, [[[x, y]]], axis = 0).astype(np.float32)
            self.status = np.append(self.status, 1)
            # 特徴点を高精度化
            cv2.cornerSubPix(self.gray_next, self.features, (10, 10), (-1, -1), CRITERIA)


    # 有効な特徴点のみ残す
    def refreshFeatures(self):
        # 特徴点が未登録
        if self.features is None:
            return

        # 全statusをチェックする
        i = 0
        while i < len(self.features):

            # 特徴点として認識できず
            if self.status[i] == 0:
                # 既存のndarrayから削除
                self.features = np.delete(self.features, i, 0)
                self.status = np.delete(self.status, i, 0)
                i -= 1

            i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='feature point tranking')
    parser.add_argument('target', help='Path to video')
    parser.add_argument('output', help='Path to output directory')
    parser.add_argument('--skipframe', '-s', type=int, default=0,
                        help='skip frame rate (default = 5)')
    parser.add_argument('-x', default=256,
                        help='rectangle x size (default = 256)')
    parser.add_argument('-y', default=256,
                        help='rectangle y size (default = 256)')

    args = parser.parse_args()

    Motion(args.target, args.output, args.skipframe, args.x, args.y).run()