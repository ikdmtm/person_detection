import os
from pathlib import Path
import datetime
import requests
from PIL import Image
import base64

#detectディレクトリの中身を取得
detect_path = './runs/detect'
#最新のpredictを取得
detect_files = sorted(Path(detect_path).iterdir(), key=os.path.getmtime)
print(detect_files)
print(detect_files[-1])

# 画像が保存されているディレクトリ
images_path = f'./{detect_files[-1]}/crops/person'

# slackにpostする関数
def post_to_slack(message, img, filename):
    # params
    SLACK_TOKEN = 'API key'
    CHANNEL_ID = 'ID'
    data = {'token': SLACK_TOKEN, 'channels': CHANNEL_ID, 'initial_comment': message, 'filename': filename}
    files = {'file': open(img, 'rb')}

    # send
    requests.post('https://slack.com/api/files.upload', data=data, files=files)
# initial commentで日付、filenameに出退勤と時間を記述
# 複数枚に対応する、とりあえず個別で

def post_to_webapp(date0, date1, img_file0, img_file1):
    # POSTリクエストを送信するURLを設定します。Railsアプリのエンドポイントに置き換え
    url = 'http://localhost:3000/cards'

    file_paths = [img_file0, img_file1]  # それぞれのファイルへのパスを含むリスト

    with open(file_paths[0], 'rb') as f:
        image0 = f.read()
    encode0=base64.b64encode(image0)
    
    with open(file_paths[1], 'rb') as f:
        image1 = f.read()
    encode1=base64.b64encode(image1)


    # 送信するデータを辞書として定義
    data = {
        'arrival_time': '2024-01-17T12:00:00Z',  # arrival_timeを適切なデータに置き換え
        'departure_time': '2024-01-17T14:00:00Z',  # departure_timeを適切なデータに置き換え
        'arrival_image': encode0,  # 画像データをリストで指定
        'departure_image': encode1
    }

    # POSTリクエストを送信
    response = requests.post(
        url,
        data = data,
        # files = files,
        # headers = headers
        )

    # レスポンスを取得して処理
    print('ステータスコード:', response.status_code)


# 画像が存在する場合、作成順で取得
if list(Path(images_path).glob("*")):
    files = sorted(Path(images_path).iterdir(), key=os.path.getmtime)
    epoch0 = os.path.getctime(files[0])
    date0 = datetime.datetime.fromtimestamp(epoch0).strftime("%Y/%m/%d %H:%M:%S") #日時をフォーマット
    epoch1 = os.path.getctime(files[-1])
    date1 = datetime.datetime.fromtimestamp(epoch1).strftime("%Y/%m/%d %H:%M:%S")
    print('出勤', files[0], date0, '退勤', files[-1], date1)
    #f = open('write.txt', 'a')
    #f.write(f'{detect_files[-1]}\n going_to_work: {files[0]}, leaving_work: {files[-1]}\n')
    f.close()

    # ここで画像をSlackに投稿
    abs_path0 = os.path.abspath(files[0]) #絶対パスを取得
    abs_path1 = os.path.abspath(files[-1])
    filename0 = "出勤"
    filename1 = "退勤"
    # post_to_slack(date0, f'{abs_path0}', filename0)
    # post_to_slack(date1, f'{abs_path1}', filename1)
    post_to_webapp(date0, date1, f'{abs_path0}', f'{abs_path1}')

else:
    # 画像が存在しない場合
    print('出勤', 'なし', '退勤', 'なし')
    #f = open('write.txt', 'a')
    #f.write(f'{detect_files[-1]}\n going_to_work: none, leaving_work: none\n')
    f.close()