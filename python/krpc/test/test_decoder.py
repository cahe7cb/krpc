#!/usr/bin/env python2

import unittest
from krpc.decoder import _Decoder as Decoder
from krpc.types import _Types as Types
from krpc.platform import hexlify, unhexlify
import krpc.schema.KRPC

class TestDecoder(unittest.TestCase):

    def test_decode_message(self):
        typ = krpc.schema.KRPC.Request
        message = '0a0b536572766963654e616d65120d50726f6365647572654e616d65'
        request = Decoder.decode(unhexlify(message), Types().as_type('KRPC.Request'))
        self.assertEqual('ServiceName', request.service)
        self.assertEqual('ProcedureName', request.procedure)

    def test_decode_value(self):
        value = Decoder.decode(unhexlify('ac02'), Types().as_type('int32'))
        self.assertEqual(int(300), value)

    def test_decode_unicode_string(self):
        value = Decoder.decode(unhexlify('03e284a2'), Types().as_type('string'))
        self.assertEqual(b'\xe2\x84\xa2'.decode('utf-8'), value)

    def test_decode_size_and_position(self):
        message = '1c'
        size,position = Decoder.decode_size_and_position(unhexlify(message))
        self.assertEqual(28, size)
        self.assertEqual(1, position)

    def test_decode_message_delimited(self):
        typ = krpc.schema.KRPC.Request
        message = '1c'+'0a0b536572766963654e616d65120d50726f6365647572654e616d65'
        request = Decoder.decode_delimited(unhexlify(message), Types().as_type('KRPC.Request'))
        self.assertEqual('ServiceName', request.service)
        self.assertEqual('ProcedureName', request.procedure)

    def test_decode_value_delimited(self):
        value = Decoder.decode_delimited(unhexlify('02'+'ac02'), Types().as_type('int32'))
        self.assertEqual(300, value)

    def test_decode_class(self):
        typ = Types().as_type('Class(ServiceName.ClassName)')
        value = Decoder.decode(unhexlify('ac02'), typ)
        self.assertTrue(isinstance(value, typ.python_type))
        self.assertEqual(300, value._object_id)

    def test_decode_class_none(self):
        typ = Types().as_type('Class(ServiceName.ClassName)')
        value = Decoder.decode(unhexlify('00'), typ)
        self.assertIsNone(value)

if __name__ == '__main__':
    unittest.main()
