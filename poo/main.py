#!/usr/bin/env python

from metaplugin import BasePlugin
import os

if __name__ == "__main__":

    # Load the plugins
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if (name.startswith("plugin") and name.endswith(".py")):
                # plugin-name = file name without the .py extension
                plugin_name = os.path.splitext(os.path.basename(name))[0]
                # Import the plugin
                try:
                    exec("import %s" % plugin_name)
                except Exception as e:
                    print("Error loading plugin %s: %s" % (plugin_name, e))
                except:
                    print("Error loading plugin %s: Unknown error" % plugin_name)
                else:
                    print("Plugin %s loaded" % plugin_name) 

    # Iter through plugins
    for p in BasePlugin.dict().keys():
        # print("%s: %s" % (p, Plugin.dict()[p]))
        # print("%s" % Plugin.dict()[p].__module__)
        cmd = "i = %s.%s()" % (BasePlugin.dict()[p].__module__, p)
        # print("Exec: %s" % cmd) 
        exec(cmd)
        # print(i)
        # print(type(i))
        print(">>> %s" % i.test())
        print(">>> %s" % i.test2())

