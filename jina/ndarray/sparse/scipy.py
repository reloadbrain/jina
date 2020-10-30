import numpy as np
import scipy.sparse
from scipy.sparse import coo_matrix

from .. import BaseNdArray
from ..dense.numpy import DenseNdArray
from ...proto import jina_pb2


class SparseNdArray(BaseNdArray):
    """Scipy powered sparse ndarray

    .. warning::
        scipy only supports ndim=2
    """

    def __init__(self, proto: 'jina_pb2.SparseNdArray' = None, sp_format: str = 'coo', *args, **kwargs):
        """

        :param sp_format: the sparse format of the scipy matrix. one of 'coo', 'bsr', 'csc', 'csr'
        :param args:
        :param kwargs:
        """
        super().__init__(proto, *args, **kwargs)
        support_fmt = {'coo', 'bsr', 'csc', 'csr'}
        if sp_format in support_fmt:
            self.spmat_fn = getattr(scipy.sparse, f'{sp_format}_matrix')
        else:
            raise ValueError(f'{sp_format} sparse matrix is not supported, please choose one of those: {support_fmt}')

    def get_null_proto(self):
        return jina_pb2.SparseNdArray()

    @property
    def value(self) -> 'scipy.sparse.spmatrix':
        row_col = DenseNdArray(self.proto.indicies).value
        if row_col.shape[-1] != 2:
            raise ValueError(f'scipy backend only supports ndim=2 sparse matrix, given {row_col.value.shape}')
        row = row_col[:, 0]
        col = row_col[:, 1]
        val = DenseNdArray(self.proto.values).value
        return self.spmat_fn((val, (row, col)), shape=self.proto.dense_shape)

    @value.setter
    def value(self, value: 'scipy.sparse.spmatrix'):
        v = coo_matrix(value)
        DenseNdArray(self.proto.indicies).value = np.stack([v.row, v.col], axis=1)
        DenseNdArray(self.proto.values).value = v.data
        self.proto.dense_shape.extend(v.shape)

    @property
    def is_sparse(self) -> bool:
        return True