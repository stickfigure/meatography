from datetime import datetime
from entities import Measurement
from moe.base.handlers import AreaRequestHandler
from pytz import UTC
from tipfy import render_json_response
from wtforms.ext.appengine.db import model_form
from wtforms.form import Form
from meat.entities import measurements_list_pager
from tipfy.ext.i18n import get_timezone
from google.appengine.ext import db
from tipfy.ext.auth import AppEngineAuthMixin, admin_required

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

class DeleteMeasurements(AreaRequestHandler, AppEngineAuthMixin):
    '''
    List all the measurements
    '''
    @admin_required
    def get(self):
        limit_arg = self.request.args.get('limit')
        l = 450
        
        if limit_arg: 
            l = int(limit_arg)
        
        db.delete(Measurement.all(keys_only=True).fetch(limit=l))
        return self.redirect_to("measurements")
    
class ListRawMeasurements(AreaRequestHandler):
    '''
    List all the measurements
    '''
    def get(self):
        curr_cursor = self.request.args.get('start')
        ms, cursor = measurements_list_pager(cursor=curr_cursor, limit=60)
        ctx = {
            'measurements':     ms,
            'is_first_page':    curr_cursor is None,
            'next_page':        cursor,
            'tz_utc':           UTC,
            'tz':               get_timezone("America/Los_Angeles"),
        }

        return self.render_template("meat/measurements.html", **ctx)