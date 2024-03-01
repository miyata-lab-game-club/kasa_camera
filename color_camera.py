import cv2
import cv2.aruco as aruco
import numpy as np
import time
import math

# 色検出のためのパラメータ
H_LOW = 150
H_HIGH = 179
S_LOW = 64
S_HIGH = 255
V_LOW = 0
V_HIGH = 255

# 検出する色の半径の下限の値
RAD_LOW = 10

# カメラ番号を取得
for i in range(100):
    cap1 = cv2.VideoCapture(i,  cv2.CAP_DSHOW)
    if cap1.isOpened():
        print("Video ", i)
# カメラからの画像取得
cap = cv2.VideoCapture(0)

# マーカー種類を呼び出し
dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    bgr_timg = frame.copy()

    # HSVに変換
    #img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # オレンジ色の閾値のマスク画像
    #img_mask = cv2.inRange(img_hsv, (H_LOW, S_LOW, V_LOW), (H_HIGH, S_HIGH, V_HIGH))

     # 二値化
    imgray = cv2.cvtColor(bgr_timg, cv2.COLOR_BGR2GRAY)
    imgray = cv2.bitwise_not(imgray)
    ret,thresh = cv2.threshold(imgray, 0, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    yl, xl = np.where(thresh == 255)

    # 白色領域を取得
    yl, xl = np.where(thresh==255)

    # 座標データ形式に変換
    yl = yl.reshape((-1, 1))
    xl = xl.reshape((-1, 1))
    vec = np.hstack((xl, yl))

    # 凸包処理
    hull = cv2.convexHull(vec)

    # 結果描画
    result_img = cv2.drawContours(bgr_timg,[hull],
                0,(0,0,255),2)
    
    cv2.imshow("totuho", result_img)

    # 輪郭領域を取得
    #contours  = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    ## 輪郭領域について
    #for contour in contours:
    #    # 外接円の中心と半径
    #    #(rx, ry), radius = cv2.minEnclosingCircle(contour)
    #    hull = cv2.convexHull(contour)
    #    if radius < RAD_LOW:
    #        # 重心を計算
    #        M = cv2.moments(contour)
    #        if M['m00'] > 0:
    #            cx = int(M['m10']) / int(M['m00'])
    #            cy = int(M['m01']) / int(M['m00'])
    #            # 重心を描画
    #            cv2.circle(frame, (cx, cy), int(radius*0.3), (0,0,255), -1)
    # マーカの検出
    corners, ids, _ = aruco.detectMarkers(frame, dict_aruco)

    # マーカが検出されたとき実行
    if ids is not None:
        # 基準マーカ0の座標
        ref_index = np.where(ids==0)[0]
        if len(ref_index) > 0:
            ref_contours = contours[ref_index[0]][0]
            x1 = ref_contours[0][0]
            y1 = ref_contours[0][1]

            # マーカ1以降の相対座標を取得
            for i in range(lem(ids)):
                if ids[i] != 0:
                    relative_corners = corners[i][0] - ref_contou
                    x2 = relative_corners[0][0]
                    y2 = relative_corners[0][1]
                    # 距離を算出
                    distance = math.sqrt((x1-cx)**2 + (y1-cy)**2)

                    x3 = x1-x2
                    y3 = y1-y2
                    tan = y3/x3
                    # 角度を算出
                    atan = np.arctan(tan*180)/math.pi

                    print('距離: '+distance+' ,角度: '+atan)

            # マーカを描画
            aruco.drawDetectedMarkers(frame, corners)

    # 画面表示
    cv2.imshow("detection", frame)
    if cv2.waitKey(1) & 0xFF == ord(('q')):
        break

cap.release()
cv2.destroyAllWindows()


                

                    

