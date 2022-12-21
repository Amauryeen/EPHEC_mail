from lib.Mail import *
import unittest


# noinspection DuplicatedCode
class TestMail(unittest.TestCase):
    def test_sender(self):
        a = 'test@example.com'
        b = Mail(['test@example.com'], sender=a)
        self.assertEqual(b.sender, a)

        with self.assertRaises(InvalidType):
            c = []
            Mail(['test@example.com'], sender=c)

        with self.assertRaises(InvalidMail):
            d = 'test@example'
            Mail(['test@example.com'], sender=d)

    def test_receivers(self):
        a = ['test@example.com']
        b = Mail(a)
        self.assertEqual(b.receivers, a)

        with self.assertRaises(InvalidType):
            c = 'Toto'
            Mail(c)

        with self.assertRaises(InvalidSize):
            d = []
            Mail(d)

        with self.assertRaises(InvalidSize):
            e = []
            for v in range(101):
                e.append(f"{v}@example.com")

            Mail(e)

        with self.assertRaises(InvalidMail):
            f = ['test@example']
            Mail(f)

    def test_subject(self):
        a = 'bonjour'
        b = Mail(['test@example.com'], subject=a)
        self.assertEqual(b.subject, a)

        with self.assertRaises(InvalidType):
            c = []
            Mail(['test@example.com'], subject=c)

        with self.assertRaises(TooManyCharacters):
            d = []
            for v in range(201):
                d.append('a')
            Mail(['test@example.com'], ''.join(d))

    def test_body(self):
        a = 'bonjour'
        b = Mail(['test@example.com'], body=a)
        self.assertEqual(b.body, a)

        with self.assertRaises(InvalidType):
            c = []
            Mail(['test@example.com'], body=c)

        with self.assertRaises(TooManyCharacters):
            d = []
            for v in range(1001):
                d.append('a')
            Mail(['test@example.com'], ''.join(d))

    def test_cc(self):
        a = ['test@example.com']
        b = Mail(['test@example.com'], cc=a)
        self.assertEqual(b.cc, a)

        c = []
        d = Mail(['test@example.com'], cc=c)
        self.assertEqual(d.cc, c)

        with self.assertRaises(InvalidType):
            e = 'Toto'
            Mail(['test@example.com'], cc=e)

        with self.assertRaises(InvalidSize):
            f = []
            for v in range(101):
                f.append(f"{v}@example.com")

            Mail(['test@example.com'], cc=f)

        with self.assertRaises(InvalidMail):
            g = ['test@example']
            Mail(['test@example.com'], cc=g)

    def test_bcc(self):
        a = ['test@example.com']
        b = Mail(['test@example.com'], bcc=a)
        self.assertEqual(b.bcc, a)

        c = []
        d = Mail(['test@example.com'], bcc=c)
        self.assertEqual(d.bcc, c)

        with self.assertRaises(InvalidType):
            e = 'Toto'
            Mail(['test@example.com'], bcc=e)

        with self.assertRaises(InvalidSize):
            f = []
            for v in range(101):
                f.append(f"{v}@example.com")

            Mail(['test@example.com'], bcc=f)

        with self.assertRaises(InvalidMail):
            g = ['test@example']
            Mail(['test@example.com'], bcc=g)


if __name__ == '__main__':
    unittest.main()
