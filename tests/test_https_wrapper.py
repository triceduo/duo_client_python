from __future__ import absolute_import
from duo_client.https_wrapper import CertValidatingHTTPSConnection
import unittest
import mock
import ssl

class TestSSLContextCreation(unittest.TestCase):
    """ Test that the SSL context used to wrap sockets is configured correctly """
    def test_no_ca_certs(self):
        conn = CertValidatingHTTPSConnection('fake host')
        self.assertEqual(conn.default_ssl_context.verify_mode, ssl.CERT_NONE)

    @mock.patch('ssl.SSLContext.load_verify_locations')
    def test_with_ca_certs(self, mock_load):
        mock_load.return_value = None
        conn = CertValidatingHTTPSConnection('fake host', ca_certs='cafilepath')
        self.assertEqual(conn.default_ssl_context.verify_mode, ssl.CERT_REQUIRED)
        mock_load.assert_called_with(cafile='cafilepath')

    @mock.patch('ssl.SSLContext.load_cert_chain')
    def test_with_certfile(self, mock_load):
        mock_load.return_value = None
        CertValidatingHTTPSConnection('fake host', cert_file='certfilepath')
        mock_load.assert_called_with('certfilepath', None)

    def test_ssl2_ssl3_off(self):
        conn = CertValidatingHTTPSConnection('fake host')
        self.assertEqual(conn.default_ssl_context.options & ssl.OP_NO_SSLv2, ssl.OP_NO_SSLv2)
        self.assertEqual(conn.default_ssl_context.options & ssl.OP_NO_SSLv3, ssl.OP_NO_SSLv3)