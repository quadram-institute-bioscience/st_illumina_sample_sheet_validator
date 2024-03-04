import csv
import re
from typing import Dict, List

ADAPTER_LIST = {"nextera_xt_v2": "./assets/nextera_xt_v2.csv"}


def get_adapter(adapter_kit: str, i5_prefix: str = "S5") -> Dict:
    """
    Retrieve adapter sequences from a specified adapter file and organize them into a dictionary.

    :param adapter_kit: Path to adapter file with two columns: name,sequence.
    :param i5_prefix: The prefix used to identify i5 adapters (default is "S5").
    :return: A dictionary containing the retrieved adapter sequences, organised by adapter type.
    """
    adapters: dict[str, dict] = {}
    adapters["i7"] = {}
    adapters["i5"] = {}
    adapter_file = ADAPTER_LIST[adapter_kit]
    with open(adapter_file, "r") as af:
        for line in af:
            if "name,sequence" not in line:
                name, sequence = line.strip().split(",")
                index = "i7"
                if name.startswith(i5_prefix):
                    index = "i5"
                adapters[index][name] = sequence
    return adapters


def reverse_complement(sequence: str) -> str:
    """
    Reverse complement a sequence.
    :param sequence: The sequence to reverse complement.
    :return: The reverse complement of the input sequence.
    """
    return sequence.translate(str.maketrans("ATCGNatcgn", "TAGCNtagcn"))[::-1]


def remove_special_chars(sample_id: str, replace_char: str = "-") -> str:
    """
    Remove special characters from a sample ID.
    :param sample_id: The sample ID to remove special characters from.
    :return: The sample ID with special characters removed.
    """
    return re.sub(r"[^a-zA-Z0-9\-|\_]", replace_char, sample_id)


def validate_sample_sheet(
    sample_sheet_file: str, adapter_kit: str = "nextera_xt_v2"
) -> List:
    """
    Read the sample sheet file and return a list of dictionaries containing sample information.
    :param sample_sheet_file: Path to the sample sheet file.
    :return: A list of dictionaries containing sample information.
    """
    adapters = get_adapter(adapter_kit)
    with open(sample_sheet_file, "r") as sf:
        expected_header = [
            "Sample_ID",
            "Description",
            "I7_Index_ID",
            "index",
            "I5_Index_ID",
            "index2",
            "Sample_Project",
        ]
        reader = csv.reader(sf)
        found_header = False
        samples = []
        _run_metadata = []
        to_check_sample = []
        duplicated_index = {}
        for row in reader:
            if found_header:
                (
                    sample_id,
                    description,
                    i7_index_id,
                    index,
                    i5_index_id,
                    index2,
                    sample_project,
                ) = row[:7]
                # sample id
                sample_id = remove_special_chars(sample_id)
                # description
                if description == "":
                    description = sample_id
                else:
                    description = remove_special_chars(description)
                pair_index = f"{index}+{index2}"
                if pair_index not in duplicated_index:
                    duplicated_index[pair_index] = sample_id
                else:
                    duplicated_index[pair_index] = (
                        duplicated_index[pair_index] + "," + sample_id
                    )
                    continue
                # i7
                i7_index_id = re.sub(r"A-", "", i7_index_id)
                if adapters["i7"][i7_index_id] != index:
                    to_check_sample.append(sample_id)
                    index = adapters["i7"][i7_index_id]
                # i5
                i5_index_id = re.sub(r"A-", "", i5_index_id)
                if adapters["i5"][i5_index_id] == index2:
                    to_check_sample.append(sample_id)
                    index2 = reverse_complement(adapters["i5"][i5_index_id])
                sample_project = remove_special_chars(sample_project)
                sample = ",".join(
                    [
                        sample_id,
                        description,
                        i7_index_id,
                        index,
                        i5_index_id,
                        index2,
                        sample_project,
                    ]
                )
                samples.append(sample)
            else:
                _run_metadata.append(",".join(row))
            if (
                "sample" in row[0].lower()
            ):  # this check assumes the first column contains sample ID
                headers = row
                if headers[:7] != expected_header[:7]:
                    raise ValueError(
                        f"Expected header {expected_header} but found {headers}"
                    )
                found_header = True
    _run_metadata.extend(samples)
    duplicated_index = {
        k: v for k, v in duplicated_index.items() if len(v.split(",")) > 1
    }
    return [_run_metadata, duplicated_index]
