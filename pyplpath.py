import os
import inspect

ExDir = os.path.join(os.path.realpath(os.path.abspath(
    os.path.split(inspect.getfile(inspect.currentframe()))[0])),
                     '../Examples') + '/'
