#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

import os
from pyplpath import ExDir
from pypl import plError

fast = fast if 'fast' in dir() else True
if fast:
    print 'executing the fast test'
else :
    print 'executing the exhaustive test'

all_examples = [
    'chapter1/dice.py',
    'chapter2/spam.py',
    'chapter4/kepera.py',
    'chapter4/simulatefollowing.py',
    'chapter4/simulatepushing.py',
    'chapter6/calibration.py',
    'chapter6/treatmentcenter.py',
    'chapter7/fusion.py',
    'chapter7/classification.py',
    'chapter7/ancillary.py',
    'chapter7/invpgm.py',
    'chapter8/logcoding.py',
    'chapter9/sprinkler.py',
    'chapter9/SubroutineFusion.py',
    'chapter9/stitching.py',
    'chapter10/Bif.py',
    'chapter10/simulateavoid.py',
    'chapter10/EMbehavior.py',
    'chapter10/EMbehavior.py',
    'chapter11/sumdices.py',
    'chapter11/pseudokalman.py',
    'chapter11/markovloc.py',
    'chapter14/optimization.py',
    'chapter15/ML.py',
    'chapter15/BE.py',
    'chapter15/genweights.py',
    'chapter15/getlambda.py'
]

fast_examples = [
    'chapter1/dice.py',
    'chapter2/spam.py',
    'chapter4/kepera.py',
    'chapter4/simulatefollowing.py',
    'chapter4/simulatepushing.py',
    'chapter7/classification.py',
    'chapter7/ancillary.py',
    'chapter7/invpgm.py',
    'chapter8/logcoding.py',
    'chapter9/sprinkler.py',
    'chapter9/SubroutineFusion.py',
    'chapter10/Bif.py',
    'chapter10/simulateavoid.py',
    'chapter10/EMbehavior.py',
    'chapter10/EMbehavior.py',
    'chapter11/sumdices.py',
    'chapter14/optimization.py',
    'chapter15/ML.py',
    'chapter15/BE.py',
    'chapter15/genweights.py',
    'chapter15/getlambda.py'
]

plError.ignore_this_message(122, True)
plError.ignore_this_message(38, True)
plError.ignore_this_message(107, True)
plError.ignore_this_message(122, True)
plError.ignore_this_message(37, True)

for example in fast_examples if fast else all_examples:
    print 'executing', example
    execfile(os.path.join(ExDir, example))
    print 'end of', example
