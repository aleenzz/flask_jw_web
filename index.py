#coding:utf-8
from flask import Flask, request, render_template, redirect, url_for
import time
import requests
from lxml import etree


app = Flask(__name__)

kes = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', says=kes)

    else:
        del kes[:]
        name = request.form.get("say_user")
        password = request.form.get("say_pass")
        login_session = requests.Session()
        headers = {
            'User-agent': 'Mozilla/5.0 (x11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0',
            'Referer': 'http://newjw.cduestc.cn/',
            'Host': 'newjw.cduestc.cn'
        }
        data = {
            'zjh': name,
            'mm': password
        }
        url = "http://newjw.cduestc.cn/loginAction.do"
        response = login_session.post(url, data=data, headers=headers)
        if "menu/s_top.jsp" not in response.text:
            return redirect(url_for('index'))
        lookscore = login_session.get('http://newjw.cduestc.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=3423')
        html = etree.HTML(lookscore.text)
        names = html.xpath('//*[@id="user"]')[0]
        trs = names.xpath(".//tr")[1:]
        # etree.tostring
        for tr in trs:
            ke = tr.xpath('./td[3]/text()')[0].strip()
            score = tr.xpath('./td[7]/p/text()')[0].strip()
            if score >="60":
                ke_pass = "YES"
            else:
                ke_pass = "x"

            kes.append({"ke": ke,
                          "score":score,
                          "ke_pass":ke_pass})
        
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, )