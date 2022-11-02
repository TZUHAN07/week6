
from flask import Flask, request, render_template, session, redirect, url_for, make_response
# 載入Flask,Request 物件, render_template 函式,session,redirect函式
import mysql.connector
from mysql.connector import pooling


# 建立Application 物件，可以設定靜態檔案的路徑處理
app = Flask(__name__, static_folder="static", static_url_path="/")
# 靜態檔案的資料價名稱 , 靜態檔案對應的網址路徑
app.secret_key = "any string but secret"  # 設定sessin的密鑰
# 連接 MySQL 資料庫
mydb = mysql.connector.connect(
    host="localhost",    # 主機名稱
    user="root",         # 帳號
    password="j610114*",  # 密碼
    database='website'   # 資料庫名稱
)


@app.route("/", methods=['GET'])
def firstpage():  # 用來回應網站首頁函式

    return render_template("firstpage.html")


@app.route("/member")  # 建立/member對應的處理函式
def sucessful():

    # check if the users exist or not
    if not session.get("name"):
        return redirect("/")
    name = session["name"]
    print(name)
    return render_template("member.html", name=session["name"])


@app.route("/error")  # 建立/error對應的處理函式
def geterror():
    message = request.args['message']
    return render_template("error.html", message=message)


@app.route("/signup", methods=["POST"])  # 建立註冊頁對應的處理函式
def signup():
    message = ''
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    try:
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT * FROM member WHERE username = %s ", (username,))
        account = mycursor.fetchone()
        if account:
            message = "帳號已經被註冊"
            return redirect(url_for("geterror", message=message))
        else:
            insert_data = (
                "INSERT INTO member (name, username,password) VALUES (%s,%s,%s)")
            val = (name, username, password)
            mycursor.execute(insert_data, val)  # 執行sql語句
            mydb.commit()  # 提交至數據庫執行
            return render_template("firstpage.html")
    except:
        print("Unexpected Error")
    finally:
        mycursor.close()
        mydb.close()


@app.route("/signin", methods=["POST", "GET"])
def signin():  # 用來進⾏驗證的函式
    username = request.form["username"]
    password = request.form["password"]
    try:
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT * FROM member WHERE username = %s AND password =%s", (username, password))
        account = mycursor.fetchone()
        if account:
            # session.permanent = True  # 若未登出 下次登入直接是登入狀態
            session["id"] = account[0]
            session["name"] = account[1]
            session["username"] = account[2]
            session["password"] = account[3]
            # mycursor.close()
            print("good")
            return redirect(url_for("sucessful"))
        else:
            return redirect(url_for("geterror", message="帳號、或密碼輸入錯誤"))
    except:
        print("Unexpected Error")
    finally:
        mycursor.close()
        mydb.close()


@app.route("/signout", methods=["GET"])
def signout():  # 用來進⾏登出的函式
    session.pop("id", None)
    session.pop("name", None)
    session.pop("username", None)
    session.pop("password", None)
    # session.clear()
    return redirect(url_for("firstpage"))


@app.route("/message", methods=["post"])
def message():
    message = request.form["message"]
    id = session["id"]  # 存放在 cookie 的 id
    try:
        insert_data = (
            "INSERT INTO message(member_id, content) VALUES (%s, %s)")
        val = (id, message)
        mycursor = mydb.cursor()
        mycursor.execute(insert_data, val)
        mydb.commit()

        mycursor.execute(
            "SELECT member.name,message.content FROM member INNER JOIN message ON member.id =message. member_id")
        content = mycursor.fetchall()
        print(content)
        for data in content:
            name = content[data][0]
            eachContent = content[data][1]
        print(name, eachContent)
        return render_template("member.html", name=name, message=eachContent)

    except:
        print("Unexpected Error")
    finally:
        mycursor.close()
        mydb.close()


# 啟動網站伺服器，可透過post參數指定埠號
app.run(port=3000, debug=True)
