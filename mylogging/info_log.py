import datetime
def Logfollower(st):
   try:
       file = open('follower.txt','a')
       if('\n'+st=='------------------------------------------------------------------------------\n'):
           file.write(st)
       else:
           Now = datetime.datetime.now()
           log=Now.strftime("%Y-%m-%d %H:%M:%S ")+st
           file.write(log)
           file.write("\n")
           file.close()
   except Exception as e:
        print(str(e)+'\n')