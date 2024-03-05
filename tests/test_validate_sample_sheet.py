from st_nextseq_sample_sheet.utils import validate_sample_sheet
import pytest
import os


class TestValidateSampleSheet:
    cwd = os.path.dirname(os.path.abspath(__file__))
    sample_sheet_file = f"{cwd}/assets/sample_sheet.csv"
    sample_sheet_file_invalid_columns = f"{cwd}/assets/sample_sheet_invalid_columns.csv"

    # Read a valid sample sheet file and return a list of dictionaries containing sample information.
    def test_valid_sample_sheet(self):
        # Act
        result = validate_sample_sheet(self.sample_sheet_file)
        # Assert
        assert isinstance(result, list)

    # Read a sample sheet file with invalid column names and raise a ValueError.
    def test_invalid_column_names(self):
        # Act & Assert
        with pytest.raises(ValueError):
            validate_sample_sheet(self.sample_sheet_file_invalid_columns)

    # Read a sample sheet file with invalid indexes and raise a ValueError.
    def test_invalid_indexes(self):
        # Act & Assert
        with pytest.raises(ValueError):
            validate_sample_sheet(self.sample_sheet_file_invalid_columns)
