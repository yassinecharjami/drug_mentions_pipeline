import unittest
import pandas as pd

from data_pipeline.helper import find_drug_in_titles, find_journal_with_most_drug_mentions, find_drugs_only_pubmed


class TestUtils(unittest.TestCase):

    def test_find_drug_in_titles(self):
        test_data = {'title': ['Hello Doliprane for sale', 'Voltarin used']}
        df = pd.DataFrame(test_data)
        result = find_drug_in_titles('doliprane', df, 'title')
        self.assertEqual(len(result), 1)

    def test_find_journal_with_most_drug_mentions(self):
        test_drug_mentions = {
            'doliprane': [{'journal': 'journal med', 'source': 'pubmed'}],
            'voltarin': [{'journal': 'journal med', 'source': 'pubmed'}],
            'fervex': [{'journal': 'journal science', 'source': 'pubmed'}]
        }

        journal = find_journal_with_most_drug_mentions(test_drug_mentions)
        self.assertEqual(journal, 'journal med')

    def test_find_drugs_only_pubmed(self):
        test_drug_mentions = {
            'doliprane': [{'journal': 'journal med', 'source': 'pubmed'}],
            'voltarin': [{'journal': 'journal med', 'source': 'pubmed'}],
            'fervex': [{'journal': 'journal science', 'source': 'pubmed'}],
            'paraceta': [{'journal': 'journal science', 'source': 'clinicalTrials'}],
            'aspigique': [{'journal': 'journal med', 'source': 'clinicalTrials'}]
        }

        only_pubmed = find_drugs_only_pubmed(test_drug_mentions)
        self.assertSetEqual(only_pubmed, {'doliprane', 'voltarin', 'fervex'})
