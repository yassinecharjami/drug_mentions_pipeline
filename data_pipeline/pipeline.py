"""
Pipeline to detect drug mentions in medical publications and clinical trials.

Main functions:
- load_clean_data: Load and clean data from input csv and json files
- drug_mentions_graph: represent the drugs and their mentions in pubmed and clinical trials
- run_pipeline: Main function to run the different steps of the pipeline

Author: Yassine Charjami
"""


import logging
from collections import defaultdict
import pandas as pd

from data_pipeline.helper import find_drug_in_titles, simplify_drug_mentions, find_journal_with_most_drug_mentions, find_drugs_only_pubmed, save_as_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def load_clean_data():
    """
    Load and clean data from input csv and json files

    Returns: Cleaned dataframes drugs, pubmed and clinical trials
    """
    # Load dataframes
    logging.info("Start loading files")
    drugs_df = pd.read_csv("data/raw/drugs.csv")
    pubmed_csv = pd.read_csv("data/raw/pubmed.csv")
    pubmed_json = pd.read_json("data/raw/pubmed.json")
    clinical_trials_df = pd.read_csv("data/raw/clinical_trials.csv")

    # Cleaning input dataframes
    logging.info("Start cleaning data")
    pubmed_csv["date"] = pd.to_datetime(pubmed_csv["date"], format="mixed")
    pubmed_json["id"] = pd.to_numeric(pubmed_json["id"])
    clinical_trials_df["date"] = pd.to_datetime(
        clinical_trials_df["date"], format="mixed"
    )
    clinical_trials_df["scientific_title"] = clinical_trials_df[
        "scientific_title"
    ].str.strip()
    clinical_trials_df["scientific_title"] = clinical_trials_df[
        "scientific_title"
    ].replace("", None)
    clinical_trials_df["journal"] = clinical_trials_df["journal"].replace(
        r"\\xc3\\x28", "", regex=True
    )

    # Drop empty values
    drugs_df.dropna(inplace=True)
    pubmed_csv.dropna(inplace=True)
    pubmed_json.dropna(inplace=True)
    clinical_trials_df.dropna(inplace=True)

    # Cast pubmed_js date and union wuth pubmed_csv
    pubmed_json["id"] = pubmed_json["id"].astype("int64")
    pubmed_df = pd.concat([pubmed_csv, pubmed_json])
    clinical_trials_df["date"] = clinical_trials_df[
        "date"
    ].dt.date  # convert to date in order to prevent timestamp conversion when convert to dict
    pubmed_df["date"] = pubmed_df["date"].dt.date

    # Drop duplicates
    drugs_df.drop_duplicates(inplace=True)
    pubmed_df.drop_duplicates(inplace=True)
    clinical_trials_df.drop_duplicates(inplace=True)

    logging.info("Files successfully loaded and cleaned")
    return drugs_df, pubmed_df, clinical_trials_df


def build_drug_mentions_graph(drugs_df, pubmed_df, clinical_trials_df):
    """
    Build a graph representing the drugs and their mentions in pubmed and clinical trials

    Parameters:
    drugs_df (DataFrame): contains the list of drugs
    pubmed_df (DataFrame): contains the medical publications articles
    clinical_trials_df (DataFrame): contains the clinical trials articles

    Returns: dict to associate each drug with its mentions in pubmed and clinical_trials
    """
    logging.info("Start building drug mentions graph")
    drug_mentions = defaultdict()

    for _, row in drugs_df.iterrows():
        drug = row["drug"]
        pubmed_mentions = find_drug_in_titles(drug, pubmed_df, "title")
        clinical_trials_mentions = find_drug_in_titles(
            drug, clinical_trials_df, "scientific_title"
        )

        drug_mentions[drug] = {
            "pubmed": pubmed_mentions[["journal", "date"]].to_dict("records"),
            "clinicalTrials": clinical_trials_mentions[["journal", "date"]].to_dict(
                "records"
            ),
        }
    logging.info("drug mentions graph built successfully")
    return drug_mentions


def run_pipeline():
    """
    Main function to run the different steps of the pipeline
    """
    drugs_df, pubmed_df, clinical_trials_df = load_clean_data()
    drug_mentions = build_drug_mentions_graph(drugs_df, pubmed_df, clinical_trials_df)

    # Simplified graph of drug_mentions
    simplified_drug_mentions = simplify_drug_mentions(drug_mentions)

    # save drug_mentions and simplified graph of drug mentions
    save_as_json(drug_mentions, "data/output/drug_mentions.json")
    save_as_json(
        simplified_drug_mentions, "data/output/simplified_drug_mentions.json"
    )

    # Bonus
    journal_with_most_drug_mentions = find_journal_with_most_drug_mentions(
        simplified_drug_mentions
    )
    drugs_only_pubmed = find_drugs_only_pubmed(simplified_drug_mentions)

    # save journal_with_most_drug_mentions and drugs_only_pubmed
    save_as_json(
        {"journal_with_most_drug_mentions": journal_with_most_drug_mentions},
        "data/output/most_drug_mentions_journal",
    )
    save_as_json(
        list(drugs_only_pubmed), "data/output/drugs_only_pubmed.json"
    )


if __name__ == "__main__":
    logging.info("Starting pipeline")
    run_pipeline()
    logging.info("End of processing")
