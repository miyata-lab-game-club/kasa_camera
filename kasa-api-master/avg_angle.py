import cv2
import cv2.aruco as aruco
import numpy as np
import math

# カメラからの画像取得
cap = cv2.VideoCapture(0)

# マーカー種類を呼び出し
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)

while True:
    ret, frame = cap.read()
    framecopy = frame.copy()
    if not ret:
        continue

    # マーカーの検出
    corners, ids, _ = aruco.detectMarkers(framecopy, dict_aruco)

    if ids is not None:
        # 基準マーカー0の座標
        #ref_index = np.where(ids == 0)[0][0]
        #ref_corners = corners[ref_index][0]
        ## 基準マーカーの対角戦の角度を計算
        #angle_rad = np.arctan2(ref_corners[2][1] - ref_corners[0][1], ref_corners[2][0] - ref_corners[0][0])
        #ref_angle_deg = np.degrees(angle_rad)
#
        # 角度のリスト
        angles = []

        # 他のマーカーの角度の合計(基準マーカーからみた角度)
        for i, marker_id in enumerate(ids):
            # 基準マーカーでないとき
            if marker_id != 0:
                corners_n0 = corners[i][0]
                # 他のマーカーの角度を求める
                ang_rad = np.arctan2(corners_n0[2][1] - corners_n0[0][1], corners_n0[2][0] - corners_n0[0][0])
                ang_deg = np.degrees(ang_rad)
                #ang_deg = (ang_deg + 360) % 360
                angles.append(ang_deg)

        # 角度をテキストファイルに書き込み
        def write_avg_angle_to_file(avg_angle):
            with open("angle_data.txt", "w") as file:
                file.write(str(avg_angle))

        # 角度の平均を計算
        if angles:
            avg_ang = np.mean(angles)
            #print('角度の平均: ' + str(avg_ang - ref_angle_deg))
            print('他: ' + str(avg_ang))
            write_avg_angle_to_file(avg_ang)  # ファイルに書き込む

    # マーカーを描画
    frame = aruco.drawDetectedMarkers(frame, corners)

    cv2.imshow("detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
