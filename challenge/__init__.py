from flask import Flask;
app = Flask(__name__)
import challenge.routes.evaluate;
import challenge.routes.instructions


