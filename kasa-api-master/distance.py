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
    if not ret:
        continue

    # マーカーの検出
    corners, ids, _ = aruco.detectMarkers(frame, dict_aruco)

    if ids is not None:
        # 基準マーカー0の座標
        ref_index = np.where(ids == 0)[0]
        if len(ref_index) > 0:
            ref_corners = corners[ref_index[0]][0]
            x1 = ref_corners[0][0]
            y1 = ref_corners[0][1]
            
            # マーカー1以降の相対座標を取得
            for i in range(len(ids)):
                if ids[i] != 0:
                    relative_corners = corners[i][0] - ref_corners
                    #print(ids[i], relative_corners[0])
                    x2 = relative_corners[0][0]
                    y2 = relative_corners[0][1]
                    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                    print(distance)

            # マーカーを描画
            aruco.drawDetectedMarkers(frame, corners)

    cv2.imshow("detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()