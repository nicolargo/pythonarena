#!/usr/bin/env python

class MetaPlugin(type):
    """ Metaclass object for plugin """

    def __init__(self, name, bases, dict):
        """ Init the Metaclass for plugin """        

        if not hasattr(self, 'plugin_dict'):
            print("Base class. Create the plugin dictionnary.")
            self.plugin_dict = {}
        else:        
            print("Register class %s using the MetaPlugin metaclass" % name)
            self.plugin_dict[name] = self
            type.__init__(self, name, bases, dict)

    def __str__(self):
        """ Return the name of the class """
        return self.__name__
    
    def printdict(self):
        print(self.plugin_dict)


# Define the base plugin class (both Python 2 and 3 compatible)
Plugin = MetaPlugin('Plugin', (object, ), {})

