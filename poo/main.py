#!/usr/bin/env python

import imp
import os

if __name__ == "__main__":

    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if (name.startswith("plugin") and name.endswith(".py")):
                # Do not want the .py extension
                plugin_name = os.path.splitext(os.path.basename(name))[0]
                # Import the plugin
                print("Load plugin: %s" % plugin_name)
                try:
                    exec("import %s" % plugin_name)
                except Exception, e:
                    print("Error loading plugin %s: %s" % (plugin_name, e))
                except:
                    print("Error loading plugin %s: Unknown error" % plugin_name)


