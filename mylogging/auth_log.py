import datetime

def login_auth(userlogin):
    file = open('auth.log', 'a')
    message = " " + "user\t" + userlogin + "\tlogged in "
    time = datetime.datetime.now()
    log = time.strftime("%Y-%m-%d %H:%M:%S\t:") + message
    file.write(log)
    file.write("\n")
    file.close()

def logout_auth(userlogout):
    file = open('auth.log', 'a')
    message = " " + "user\t" + userlogout + "\tlogout "
    time = datetime.datetime.now()
    log = time.strftime("%Y-%m-%d %H:%M:%S\t:") + message
    file.write(log)
    file.write("\n")
    file.close()

def login_insta(userlogin):
    file = open('authinsta.log', 'a')
    message = " " + "user\t" + userlogin + "\tstarted instagram "
    time = datetime.datetime.now()
    log = time.strftime("%Y-%m-%d %H:%M:%S\t:") + message
    file.write(log)
    file.write("\n")
    file.close()
