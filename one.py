from flask import Flask,request , url_for,render_template,send_from_directory,session
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('one.html')

@app.route('/submit',methods=['POST'])
def submit():
    if request.method=='POST':
        name=request.form['name']
        location=request.form['location']
        print(f' name: {name}')
    else:
        name=request.args.get('name')
        location=request.args.get('location')
        print(f'name: {name}')
    return render_template('one.html',message='success',name=name,location=location,) 

if __name__=='__main__':
    app.run(debug=True)