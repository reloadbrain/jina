from typing import TypeVar

from ..proto import jina_pb2

AnyNdArray = TypeVar('AnyNdArray')


class BaseNdArray:
    """A base class for containing the protobuf message of NdArray. It defines interfaces
    for easier get/set value.

    Do not use this class directly. Subclass should be used.
    """

    def __init__(self, proto: 'jina_pb2._reflection.GeneratedProtocolMessageType' = None, *args, **kwargs):
        """

        :param proto: the protobuf message, when not given then create a new one via :meth:`get_null_proto`
        """
        if proto:
            self.proto = proto  # a weak ref/copy
        else:
            self.proto = self.get_null_proto()

    def get_null_proto(self):
        """Get the new protobuf representation"""
        raise NotImplementedError

    @property
    def value(self) -> AnyNdArray:
        """Return the value of the ndarray, in numpy, scipy, tensorflow, pytorch type"""
        raise NotImplementedError

    @value.setter
    def value(self, value: AnyNdArray):
        """Set the value from numpy, scipy, tensorflow, pytorch type to protobuf"""
        raise NotImplementedError

    @property
    def is_sparse(self) -> bool:
        """Return true if the ndarray is sparse """
        raise NotImplementedError

    def copy_to(self, proto: 'jina_pb2._reflection.GeneratedProtocolMessageType') -> 'BaseNdArray':
        """Copy itself to another protobuf message, return a view of the copied message"""
        proto.CopyFrom(self.proto)
        return BaseNdArray(proto)