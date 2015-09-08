#!/usr/bin/env python

# PAS BON: regarder: https://github.com/rubenrua/GstreamerCodeSnippets/blob/master/1.0/Python/pygst-tutorial/example4.py


import sys

# Load the GStreamer 1.x lib through the new PyGTK
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject


def play_mp3(uri):
    # Play the uri
    # mainloop = GObject.MainLoop()
    GObject.threads_init()
    Gst.init([])
    pipeline = Gst.ElementFactory.make("playbin", None)
    if pipeline is None:
        print("ERROR: Can not create pipe")
        sys.exit(1)

    print("Playing: %s" % uri)
    pipeline.set_property("uri", uri)
    pipeline.set_state(Gst.State.PLAYING)
    # Il manque le truc pour lancer la pipeline...

def main():
    print("Load %s" % str(Gst.version_string()))
    play_mp3("/home/nicolargo/Musique/Goldman/06 Rouge.mp3")

if __name__ == '__main__':
    main()
