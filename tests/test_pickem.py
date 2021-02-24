from unittest import TestCase, mock, main
from requests.exceptions import Timeout
import pickem


class TestPickem(TestCase):
    def test_http_headers(self):
        p = pickem.Pickem("199.127.92.1")
        self.assertTrue("'Content-Type': 'application/json'", str(p.headers))

    def test_http_none_return(self):
        with mock.patch('pickem.Pickem.get_cidr_list') as mock_get:
            p = pickem.Pickem("199.127.92.1")
            mock_get.return_value = None
            self.assertEqual(p.source_cidr_list, [])
            self.assertEqual(p.find_ip()[0], False)
            self.assertEqual(p.find_ip()[1], "")
    def test_http_non_200(self):
        with mock.patch("pickem.Pickem.get_cidr_list") as mock_get:
            p = pickem.Pickem("199.127.92.1")
            class mock_response():
                @property
                def status_code(self):
                    return 404
            mock_get.return_value = mock_response
            self.assertEqual(p.source_cidr_list, [])
    def test_ip_valid_null(self):
        p = pickem.Pickem(None)
        self.assertEqual(p.ip_valid, False)

    def test_ip_valid_invalid_arg(self):
        p = pickem.Pickem("bad")
        self.assertEqual(p.ip_valid, False)

    def test_source_cidr_list(self):
        p = pickem.Pickem("199.127.92.1")
        self.assertNotEqual(p.source_cidr_list, [], "List should not be empty")

    def test_source_cidr_list_type_return(self):
        p = pickem.Pickem("199.127.92.1")
        self.assertIsInstance(p.source_cidr_list, list)

    def test_octest_creation(self):
        p = pickem.Pickem("199.127.92.1")
        self.assertEqual(p.first_two_octets, "199.127")


if __name__ == '__main__':
    main()
