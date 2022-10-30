from flask import Flask, render_template, request
import json
import hh_query as hh
import habr_news as habr
news_url = habr.get_news()
hh_urls = []
# print(hh_urls)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

def top(json_file):
    with open(json_file, 'r') as f:
        result = json.load(f)
    json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    return result[:10]


@app.route("/topPY/")
def top_py():
    return render_template('top.html', data=top('py_stat.json'))

@app.route("/topJava/")
def top_java():
    return render_template('top.html', data=top('java_stat.json'))

@app.route("/habr/", endpoint="habr_news")
def habr_news():
    try:
        new = int(request.args.get('new'))
    except:
        new = 1
    nums = len(news_url)
    habr_new = habr.read_new(news_url, new-1)
    # print(habr_new['text'])
    return render_template('habr_news.html', data=habr_new, num=new, nums=nums)



@app.route('/about/', methods=['GET'])
def contacts():
    return render_template('about.html')

@app.route('/about/', methods=['POST'])
def contacts_post():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    print(name , email , subject , message)
    # TO DO данные отправляем в базу
    return render_template('about.html')


@app.route('/HH/', methods=['GET'])
def hh_get():
    return render_template('HH.html')

@app.route('/HH_result/', methods=['GET'])
def hh_result_get():
    global hh_urls
    try:
        num = int(request.args.get('vacancy'))
    except:
        num = 1
    nums = len(hh_urls)
    hh_url = hh.read_url(hh_urls[num-1])
    return render_template('HH_result.html', data=hh_url, num=num, nums=nums)

@app.route('/HH_result/', methods=['POST'])
def hh_post():
    global hh_urls
    try:
        page = int(request.form.get('page' ))
        area = int(request.form.get('area'))
        search = request.form.get('key')
    except:
        return render_template('HH.html')


    hh_urls = hh.getUrls(search, area, page )
    hh_url = hh.read_url(hh_urls[0])
    # print(hh_url)
    nums = len(hh_urls)
    return render_template('HH_result.html', data=hh_url, num=1, nums=nums)


if __name__ == "__main__":
    app.run(debug=True)