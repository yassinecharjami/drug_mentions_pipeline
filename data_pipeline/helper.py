"""
Helper contains utility functions for drug mention detection.

Main functions:
- find_drug_in_titles: Find drugs mention in the column title in pubmed and clinical trials
- simplify_drug_mentions: Simplify the graph of drug_mentions and remove complexity
- find_journal_with_most_drug_mentions: Find the journal with most different drugs mentions
- find_drugs_only_pubmed: Find the drugs mentioned only in pubmed

Author: Yassine Charjami
"""


from collections import defaultdict
from datetime import date
import json
import os

def find_drug_in_titles(drug, title_df, title_column):
    """
    Find drugs mention in the column title in pubmed and clinical trials dataframes

    Parameters:
    drug (str): contains the drug to be found in the titles
    title_df (DataFrame): the dataframe where to search the drug name
    title_column (str): the name of the column of titles

    Returns: DataFrame contains the rows where the drug is mentionned in title column
    """
    return title_df[title_df[title_column].str.contains(drug, case=False)]

def simplify_drug_mentions(drug_mentions):
    """
    Simplify the graph of drug_mentions and remove complexity

    Parameters:
    drug_mentions (dict): graph of each drug with its mentions in pubmed and clinical trials

    Returns: dict contains a simplified representation of drug mentions
    """
    simplified_drug_mentions = defaultdict(list)

    for drug, mentions in drug_mentions.items():

        for pubmed in mentions['pubmed']:
            simplified_drug_mentions[drug].append({
                'journal': pubmed['journal'],
                'date': pubmed['date'],
                'source': 'pubMed'
            })

        for clinical_trial in mentions['clinicalTrials']:
            simplified_drug_mentions[drug].append({
                'journal': clinical_trial['journal'],
                'date': clinical_trial['date'],
                'source': 'clinicalTrials'
            })

    return simplified_drug_mentions


def find_journal_with_most_drug_mentions(drug_mentions):
    """
    Find the journal with most different drugs mentions

    Parameters:
    drug_mentions (dict): graph of each drug with its mentions in pubmed and clinical trials

    Returns: str contains the journal with most different drugs mentions
    """
    journal_drug = defaultdict(set)

    for drug, mentions in drug_mentions.items():
        for mention in mentions:
            journal_drug[mention['journal']].add(drug)

    return max(journal_drug, key=lambda k: len(journal_drug[k]))

def find_drugs_only_pubmed(drug_mentions):
    """
    Find the drugs mentioned only in pubmed

    Parameters:
    drug_mentions (dict): graph of each drug with its mentions in pubmed and clinical trials

    Returns: set contains the drugs mentioned only in pubmed
    """
    pubmed_drugs = set()
    clinical_trials_drugs = set()

    for drug, mentions in drug_mentions.items():
        for mention in mentions:
            if mention['source'] == 'pubmed':
                pubmed_drugs.add(drug)
            else:
                clinical_trials_drugs.add(drug)

    return pubmed_drugs.difference(clinical_trials_drugs)

def custom_serializer(obj):
    """
    Custom serializer to handle dates

    Parameters:
    obj: the object to be serialized

    Returns: object isoformated if it's an instance of date
    """
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} is not serializable")

def save_as_json(data, output_path):
    """
    Save data in files in json format

    Parameters:
    data: dict the data to be saved in json format
    output_path: path where the data will be saved
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, default=custom_serializer, ensure_ascii=False ,indent=4)
