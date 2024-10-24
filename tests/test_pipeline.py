import unittest

from data_pipeline.pipeline import load_clean_data, build_drug_mentions_graph

class TestPipeline(unittest.TestCase):

    def test_load_clean_data(self):
        drugs_df, pubmed_df, clinical_trials_df = load_clean_data()

        # Check that dataframes are not empty
        self.assertFalse(drugs_df.empty)
        self.assertFalse(pubmed_df.empty)
        self.assertFalse(clinical_trials_df.empty)


    def test_build_drug_mentions_graph(self):
        drugs_df, pubmed_df, clinical_trials_df = load_clean_data()
        drug_mentions = build_drug_mentions_graph(drugs_df, pubmed_df, clinical_trials_df)

        # Check that the graph contains data
        self.assertGreater(len(drug_mentions), 0)


if __name__ == '__main__':
    unittest.main()