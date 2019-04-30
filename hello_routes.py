#
# HELLO ROUTES
#

from main import app

@app.route('/hello', methods=['GET'])
def get_hello():
    return "Hello"

@app.route('/goodbye', methods=['GET'])
def get_goodbye():
    return "Goodbye"
