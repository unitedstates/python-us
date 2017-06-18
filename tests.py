from __future__ import unicode_literals
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
        self.assertEqual(us.states.lookup('Maryland', field='name'),
                         us.states.MD)
        self.assertEqual(us.states.lookup('maryland', field='name'), None)
        self.assertEqual(us.states.lookup('murryland'), us.states.MD)
        self.assertNotEqual(us.states.lookup('Virginia'), us.states.MD)


class LookupTestCase(unittest.TestCase):

    def test_abbr_lookup(self):
        for state in us.STATES:
            self.assertEqual(us.states.lookup(state.abbr), state)

    def test_fips_lookup(self):
        for state in us.STATES:
            self.assertEqual(us.states.lookup(state.fips), state)

    def test_name_lookup(self):
        for state in us.STATES:
            self.assertEqual(us.states.lookup(state.name), state)


class MappingTestCase(unittest.TestCase):

    def test_mapping(self):

        states = us.STATES[:5]

        self.assertEqual(
            us.states.mapping('abbr', 'fips', states=states),
            dict((s.abbr, s.fips) for s in states))


class KnownBugsTestCase(unittest.TestCase):

    def test_kentucky_uppercase(self):
        self.assertEqual(us.states.lookup('kentucky'), us.states.KY)
        self.assertEqual(us.states.lookup('KENTUCKY'), us.states.KY)


class ShapefileTestCase(unittest.TestCase):

    def test_head(self):

        for state in us.STATES_AND_TERRITORIES:

            for region, url in state.shapefile_urls().items():
                resp = requests.head(url, allow_redirects=True)
                self.assertEqual(resp.status_code, 200)


class CountsTestCase(unittest.TestCase):

    def test_obsolete(self):
        self.assertEqual(len(us.OBSOLETE), 3)

    def test_states(self):
        self.assertEqual(len(us.STATES), 51)

    def test_territories(self):
        self.assertEqual(len(us.TERRITORIES), 5)

    def test_contiguous(self):
        # Lower 48 + DC
        self.assertEqual(len(us.STATES_CONTIGUOUS), 49)

    def test_continental(self):
        # Lower 48 + DC + Alaska
        self.assertEqual(len(us.STATES_CONTINENTAL), 50)


if __name__ == '__main__':
    unittest.main()
