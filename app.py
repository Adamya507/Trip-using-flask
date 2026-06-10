import mysql.connector
import json
import collections
from flask import Flask,render_template,redirect,url_for,request
app=Flask(__name__)

conn = mysql.connector.connect(host="localhost",user="root",password="",db="trip")


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/createForm")
def createForm():
    return render_template("insert.html")

@app.route("/insert",methods=['POST','GET'])
def insert():
    if request.method=='POST':
        cursor = conn.cursor()
        name=request.form["name"]
        latitude=request.form["latitude"]
        longitude=request.form["longitude"]
        cursor.execute("insert into triptable(name,latitude,longitude) values(%s,%s,%s)",(name,latitude,longitude))
        conn.commit()
        cursor.close()
        return render_template("linkinsert.html",name=name)
    
    return redirect(url_for("createForm"))

@app.route("/listForm")
def show():
    cursor=conn.cursor()
    cursor.execute('select *from triptable')
    data=cursor.fetchall()
    cursor.close()
    return render_template("show.html",data=data)

@app.route("/updateForm")
def updateform():
    return render_template("updateid.html")

@app.route("/updateid", methods=['POST','GET'])
def updateid():
    if(request.method=='POST'):
        cursor=conn.cursor()
        id=int(request.form["upid"])
        cursor.execute("select *from triptable where id=%s",(id,))
        data=cursor.fetchall()
        if data:
            cursor.close()
        
            return render_template("update.html",data=data)
        else:
            return render_template("error.html")
    
@app.route("/update_dat",methods=['POST','GET'])
def updatedata():
    if request.method=='POST':
        cursor=conn.cursor()
        id=int(request.form["id"])
        name=request.form["name"]
        latitude=int(request.form["lat"])
        longitude=int(request.form["lon"])
        cursor.execute("update triptable set name=%s,latitude=%s,longitude=%s where id=%s",(name,latitude,longitude,id))
        conn.commit()
        cursor.close()
        return render_template("link.html",name=name)
    
    return redirect(url_for("main"))

@app.route("/listjsonForm")
def listjsonForm():
    cursor=conn.cursor()
    cursor.execute("select *from triptable ") 
    rows=cursor.fetchall()
    object=[]
    for row in rows:
        d=collections.OrderedDict()
        d["id"]=row[0]
        d["name"]=row[1]
        d["latitude"]=row[2]
        d["longitude"]=row[2]
        object.append(d)
        
    j=json.dumps(object)
    cursor.close()
    return render_template("listjson.html",d=j) 

@app.route("/deleteForm")
def deleteform():
    return render_template("deleteid.html")  

@app.route("/deleteid",methods=['GET','POST'])
def deleteid():
    if request.method=='POST':
        cursor=conn.cursor()
        delid=int(request.form["delid"])
        cursor.execute("select *from triptable where id=%s",(delid,))
        data=cursor.fetchall()
        if data:
            cursor=conn.cursor()
            cursor.execute("delete from triptable where id=%s ",(delid,))
            conn.commit()
            cursor.close()
            return render_template("index.html")
        else:
            return render_template("error_delete.html")
        
    
if __name__=="__main__":
    app.run(debug=True)