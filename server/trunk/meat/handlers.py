from entities import Measurement
from moe.base.handlers import AreaRequestHandler
from wtforms.ext.appengine.db import model_form
from wtforms.form import Form

class MainPage(AreaRequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.write('Hello, webapp2 World!')
        
class NewMeasurement(AreaRequestHandler):
    '''
    Creates a new measurement from a post/get
    '''
    def createNew(self):
        m = Measurement()
        m_form = model_form(Measurement)
        assert isinstance(m_form, Form)
        m_form.populate_obj(m)
        m.save()
        
    def get(self):
        self.createNew()
        return self.redirect_to("measurements", 302)
    def post(self):
        self.createNew()
        return self.redirect_to("measurements", 302)

class ListRawMeasurements(AreaRequestHandler):
    '''
    List all the measurements
    '''
    def get(self):
        return self.render_template("meat/measurements.html", measurements = Measurement.all())