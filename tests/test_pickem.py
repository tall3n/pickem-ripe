from unittest import TestCase, mock, main

import pickem


class TestPickem(TestCase):
            
    def test_ip_valid_null(self):
        p = pickem.Pickem(None)
        self.assertFalse(p.ip_valid, "Should be false")

    def test_ip_valid_invalid_arg(self):
        p = pickem.Pickem("bad")
        self.assertFalse(p.ip_valid, "Should be false")

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
