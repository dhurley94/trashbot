from flask import Flask, escape, request
from models.submission import Submissions
from database import SubmissionManager

app = Flask(__name__)


@app.route('/home', methods=['GET', 'POST'])
def home():
    uri = request.args.get['uri']
    return {"data": SubmissionManager.get_submission_by_uri(uri=uri)}
