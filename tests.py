import unittest

from main import calculate_sector_tokens, rik, tiv, gy, jy, nd, identify_sector


class TestCalculateSectorTokens(unittest.TestCase):

    def test_all_sector_tokens_present(self):
        patent_tokens = {'compounds': 2, 'tube': 1, 'packaging': 3, 'box': 1, 'formulation': 2}
        expected_output = {rik: 4, tiv: 1, gy: 3, jy: 1, nd: 0}
        output = calculate_sector_tokens(patent_tokens)
        self.assertEqual(expected_output, output)

    def test_no_sector_tokens_present(self):
        patent_tokens = {'token6': 2, 'token7': 1, 'token8': 3}
        expected_output = {rik: 0, tiv: 0, gy: 0, jy: 0, nd: 6}
        output = calculate_sector_tokens(patent_tokens)
        self.assertEqual(expected_output, output)

    def test_some_sector_tokens_present(self):
        patent_tokens = {'compounds': 2, 'fiber': 1, 'token9': 3}
        expected_output = {rik: 2, tiv: 1, gy: 0, jy: 0, nd: 3}
        output = calculate_sector_tokens(patent_tokens)
        self.assertEqual(expected_output, output)


class TestIdentifySector(unittest.TestCase):

    def test_identify_rik(self):
        patent_tokens = {'compounds': 2, 'formulation': 2, 'film': 3}
        expected_output = rik
        output = identify_sector(patent_tokens)
        self.assertEqual(expected_output, output)

    def test_identify_tiv(self):
        patent_tokens = {'tube': 2, 'fiber': 2, 'bag': 3}
        expected_output = tiv
        output = identify_sector(patent_tokens)
        self.assertEqual(expected_output, output)

    def test_identify_gy(self):
        patent_tokens = {'packaging': 2, 'film': 2, 'pouch': 3}
        expected_output = gy
        output = identify_sector(patent_tokens)
        self.assertEqual(expected_output, output)

    def test_identify_jy(self):
        patent_tokens = {'box': 2, 'carton': 2, 'container': 3}
        expected_output = jy
        output = identify_sector(patent_tokens)
        self.assertEqual(expected_output, output)

    def test_identify_nd(self):
        patent_tokens = {'token1': 2, 'token2': 1, 'token3': 3}
        expected_output = nd
        output = identify_sector(patent_tokens)
        self.assertEqual(expected_output, output)

    def test_identify_tiv_with_nd_majority(self):
        patent_tokens = {'pipe': 3, 'token1': 2, 'token2': 1, 'token3': 3}
        expected_output = tiv
        output = identify_sector(patent_tokens)
        self.assertEqual(expected_output, output)


if __name__ == '__main__':
    unittest.main()