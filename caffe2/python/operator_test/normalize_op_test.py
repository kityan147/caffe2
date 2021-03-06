from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from hypothesis import given
import hypothesis.strategies as st
from caffe2.python import core
import caffe2.python.hypothesis_test_util as hu


class TestNormalizeOp(hu.HypothesisTestCase):

    @given(X=hu.tensor(min_dim=2,
                       max_dim=2,
                       elements=st.floats(min_value=0.5, max_value=1.0)),
           **hu.gcs)
    def test_normalize(self, X, gc, dc):
        op = core.CreateOperator("Normalize", "X", "Y")

        def ref_normalize(X):
            x_normed = X / (
                np.sqrt((X**2).sum(-1))[:, np.newaxis] + np.finfo(X.dtype).tiny)
            return (x_normed,)

        self.assertReferenceChecks(gc, op, [X], ref_normalize)
        self.assertDeviceChecks(dc, op, [X], [0])
        self.assertGradientChecks(gc, op, [X], 0, [0])
