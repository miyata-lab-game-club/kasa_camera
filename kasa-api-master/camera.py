import cv2
import cv2.aruco as aruco
import numpy as np
import time

#for i in range(100):
#    cap1 = cv2.VideoCapture(i,  cv2.CAP_DSHOW)
#    if cap1.isOpened():
#        print("Video ", i)
# カメラからの画像取得
cap = cv2.VideoCapture(0)

# マーカーの角度と座標を格納する配列
marker_data = []
prev_time = time.time()

# グローバル変数の定義
global_avg_angle = 0

while True:
    # キャプチャを読み込む
    ret, frame = cap.read()

    key = cv2.waitKey(1)

    # マーカー種類を呼び出し
    dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

    # マーカーの検出
    corners, ids, _ = aruco.detectMarkers(frame, dict_aruco)

    if ids is not None:
        marker_data = []

        for i in range(len(ids)):
            # マーカーの0番目の角と2番目の角にあたるコーナー座標を取得
            corner1 = corners[i][0][0]
            corner2 = corners[i][0][2]
            x1, y1 = corner1[0], corner1[1]
            x2, y2 = corner2[0], corner2[1]

            # 0番目と2番目のコーナーの変化量
            varx = x1 - x2
            vary = y1 - y2

            # 角度と座標を保存
            angle = np.degrees(np.arctan2(vary, varx))
            marker_data.append({
                "id": ids[i],
                "angle": angle + 135,
                "x": (x1 + x2) / 2,
                "y": (y1 + y2) / 2
            })

        now = time.time()

        # 5秒ごとに表示
        # if now - prev_time >= 5:
        #     for data in marker_data:
        #         print("マーカー" + str(data['id']) + ": (" + str(data['x']) + ", " + str(data['y']) + ")")
        #     prev_time = now

        # 平均角度をファイルに書き込む関数
        def write_avg_angle_to_file(avg_angle):
            with open("angle_data.txt", "w") as file:
                file.write(str(avg_angle))

        # 角度の平均を計算
        angles = [data['angle'] for data in marker_data]
        if len(angles) > 0:
            global_avg_angle = np.mean(angles)  # グローバル変数を更新
            write_avg_angle_to_file(global_avg_angle)  # ファイルに書き込む
            print("角度の平均: " + str(global_avg_angle))

    # 描画
    if corners is not None and len(corners) > 0:
        aruco.drawDetectedMarkers(frame, corners, ids)

    # 画面表示
    cv2.imshow('detection', frame)

    # qを押すとbreak
    if key == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
