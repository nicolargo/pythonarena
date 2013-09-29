#!/usr/bin/env python

class MetaPlugin(type):
    """ Metaclass object for plugin """

    def __init__(self, name, bases, dict):
        """ Init the Metaclass for plugin """        

        if not hasattr(self, '_plugin_dict'):
            #print("Base class. Create the plugin dictionnary.")
            self._plugin_dict = {}
        else:        
            #print("Register class %s using the MetaPlugin metaclass" % name)
            self._plugin_dict[name] = self
            type.__init__(self, name, bases, dict)

    def __del__(self):
        """ Delete the object => Delete it from the dict """
        del(self._plugin_dict[self.__name__])
    
    def __repr__(self):
        """ Return the plugins dictionnary """
        return repr(self._plugin_dict)

    def __str__(self):
        """ Return class name """
        return str(self.__name__)

    def dict(self):
        """ Return the plugins dictionnary """
        return self._plugin_dict

# Define the base plugin class (both Python 2 and 3 compatible)
# But how to define the test2 method ???
# BasePlugin = MetaPlugin('Plugin', (object, ), {})

# Python 3 Only...
class BasePlugin(object):
    """ Metaclass object for plugin """    
    __metaclass__ = MetaPlugin

    def test2(self):
        return "test2"        

# Python 2 Only...
# class BasePlugin(object):
#     __metaclass__ = MetaPlugin

#     def test2(self):
#         return "test2"        
