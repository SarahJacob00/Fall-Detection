from flask import Flask,render_template,request,redirect, url_for
import Fall_Model
import json
import requests


#ctrl+shift+R...i think


app= Flask(__name__,static_folder=r"C:\Users\jacob\#A FYP\FallApplication\static")
i=0
fall=''
stood=''

#RESULTS OF PAGES

@app.route("/page2a",methods = ['POST', 'GET'])
def page2a():
    global add,i
    if request.method == 'POST': 
        if request.form['btn']=='Yes':
            return render_template('page1.html')
        
        
    else: 
        if request.form['btn']=='Yes':
            return render_template('page1.html')

#PAGE TO UPLOAD FILE
@app.route("/page1",methods = ['POST', 'GET'])
def page1():
    global i,add
    if request.method == 'POST':
        if request.form['submit']=='Upload Video':
            video = request.form['videomp4']
            sfall,stoodstr=Fall_Model.model(video)
            
            
            return render_template('page2a.html',fall=sfall,stood=stoodstr) #Song VERIFIED page

        
    elif request.method=='GET':
        if request.form['submit']=='Upload Video':
            video = request.form['videomp4']
            sfall,stoodstr=Fall_Model.model(video)
            
            
            return render_template('page2a.html',fall=sfall,stood=stoodstr) #Song VERIFIED page


        

#HOME PAGE
@app.route("/home",methods = ['POST', 'GET'])
def home(): 
    global add
    if request.method == 'POST': 
      #user = request.form['nm'] 
      return render_template('page1.html')
    else: 
      #user = request.args.get('nm') 
      return render_template('page1.html')

@app.route("/")
@app.route("/routee",methods = ['POST', 'GET'])
def routee():
    if request.method == 'POST':
        return render_template('homee.html')
    else:
        return render_template('homee.html')

if __name__=='__main__':
    app.add_url_rule('/', 'routee', routee)
    app.add_url_rule('/', 'homee', home)
    app.add_url_rule('/', 'page1', page1)
    app.add_url_rule('/', 'page2a', page2a)
   
    
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)