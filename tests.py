import unittest
import requests

import us


class AttributeTestCase(unittest.TestCase):

    def test_attribute(self):

        for state in us.STATES_AND_TERRITORIES:
            self.assertEqual(state, getattr(us.states, state.abbr))


class MarylandLookupTestCase(unittest.TestCase):

    def test_fips(self):
        self.assertEqual(us.states.lookup('24'), us.states.MD)
        self.assertNotEqual(us.states.lookup('51'), us.states.MD)

    def test_abbr(self):
        self.assertEqual(us.states.lookup('MD'), us.states.MD)
        self.assertEqual(us.states.lookup('md'), us.states.MD)
        self.assertNotEqual(us.states.lookup('VA'), us.states.MD)
        self.assertNotEqual(us.states.lookup('va'), us.states.MD)

    def test_name(self):
        self.assertEqual(us.states.lookup('Maryland'), us.states.MD)
        self.assertEqual(us.states.lookup('maryland'), us.states.MD)
        self.assertEqual(us.states.lookup('Maryland', field='name'), us.states.MD)
        self.assertEqual(us.states.lookup('maryland', field='name'), None)
        self.assertEqual(us.states.lookup('murryland'), us.states.MD)
        self.assertNotEqual(us.states.lookup('Virginia'), us.states.MD)


class MappingTestCase(unittest.TestCase):

    def test_mapping(self):

        states = us.STATES[:5]

        self.assertEqual(
            us.states.mapping('abbr', 'fips', states=states),
            dict((s.abbr, s.fips) for s in states))


class ShapefileTestCase(unittest.TestCase):

    def test_state_head(self):

        for state in us.STATES_AND_TERRITORIES:

            for region, url in state.shapefile_urls().items():
                resp = requests.head(url)
                self.assertEqual(resp.status_code, 200)

    def test_national_head(self):

        for region, url in us.shapefile_urls().items():
            resp = requests.head(url)
            self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
