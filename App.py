from flask import Flask, render_template, flash, request, session, send_file
from flask import render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import mysql.connector
import sys
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import base64, os

app = Flask(__name__)
app.secret_key = 'a'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/DoctorLogin')
def DoctorLogin():
    return render_template('DoctorLogin.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route('/NewDoctor')
def NewDoctor():
    return render_template('NewDoctor.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctb ")
            data = cur.fetchall()

            return render_template('AdminHome.html', data=data)

        else:
            flash('Username or Password is wrong')
            return render_template('AdminLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctb ")
    data = cur.fetchall()

    return render_template('AdminHome.html', data=data)


@app.route("/AUserInfo")
def AUserInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()
    return render_template('AUserInfo.html', data=data)


@app.route('/ANewModel')
def ANewModel():
    return render_template('ANewModel.html')


@app.route("/newmodel", methods=['GET', 'POST'])
def newmodel():
    if request.method == 'POST':

        name1 = "Admin"
        info = request.form['info']
        file = request.files['file']
        file.save("static/upload/" + file.filename)

        secp_k = generate_key()
        privhex = secp_k.to_hex()
        pubhex = secp_k.public_key.format(True).hex()

        filepath = "./static/upload/" + file.filename
        head, tail = os.path.split(filepath)

        newfilepath1 = './static/Encrypt/' + str(tail)
        newfilepath2 = './static/Decrypt/' + str(tail)

        data = 0
        with open(filepath, "rb") as File:
            data = base64.b64encode(File.read())  # convert binary to string data to read file

        print("Private_key:", privhex, "\nPublic_key:", pubhex, "Type: ", type(privhex))

        if (privhex == 'null'):
            alert = 'Please Choose Another File,file corrupted!'
            return render_template('goback.html', data=alert)

        else:

            print("Binary of the file:", data)
            encrypted_secp = encrypt(pubhex, data)
            print("Encrypted binary:", encrypted_secp)

            with open(newfilepath1, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO  modeltb VALUES ('','" + name1 + "','" + info + "','" + file.filename + "','" + pubhex + "','" + privhex + "')")
            conn.commit()
            conn.close()
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM modeltb where ownerName='" + name1 + "' ")
            data = cur.fetchall()
            return render_template('UploadInfo.html', data=data)


@app.route("/UploadInfo")
def UploadInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM modeltb ")
    data = cur.fetchall()
    return render_template('UploadInfo.html', data=data)


@app.route("/ARequestInfo")
def ARequestInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb  where Status='waiting'")
    data = cur.fetchall()
    return render_template('ARequestInfo.html', data=data)


@app.route('/Accept')
def Accept():
    id = request.args.get('id')
    session['id'] = id

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM requesttb where  id='" + session['id'] + "'  ")
    data = cursor.fetchone()
    if data:
        username = data[1]
        Prikey = data[5]

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM regtb  where  username='" + username + "'  ")
    data = cursor.fetchone()
    if data:
        mail = data[3]
        print(mail)
        sendmail(mail, "Id " + session['id'] + "  Prikey " + str(Prikey))

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute(
        "update  requesttb set status='Accept' where Id='" + session['id'] + "'")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where Status='waiting'")
    data = cur.fetchall()

    return render_template('ARequestInfo.html', data=data)


@app.route("/newofficer", methods=['GET', 'POST'])
def newofficer():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from doctb where username='" + username + "'  ")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO doctb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
            conn.commit()
            conn.close()

            flash('Record Saved!')
            return render_template('DoctorLogin.html')
        else:
            flash('Already Register This  Officer Name!')
            return render_template('NewDoctor.html')


@app.route("/officerlogin", methods=['GET', 'POST'])
def officerlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']
        session['dname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from doctb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('DoctorLogin.html')

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                           database='1federatedlearninglungdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctb where username='" + session['oname'] + "'")
            data1 = cur.fetchall()
            return render_template('DoctorHome.html', data=data1)


@app.route('/DoctorHome')
def DoctorHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctb where username='" + session['dname'] + "'")
    data1 = cur.fetchall()
    return render_template('DoctorHome.html', data=data1)


@app.route('/DRequestInfo')
def DRequestInfo():
    dname = session['dname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + dname + "' ")
    data = cur.fetchall()

    return render_template('DRequestInfo.html', data=data)




@app.route("/searchid")
def searchid():
    user = request.args.get('user')
    id = request.args.get('id')
    session['user'] = user
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute(
        "SELECT  *  FROM apptb where  id='" + str(id) + "'")
    data = cur.fetchall()
    print(data)

    return render_template('DoctAssign.html', data=data)



@app.route("/assigndrug", methods=['GET', 'POST'])
def assigndrug():
    if request.method == 'POST':
        uname = request.form['UserName']
        phone = request.form['Phone']
        email = request.form['Email']
        dname = session['oname']
        medi = request.form['Medicine']
        other = request.form['Other']
        file = request.files['file']
        file.save("static/upload/" + file.filename)
        Adate = request.form['Adate']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  drugtb VALUES ('','" + uname + "','" + phone + "','" + email + "','" + dname + "','" + medi + "','" + other + "','" + file.filename + "','" + Adate + "')")
        conn.commit()
        conn.close()

        # return 'file register successfully'
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
        # cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT * FROM drugtb where DoctorName='" + dname + "' ")
        data = cur.fetchall()

    return render_template('DMedicineInfo.html', data=data)


@app.route("/DMedicineInfo")
def DMedicineInfo():
    dname = session['dname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM drugtb where DoctorName='" + dname + "' ")
    data = cur.fetchall()

    return render_template('DMedicineInfo.html', data=data)


@app.route("/Approved")
def Approved():
    id = request.args.get('lid')
    email = request.args.get('email')
    mob = request.args.get('mob')
    import random
    loginkey = random.randint(1111, 9999)
    message = "Your Defense  Login Key :" + str(loginkey)

    sendmail(email, message)
    sendmsg(mob, message)

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute("Update regtb set Status='Active',LoginKey='" + str(loginkey) + "' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status !='waiting'")
    data1 = cur.fetchall()

    return render_template('OUserInfo.html', data=data, data1=data1)


@app.route("/Reject")
def Reject():
    id = request.args.get('lid')
    email = request.args.get('email')

    message = "Your Request  Rejected"

    sendmail(email, message)

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute("Update regtb set Status='reject' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status !='waiting'")
    data1 = cur.fetchall()

    return render_template('OUserInfo.html', data=data, data1=data1)


@app.route('/OActivityInfo')
def OActivityInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM activitytb ORDER BY id ")
    data1 = cur.fetchall()
    return render_template('OActivityInfo.html', data=data1)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "'  ")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO regtb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + address + "','" +
                username + "','" + password + "')")
            conn.commit()
            conn.close()

            flash('Record Saved!')

            return render_template('NewUser.html')
        else:
            flash('Already Register This  UserName!')
            return render_template('NewUser.html')


@app.route("/Download")
def Download():
    fid = request.args.get('lid')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  filetb where  id='" + fid + "'")
    data = cursor.fetchone()
    if data:

        fname = data[3]

    else:
        return 'Incorrect username / password !'

    filepath = "./static/upload/" + fname

    return send_file(filepath, as_attachment=True)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']

        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                           database='1federatedlearninglungdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "'")
            data1 = cur.fetchall()
            flash('Login Successfully')
            return render_template('UserHome.html', data=data1)


@app.route('/UserHome')
def UserHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where OwnerName='" + session['uname'] + "'")
    data1 = cur.fetchall()
    return render_template('UserHome.html', data=data1)


@app.route("/Model", methods=['GET', 'POST'])
def Model():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM modeltb ")
    data = cur.fetchall()
    return render_template('Model.html', data=data)


@app.route('/SendRequest')
def SendRequest():
    id = request.args.get('id')
    session['id'] = id

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM modeltb where  id='" + session['id'] + "'  ")
    data = cursor.fetchone()

    if data:
        Ownername = data[1]
        type = data[2]
        Model = data[3]
        Privkey = data[5]

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO  requesttb VALUES ('','" + session[
            'uname'] + "','" + Ownername + "','" + type + "','" + Model + "','" + Privkey + "','waiting')")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where UserName='" + session['uname'] + "' ")
    data = cur.fetchall()

    return render_template('URequestInfo.html', data=data)


@app.route("/URequestInfo", methods=['GET', 'POST'])
def URequestInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where UserName='" + session['uname'] + "' ")
    data = cur.fetchall()
    return render_template('URequestInfo.html', data=data)


@app.route('/Decrypt')
def Decrypt():
    id = request.args.get('id')
    session['id'] = id
    st = request.args.get('st')

    if st == "Accept":
        return render_template('Decrypt.html')
    else:
        data1 = 'Waiting For  Owner Approved! '
        return render_template('goback.html', data=data1)


@app.route("/decryt", methods=['GET', 'POST'])
def decryt():
    if request.method == 'POST':

        keys = request.form['keys']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM requesttb where  id='" + session['id'] + "' and PriKey='" + keys + "' ")
        data = cursor.fetchone()

        if data:
            typ = data[3]
            prkey = data[5]
            fname = data[4]
            session['oname'] = data[2]

            privhex = prkey

            filepath = "./static/Encrypt/" + fname
            head, tail = os.path.split(filepath)

            newfilepath1 = './static/Encrypt/' + str(tail)
            newfilepath2 = './static/Decrypt/' + str(tail)

            data = 0
            with open(newfilepath1, "rb") as File:
                data = base64.b64decode(File.read())

            print(data)
            decrypted_secp = decrypt(privhex, data)
            print("\nDecrypted:", decrypted_secp)
            with open(newfilepath2, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

            return render_template('Predict.html', model=typ)
        else:

            data1 = 'Key Incorrect! '
            return render_template('goback.html', data=data1)


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        username = session['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' ")
        data = cursor.fetchone()
        if data is None:

            data1 = 'Username or Password is Incorrect!'
            return render_template('goback.html', data=data1)



        else:
            print(data[0])
            session['uid'] = data[0]
            mob = data[4]
            email = data[3]

        if "Lung" == "Lung":
            import tensorflow as tf
            import cv2
            import numpy as np
            from keras.preprocessing import image

            file = request.files['file']
            file.save('static/upload/Test.png')
            fname = 'static/upload/Test.png'
            img1 = cv2.imread('static/upload/Test.png')
            dst = cv2.fastNlMeansDenoisingColored(img1, None, 10, 10, 7, 21)
            noi = 'static/upload/noi.png'

            cv2.imwrite(noi, dst)

            import warnings
            warnings.filterwarnings('ignore')

            classifierLoad = tf.keras.models.load_model('lungmodel.h5')
            test_image = image.load_img('static/upload/Test.png', target_size=(200, 200))
            test_image = np.expand_dims(test_image, axis=0)
            result = classifierLoad.predict(test_image)
            print(result)
            ind = np.argmax(result)
            out = ''

            if ind == 0:
                out = 'Covid'
                session['Ans'] = 'yes'
            elif ind == 1:
                out = 'Influenza'
                session['Ans'] = 'yes'
            elif ind == 2:
                out = 'Normal'
                session['Ans'] = 'No'
            elif ind == 3:
                out = 'Pneumonia'
                session['Ans'] = 'yes'
            elif ind == 4:
                out = 'Tuberculosis'
                session['Ans'] = 'yes'

            if session['Ans'] == 'yes':
                sendmail(email, "You Have " + out + "Appointment Today")

            session['out'] = out

            return render_template('Answer.html', data=out, org=fname)


@app.route("/ViewDoctor", methods=['GET', 'POST'])
def ViewDoctor():
    if session['Ans'] == 'yes':
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')

        cur = conn.cursor()
        cur.execute("SELECT * FROM doctb")
        data = cur.fetchall()

        return render_template('UserAppointment.html', data=data)
    else:
        data1 = 'Your Are Normal!'
        return render_template('goback.html', data=data1)


@app.route("/UMedicineInfo")
def UMedicineInfo():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  drugtb where UserName='" + uname + "'  ")
    data = cur.fetchall()

    return render_template('UMedicineInfo.html', data=data)


@app.route("/Appointment")
def Appointment():
    dusername = request.args.get('id')
    import datetime
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    uname = session['uname']
    dise = session['out']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  doctb where  UserNAme='" + dusername + "'")
    data = cursor.fetchone()

    if data:
        spec = data[5]



    else:

        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM regtb where  UserNAme='" + uname + "'")
    data = cursor.fetchone()

    if data:
        mobile = data[2]
        email = data[3]


    else:

        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO  apptb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + dusername + "','" + date + "','" + spec + "','" + dise + "')")
    conn.commit()
    conn.close()

    flash("Record Saved")
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  drugtb where UserName='" + uname + "'  ")
    data = cur.fetchall()

    return render_template('UMedicineInfo.html', data=data)


@app.route('/download')
def download():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1federatedlearninglungdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM drugtb where  id = '" + str(id) + "'")
    data = cursor.fetchone()
    if data:
        filename = "static\\upload\\" + data[7]

        return send_file(filename, as_attachment=True)

    else:
        return 'Incorrect username / password !'


def sendmail(Mailid, message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "kkvz xxke jmeb pcyb")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, port=5000)
    app.run(debug=True, use_reloader=True)
