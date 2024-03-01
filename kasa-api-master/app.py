from flask import Flask, jsonify
import os

app = Flask(__name__)

def read_avg_angle_from_file():
    if os.path.exists("angle_data.txt"):
        with open("angle_data.txt", "r") as file:
            data = file.read()
            try:
                # 文字列をfloatに変換
                return float(data)
            except ValueError:
                # ファイルに有効な数値がない場合は0を返す
                return 0.0
    else:
        return 0.0

@app.route('/get_average_angle', methods=['GET'])
def get_average_angle():
    avg_angle = read_avg_angle_from_file()
    # float型の値をそのままJSONに変換
    return jsonify({"average_angle": avg_angle})

if __name__ == '__main__':
    app.run(debug=True)
