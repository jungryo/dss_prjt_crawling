from flask import Flask, request, Response 
import libs.path as path
import libs.matzip as matzip
import libs.slack as slack
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('/home/ubuntu/aws.ini')
datas = config["matzip_crawling"]
naver_id= datas["naver_id"]
naver_secret = datas["naver_secret"]
odsay_key = datas["odsay_key"]
webhook_url = 'https://hooks.slack.com/services/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'

@app.route("/")
def index():
    return "server is running!"

@app.route("/bot", methods=['POST'])
def bot():
    username = request.form.get('user_name') 
    token = request.form.get('token')
    text = request.form.get('text')
    
    print(username, token, text)
    
    # 문장 형식이 맞는지 확인
    text = text.replace("matzip!", "")
    if len(text.split("/")) != 4:
        slack.send_msg(webhook_url, "'주소1/주소2/교통수단/음식카테고리' 포멧으로 입력해주세요.")
        slack.send_msg(webhook_url,"교통수단: 자동차 / 대중교통")
        slack.send_msg(webhook_url,"음식카테고리: 한식/양식/디저트/일식/바/중식/분식/동남아식/뷔페/기타")
        return Response(), 200
    
    splited_text = text.split("/")
    # 명령 문자열에 따라서 코드 실행
    d1_address, d2_address, by, category = splited_text[0], splited_text[1], splited_text[2],  splited_text[3]
    ranking = matzip.find_matzip(by, category, d1_address, d2_address, naver_id, naver_secret, odsay_key)
    slack.send_msg(webhook_url, "{}경로 내 {}맛집 당장만나 별점 top{}".format(by, category, len(ranking.index)))
    for i in range(len(ranking.index)):
        slack.send_msg(webhook_url, "{}위: {}, {}점, {}".format(i+1, ranking.iloc[i,0], ranking.iloc[i,6], ranking.iloc[i,2]))    
    
    return Response(), 200
    
app.run(debug=True)
