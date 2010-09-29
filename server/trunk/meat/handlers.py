from entities import Measurement
from moe.base.handlers import AreaRequestHandler
from wtforms.ext.appengine.db import model_form
from wtforms.form import Form
from pytz import UTC
from datetime import datetime
from tipfy import render_json_response

class NewMeasurement(AreaRequestHandler):
    '''
    Creates a new measurement from a post/get
    '''
    def createNew(self):
        m = Measurement()
        m_form = model_form(Measurement, exclude=("when"))
        assert isinstance(m_form, Form)
        m_form.populate_obj(m)
        m.when = datetime.datetime.fromtimestamp(int(self.request.get("when")), UTC)
        m.save()
        
    def get(self):
        self.createNew()
        return self.redirect_to("measurements", 302)
    def post(self):
        self.createNew()
        return self.redirect_to("measurements", 302)

class ResultStub(AreaRequestHandler):
    def get(self):
        return render_json_response({ "status":0, "tempTarget": 50, "humidityTarget": 70 })
    
class ListRawMeasurements(AreaRequestHandler):
    '''
    List all the measurements
    '''
    def get(self):
        return self.render_template("meat/measurements.html", measurements = Measurement.all())