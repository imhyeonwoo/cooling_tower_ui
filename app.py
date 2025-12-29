from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Cooling Tower Monitor</h1><p>서버가 정상 작동 중입니다!</p>'

if __name__ == '__main__':
    # 외부에서 접속 가능하도록 0.0.0.0으로 설정
    app.run(host='0.0.0.0', port=5000, debug=True)
