# SampleSheet Validator

[![Pytest](https://github.com/quadram-institute-bioscience/st_illumina_sample_sheet_validator/actions/workflows/python-app.yml/badge.svg)](https://github.com/quadram-institute-bioscience/st_illumina_sample_sheet_validator/actions/workflows/python-app.yml)

## Overview
This little streamlit app provides a simple interface to validate the sample sheet using for demultiplexing samples from the Nextseq.

## Features
- If the i7 and i5 sequences are not correct for demultiplexing. It will search the index name instead of the index sequence for validation.

- If the i7 and i5 sequences per sample are duplicated.

- If the sample IDs contains special characters that are not allowed.

- For now, only nextera_xt_v2 adapters are supported.

## Installation & Usage
The app is deployed at: https://
