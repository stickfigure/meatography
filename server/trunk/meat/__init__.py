'''
Created on Sep 14, 2010

@author: skot
'''
from google.appengine.ext import db
from google.appengine.ext.db import BadValueError

        
        

class KeyProperty(db.Property):
    """A property that stores a key, without automatically dereferencing it.

    Example usage:

    >>> class SampleModel(db.Model):
    ...   sample_key = KeyProperty()

    >>> model = SampleModel()
    >>> model.sample_key = db.Key.from_path("Foo", "bar")
    >>> model.put() # doctest: +ELLIPSIS
    datastore_types.Key.from_path(u'SampleModel', ...)

    >>> model.sample_key # doctest: +ELLIPSIS
    datastore_types.Key.from_path(u'Foo', u'bar', ...)

    Adapted from aetycoon: http://github.com/Arachnid/aetycoon/
    Added possibility to set it using a db.Model instance.
    """
    def validate(self, value):
        """Validate the value.

        Args:
          value: The value to validate.
        Returns:
          A valid key.
        """
        if isinstance(value, basestring):
            value = db.Key(value)
        elif isinstance(value, db.Model):
            if not value.has_key():
                raise BadValueError('%s instance must have a complete key to '
                    'be stored.' % value.__class__.kind())

            value = value.key()

        if value is not None:
            if not isinstance(value, db.Key):
                raise TypeError('Property %s must be an instance of db.Key'
                    % self.name)

        return super(KeyProperty, self).validate(value)    
    