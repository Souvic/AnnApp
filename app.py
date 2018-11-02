
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
  ssl._create_default_https_context = ssl._create_unverified_context


from flask import Flask, request,render_template
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
def valid_login(p,q):
    tt=os.listdir("./answers/")
    if(p+"_unique_"+q+".txt" in tt):
        return(True)
    else:
        
        return(False)

def valid_firstname(p):
    tt=[op.split("_unique_")[0] for op in os.listdir("./answers/")]
    if(p in tt):
        return(True)
    else:
        
        return(False)
def update_answer(v,w,z):
    fi=open("answers/"+w+"_unique_"+z+".txt","a")
    fi.write(v)
    fi.close()
def chooseQ(xx,yy):
    fi=open("answers/"+xx+"_unique_"+yy+".txt","r")
    y=fi.read()
    fi.close()
    nqa=len(y)//6
    fi=open("q.txt","r")
    y=fi.read()
    fi.close()
    return(y.split("#uniqjoin#")[nqa])

def done(xx,yy):
    fi=open("answers/"+xx+"_unique_"+yy+".txt","r")
    y=fi.read()
    fi.close()
    nqa=len(y)//6
    fi=open("q.txt","r")
    y=fi.read()
    fi.close()
    print(len(y.split("#uniqjoin#")))
    print(nqa)
    return(len(y.split("#uniqjoin#"))==nqa+1)

@app.route('/app/login/',methods=['POST', 'GET'])

def login():
    return("working")
    
    error = ""
    if request.method == 'POST':
        if(request.form["from"]=="exit"):
            error="Logged out successfully"
            return render_template('i.html', error=error)
        
        if(request.form["from"]=="app"):
            if valid_login(request.form['FirstName'],request.form['password']):
                if(done(request.form['FirstName'],request.form['password'])):
                    return("done")
                update_answer(request.form["a"],request.form['FirstName'],request.form['password'])
                return render_template('app.html',error=error,q=chooseQ(request.form['FirstName'],request.form['password']),fn=request.form['FirstName'],pwd=request.form['password'])
            else:
                error = 'Invalid username/password'
        else:
            if(request.form["from"]=="register"):
                if valid_login(request.form['FirstName'],request.form['password']):
                    error="Already Registered"
                        
                else:
                    if valid_firstname(request.form['FirstName']):
                        error="Wrong password, username already registered"
                    else:
                        oo=open("./answers/"+request.form['FirstName']+"_unique_"+request.form['password']+".txt","w+")
                        oo.close()
                        error="Successfully registered, you may log in now"
            else:
                if valid_login(request.form['FirstName'],request.form['password']):
                    if(done(request.form['FirstName'],request.form['password'])):
                        return("done")
                    else:
                        return render_template('app.html',error=error,q=chooseQ(request.form['FirstName'],request.form['password']),fn=request.form['FirstName'],pwd=request.form['password'])
                    
                        
                error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    
    return render_template('i.html', error=error)
    
    
app.run(host='127.0.0.1',port="80")
