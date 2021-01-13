# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from lebai_msgs/SetAOutRequest.msg. Do not edit."""
import codecs
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct


class SetAOutRequest(genpy.Message):
  _md5sum = "ea7eca226d31910fccddba8c483e4857"
  _type = "lebai_msgs/SetAOutRequest"
  _has_header = False  # flag to mark the presence of a Header object
  _full_text = """uint8 group
uint16 index
float64 value
"""
  __slots__ = ['group','index','value']
  _slot_types = ['uint8','uint16','float64']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       group,index,value

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(SetAOutRequest, self).__init__(*args, **kwds)
      # message fields cannot be None, assign default values for those that are
      if self.group is None:
        self.group = 0
      if self.index is None:
        self.index = 0
      if self.value is None:
        self.value = 0.
    else:
      self.group = 0
      self.index = 0
      self.value = 0.

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_get_struct_BHd().pack(_x.group, _x.index, _x.value))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      end = 0
      _x = self
      start = end
      end += 11
      (_x.group, _x.index, _x.value,) = _get_struct_BHd().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_get_struct_BHd().pack(_x.group, _x.index, _x.value))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      end = 0
      _x = self
      start = end
      end += 11
      (_x.group, _x.index, _x.value,) = _get_struct_BHd().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_BHd = None
def _get_struct_BHd():
    global _struct_BHd
    if _struct_BHd is None:
        _struct_BHd = struct.Struct("<BHd")
    return _struct_BHd
# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from lebai_msgs/SetAOutResponse.msg. Do not edit."""
import codecs
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import industrial_msgs.msg

class SetAOutResponse(genpy.Message):
  _md5sum = "50b1f38f75f5677e5692f3b3e7e1ea48"
  _type = "lebai_msgs/SetAOutResponse"
  _has_header = False  # flag to mark the presence of a Header object
  _full_text = """industrial_msgs/ServiceReturnCode code

================================================================================
MSG: industrial_msgs/ServiceReturnCode
# Service return codes for simple requests.  All ROS-Industrial service
# replies are required to have a return code indicating success or failure
# Specific return codes for different failure should be negative.
int8 val

int8 SUCCESS = 1
int8 FAILURE = -1

"""
  __slots__ = ['code']
  _slot_types = ['industrial_msgs/ServiceReturnCode']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       code

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(SetAOutResponse, self).__init__(*args, **kwds)
      # message fields cannot be None, assign default values for those that are
      if self.code is None:
        self.code = industrial_msgs.msg.ServiceReturnCode()
    else:
      self.code = industrial_msgs.msg.ServiceReturnCode()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self.code.val
      buff.write(_get_struct_b().pack(_x))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      if self.code is None:
        self.code = industrial_msgs.msg.ServiceReturnCode()
      end = 0
      start = end
      end += 1
      (self.code.val,) = _get_struct_b().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self.code.val
      buff.write(_get_struct_b().pack(_x))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      if self.code is None:
        self.code = industrial_msgs.msg.ServiceReturnCode()
      end = 0
      start = end
      end += 1
      (self.code.val,) = _get_struct_b().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_b = None
def _get_struct_b():
    global _struct_b
    if _struct_b is None:
        _struct_b = struct.Struct("<b")
    return _struct_b
class SetAOut(object):
  _type          = 'lebai_msgs/SetAOut'
  _md5sum = '51928732046ffb5b5606f765ba7fcd8b'
  _request_class  = SetAOutRequest
  _response_class = SetAOutResponse