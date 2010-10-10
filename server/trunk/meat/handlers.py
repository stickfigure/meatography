from datetime import datetime
from entities import Measurement
from moe.base.handlers import AreaRequestHandler
from pytz import UTC
from tipfy import render_json_response
from wtforms.ext.appengine.db import model_form
from wtforms.form import Form

class NewMeasurement(AreaRequestHandler):
    '''
    Creates a new measurement from a post/get
    '''
    def createNew(self, params):
        m = Measurement()
        form_type = model_form(Measurement, exclude=("when"))
        mForm = form_type(params)
        assert isinstance(mForm, Form)
        mForm.populate_obj(m)
        m.when = datetime.fromtimestamp(int(params["when"]), UTC)
        m.save()

    def get(self):
        self.createNew(self.request.args)
        return self.redirect_to("measurements", 302)
    def post(self):
        self.createNew(self.request.form)
        return render_json_response({ "status":0, "tempTarget": 50, "humidityTarget": 70 })

class ResultStub(AreaRequestHandler):
    def get(self):
        return render_json_response({ "status":0, "tempTarget": 50, "humidityTarget": 70 })
    def post(self):
        return self.get()
    
class ListRawMeasurements(AreaRequestHandler):
    '''
    List all the measurements
    '''
    def get(self):
        m = Measurement.all()
        return self.render_template("meat/measurements.html", measurements = m)