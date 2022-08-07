from flask import Flask, render_template, jsonify, request, redirect
from Shortener import Shortener
import json
import traceback

app = Flask(__name__)

@app.route('/')
def list_endpoints():
    app.logger.info("Listing actions")
    return "200"

short = Shortener()

@app.route('/get-short-url', methods = ['GET', 'POST'])
def getShortUrl():
    try:
        data = json.loads(request.data)
        short_code = short.set_short_code(data, scheme = request.scheme, host = request.host)
        return request.host_url + short_code
    except Exception as e:
        traceback.print_exc()
        return "200"

@app.route('/<shortcode>', methods=['GET'])
def redirect_url(shortcode):
    return redirect(short.get_short_url(shortcode, scheme = request.scheme, host = request.host))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)