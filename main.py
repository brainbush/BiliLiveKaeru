import flask
import requests
from flask import request, render_template

app = flask.Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return app.send_static_file("index.html")
    elif request.method == "POST":
        content = request.json
        ua = request.headers.get("User-Agent")
        plain_cookies = content.get("cookies")
        try:
            cookies = dict(p.split("=") for p in plain_cookies.split("; "))
        except ValueError:
            return flask.jsonify({})
        post_data = dict(
            room_id=content.get("room_id"),
            platform="pc",
            area_v2=content.get("area_v2"),
            csrf_token=cookies.get("bili_jct"),
            csrf=cookies.get("bili_jct"),
        )
        headers = {
            "User-Agent": ua,
            # "origin": "https://link.bilibili.com",
            # "referrer": "https://link.bilibili.com/p/center/index",
        }
        print(headers)
        print(post_data)
        r = requests.post(
            "https://api.live.bilibili.com/room/v1/Room/startLive",
            headers=headers,
            data=post_data,
            cookies=cookies,
        )
        return flask.jsonify(r.json())


@app.route("/scan", methods=["GET", "POST"])
def login():
    ua = request.headers.get("User-Agent")
    headers = {"User-Agent": ua}

    if request.method == "GET":
        r = requests.get(
            "https://passport.bilibili.com/qrcode/getLoginUrl", headers=headers
        )
        return flask.jsonify(r.json())
    elif request.method == "POST":
        oauthKey = request.json.get("oauthKey")
        s = requests.session()
        r = s.post(
            "https://passport.bilibili.com/qrcode/getLoginInfo",
            headers=headers,
            data=dict(oauthKey=oauthKey),
        ).json()
        if r.get("status") == True:
            c = s.cookies
            f = ["%s=%s" % (name, value) for (name, value) in c.items()]
            cookies = "; ".join(f)
            r["cookies"] = cookies
        return flask.jsonify(r)


@app.route("/area_list", methods=["GET"])
def get_area_list():
    r = requests.get("https://api.live.bilibili.com/room/v1/Area/getList").json()
    return flask.jsonify(r.get("data"))


if __name__ == "__main__":
    app.run()