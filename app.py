from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form.get('name')
    return f"Hello, {name}!"

if __name__ == '__main__':
    import os
    # to run app in production
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
