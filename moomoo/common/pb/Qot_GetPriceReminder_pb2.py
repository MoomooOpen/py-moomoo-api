# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Qot_GetPriceReminder.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Common_pb2 as Common__pb2
import Qot_Common_pb2 as Qot__Common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Qot_GetPriceReminder.proto',
  package='Qot_GetPriceReminder',
  syntax='proto2',
  serialized_pb=_b('\n\x1aQot_GetPriceReminder.proto\x12\x14Qot_GetPriceReminder\x1a\x0c\x43ommon.proto\x1a\x10Qot_Common.proto\"k\n\x11PriceReminderItem\x12\x0b\n\x03key\x18\x01 \x02(\x03\x12\x0c\n\x04type\x18\x02 \x02(\x05\x12\r\n\x05value\x18\x03 \x02(\x01\x12\x0c\n\x04note\x18\x04 \x02(\t\x12\x0c\n\x04\x66req\x18\x05 \x02(\x05\x12\x10\n\x08isEnable\x18\x06 \x02(\x08\"\x80\x01\n\rPriceReminder\x12&\n\x08security\x18\x01 \x02(\x0b\x32\x14.Qot_Common.Security\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x39\n\x08itemList\x18\x02 \x03(\x0b\x32\'.Qot_GetPriceReminder.PriceReminderItem\"=\n\x03\x43\x32S\x12&\n\x08security\x18\x01 \x01(\x0b\x32\x14.Qot_Common.Security\x12\x0e\n\x06market\x18\x02 \x01(\x05\"E\n\x03S2C\x12>\n\x11priceReminderList\x18\x01 \x03(\x0b\x32#.Qot_GetPriceReminder.PriceReminder\"1\n\x07Request\x12&\n\x03\x63\x32s\x18\x01 \x02(\x0b\x32\x19.Qot_GetPriceReminder.C2S\"j\n\x08Response\x12\x15\n\x07retType\x18\x01 \x02(\x05:\x04-400\x12\x0e\n\x06retMsg\x18\x02 \x01(\t\x12\x0f\n\x07\x65rrCode\x18\x03 \x01(\x05\x12&\n\x03s2c\x18\x04 \x01(\x0b\x32\x19.Qot_GetPriceReminder.S2CBJ\n\x13\x63om.futu.openapi.pbZ3github.com/futuopen/ftapi4go/pb/qotgetpricereminder')
  ,
  dependencies=[Common__pb2.DESCRIPTOR,Qot__Common__pb2.DESCRIPTOR,])




_PRICEREMINDERITEM = _descriptor.Descriptor(
  name='PriceReminderItem',
  full_name='Qot_GetPriceReminder.PriceReminderItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Qot_GetPriceReminder.PriceReminderItem.key', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='Qot_GetPriceReminder.PriceReminderItem.type', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='Qot_GetPriceReminder.PriceReminderItem.value', index=2,
      number=3, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='note', full_name='Qot_GetPriceReminder.PriceReminderItem.note', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='freq', full_name='Qot_GetPriceReminder.PriceReminderItem.freq', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='isEnable', full_name='Qot_GetPriceReminder.PriceReminderItem.isEnable', index=5,
      number=6, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=84,
  serialized_end=191,
)


_PRICEREMINDER = _descriptor.Descriptor(
  name='PriceReminder',
  full_name='Qot_GetPriceReminder.PriceReminder',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='security', full_name='Qot_GetPriceReminder.PriceReminder.security', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='Qot_GetPriceReminder.PriceReminder.name', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='itemList', full_name='Qot_GetPriceReminder.PriceReminder.itemList', index=2,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=194,
  serialized_end=322,
)


_C2S = _descriptor.Descriptor(
  name='C2S',
  full_name='Qot_GetPriceReminder.C2S',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='security', full_name='Qot_GetPriceReminder.C2S.security', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='market', full_name='Qot_GetPriceReminder.C2S.market', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=324,
  serialized_end=385,
)


_S2C = _descriptor.Descriptor(
  name='S2C',
  full_name='Qot_GetPriceReminder.S2C',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='priceReminderList', full_name='Qot_GetPriceReminder.S2C.priceReminderList', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=387,
  serialized_end=456,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='Qot_GetPriceReminder.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='c2s', full_name='Qot_GetPriceReminder.Request.c2s', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=458,
  serialized_end=507,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='Qot_GetPriceReminder.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='retType', full_name='Qot_GetPriceReminder.Response.retType', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=True, default_value=-400,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='retMsg', full_name='Qot_GetPriceReminder.Response.retMsg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='errCode', full_name='Qot_GetPriceReminder.Response.errCode', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='s2c', full_name='Qot_GetPriceReminder.Response.s2c', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=509,
  serialized_end=615,
)

_PRICEREMINDER.fields_by_name['security'].message_type = Qot__Common__pb2._SECURITY
_PRICEREMINDER.fields_by_name['itemList'].message_type = _PRICEREMINDERITEM
_C2S.fields_by_name['security'].message_type = Qot__Common__pb2._SECURITY
_S2C.fields_by_name['priceReminderList'].message_type = _PRICEREMINDER
_REQUEST.fields_by_name['c2s'].message_type = _C2S
_RESPONSE.fields_by_name['s2c'].message_type = _S2C
DESCRIPTOR.message_types_by_name['PriceReminderItem'] = _PRICEREMINDERITEM
DESCRIPTOR.message_types_by_name['PriceReminder'] = _PRICEREMINDER
DESCRIPTOR.message_types_by_name['C2S'] = _C2S
DESCRIPTOR.message_types_by_name['S2C'] = _S2C
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PriceReminderItem = _reflection.GeneratedProtocolMessageType('PriceReminderItem', (_message.Message,), dict(
  DESCRIPTOR = _PRICEREMINDERITEM,
  __module__ = 'Qot_GetPriceReminder_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetPriceReminder.PriceReminderItem)
  ))
_sym_db.RegisterMessage(PriceReminderItem)

PriceReminder = _reflection.GeneratedProtocolMessageType('PriceReminder', (_message.Message,), dict(
  DESCRIPTOR = _PRICEREMINDER,
  __module__ = 'Qot_GetPriceReminder_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetPriceReminder.PriceReminder)
  ))
_sym_db.RegisterMessage(PriceReminder)

C2S = _reflection.GeneratedProtocolMessageType('C2S', (_message.Message,), dict(
  DESCRIPTOR = _C2S,
  __module__ = 'Qot_GetPriceReminder_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetPriceReminder.C2S)
  ))
_sym_db.RegisterMessage(C2S)

S2C = _reflection.GeneratedProtocolMessageType('S2C', (_message.Message,), dict(
  DESCRIPTOR = _S2C,
  __module__ = 'Qot_GetPriceReminder_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetPriceReminder.S2C)
  ))
_sym_db.RegisterMessage(S2C)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'Qot_GetPriceReminder_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetPriceReminder.Request)
  ))
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'Qot_GetPriceReminder_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetPriceReminder.Response)
  ))
_sym_db.RegisterMessage(Response)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\023com.futu.openapi.pbZ3github.com/futuopen/ftapi4go/pb/qotgetpricereminder'))
# @@protoc_insertion_point(module_scope)
