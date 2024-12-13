from flask import Flask,request , url_for,render_template,send_from_directory,session


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('two.html')

@app.route('/submit',methods=['GET'])
def submit():
    if request.method=='GET':
        name=request.args.get('Name')
        DOB=request.args.get('DOB')
        Number=request.args.get('Number')
        Email=request.args.get('Email')
        Introduction=request.args.get('Introduction')
        print(f'name:{name}')
    else:
        print('something went wrong')
    return render_template('two.html',message='success',Name=name,DOB=DOB,Number=Number,Email=Email,Introduction=Introduction)
        
if __name__=="__main__":
    app.run(debug=True)
