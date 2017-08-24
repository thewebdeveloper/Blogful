# fire up the development server
import os
from flask import Flask

app = Flask(__name__)
# load the configuration from config
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
app.config.from_object(config_path)


# to make use of the app object
from . import views
from . import filters