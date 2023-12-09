import os
from pathlib import Path
import datetime
import requests

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
    SLACK_TOKEN = 'xoxb-5572523844211-5589900450967-9pCVMkofWRSMNjZG7PcMaNA8'
    CHANNEL_ID = 'C05GUFKB0RZ'
    data = {'token': SLACK_TOKEN, 'channels': CHANNEL_ID, 'initial_comment': message, 'filename': filename}
    files = {'file': open(img, 'rb')}

    # send
    requests.post('https://slack.com/api/files.upload', data=data, files=files)
# initial commentで日付、filenameに出退勤と時間を記述
# 複数枚に対応する、とりあえず個別で

def post_to_webapp():
    # POSTリクエストを送信するURLを設定します。Railsアプリのエンドポイントに置き換え
    url = 'http://example.com/rails_endpoint'

    # 送信するデータを辞書として定義
    data = {
        'key1': 'value1',
        'key2': 'value2',
    }

    # POSTリクエストを送信
    response = requests.post(url, data=data)

    # レスポンスを取得して処理
    if response.status_code == 200:
        # リクエストが成功した場合の処理
        print('POSTリクエストが成功しました。')
        print('レスポンス:', response.text)
    else:
        # リクエストが失敗した場合の処理
        print('POSTリクエストが失敗しました。')
        print('エラーコード:', response.status_code)


# 画像が存在する場合、作成順で取得
if list(Path(images_path).glob("*")):
    files = sorted(Path(images_path).iterdir(), key=os.path.getmtime)
    epoch0 = os.path.getctime(files[0])
    date0 = datetime.datetime.fromtimestamp(epoch0).strftime("%Y/%m/%d %H:%M:%S") #日時をフォーマット
    epoch1 = os.path.getctime(files[-1])
    date1 = datetime.datetime.fromtimestamp(epoch1).strftime("%Y/%m/%d %H:%M:%S")
    print('出勤', files[0], date0, '退勤', files[-1], date1)
    f = open('write.txt', 'a')
    f.write(f'{detect_files[-1]}\n going_to_work: {files[0]}, leaving_work: {files[-1]}\n')
    f.close()

    # ここで画像をSlackに投稿
    abs_path0 = os.path.abspath(files[0]) #絶対パスを取得
    abs_path1 = os.path.abspath(files[-1])
    filename0 = "出勤"
    filename1 = "退勤"
    post_to_slack(date0, f'{abs_path0}', filename0)
    post_to_slack(date1, f'{abs_path1}', filename1)
else:
    # 画像が存在しない場合
    print('出勤', 'なし', '退勤', 'なし')
    f = open('write.txt', 'a')
    f.write(f'{detect_files[-1]}\n going_to_work: none, leaving_work: none\n')
    f.close()