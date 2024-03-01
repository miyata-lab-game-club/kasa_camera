import cv2
import cv2.aruco as aruco
import numpy as np
import math

# パラメータ
H_LOW = 30   # Hの下限
H_HIGH = 90 # Hの上限
S_LOW = 100 # Sの下限
S_HIGH = 250
V_LOW = 75  # Vの下限
V_HIGH = 255
RADIUS_LOW = 10 # 外接円の半径の下限

# カメラからの画像取得
cap = cv2.VideoCapture(0)

# マーカー種類を呼び出し
dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)

# 基準マーカと赤色の点の座標を初期化
ref_marker_coords = None
red_point_coords = None

while True:
    ret, frame = cap.read()
    framecopy = frame.copy()
    if not ret:
        continue

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # HSVに変換
    mask = cv2.inRange(img_hsv, (H_LOW, S_LOW, V_LOW),
                       (H_HIGH, S_HIGH, V_HIGH)) # オレンジ領域の2値画像

    conts = cv2.findContours(mask, cv2.RETR_EXTERNAL, 
                            cv2.CHAIN_APPROX_SIMPLE)[1] # 全輪郭線

    for cnt in conts: # 各輪郭線についての処理
        # cnt の外接円の中心 (rx, ry)と半径 radius
        (rx, ry), radius = cv2.minEnclosingCircle(cnt)
        if radius > RADIUS_LOW:
            # 外接円の半径がRADIUS_LOWよりも大きいとき
            # 重心 cx, cy を計算
            M=cv2.moments(cnt)
            if M['m00'] > 0:
                cx=int(M['m10'] / M['m00'])
                cy=int(M['m01'] / M['m00'])
                cv2.circle(frame, (cx, cy), int(radius * 0.3),
                        (0, 0, 255), -1)
                
                red_point_coords = (cx, cy)

    # マーカーの検出
    corners, ids, _ = aruco.detectMarkers(framecopy, dict_aruco)

    if ids is not None:
        # 基準マーカー0の座標
        ref_index = np.where(ids == 0)[0]
        if len(ref_index) > 0:
            ref_corners = corners[ref_index[0]][0]
            x1 = ref_corners[0][0]
            y1 = ref_corners[0][1]

            # 基準マーカーの座標を更新
            ref_marker_coords = (x1, y1)
            
            angles = []
            # マーカー1以降の相対座標を取得
            for i in range(len(ids)):
                if ids[i] != 0:
                    relative_corners = corners[i][0] - red_point_coords
                    #print(ids[i], relative_corners[0])
                    x2 = relative_corners[0][0]
                    y2 = relative_corners[0][1]

                    # 赤色の点と基準マーカの角度を算出
                    angle_to_ref = math.atan2(y1 - red_point_coords[1], x1 - red_point_coords[0]) * 180 / math.pi
                    angle_to_marker = math.atan2(y2, x2) * 180 / math.pi
                    angle = angle_to_marker - angle_to_ref
                    print('id: ' + str(i) + ', angle: ' + str(angle))
                    if angle<0:
                        angle = angle + 360
                    angles.append(angle)

            # 角度の平均を計算
            if angles:
                mean_angle = sum(angles) / len(angles)
                print('角度の平均： ' , mean_angle)

                    #distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                    #distance = math.sqrt((x1 - cx)**2 + (y1 - cy)**2)
                    #x3 = x1-x2
                    #y3 = y1-y2
                    #tan = y3/x3
                    #atan = np.arctan(tan)*180/math.pi
                    #print("距離：" + str(distance))

            # マーカーを描画
            aruco.drawDetectedMarkers(frame, corners)

    cv2.imshow("detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
