from st_nextseq_sample_sheet.utils import get_adapter
import pytest


class TestGetAdapter:
    kit_name = "nextera_xt_v2"

    # Retrieve i7 and i5 adapter sequences from a specified adapter file
    def test_retrieve_adapter_sequences(self):
        # Arrange
        adapter_kit = self.kit_name

        # Act
        result = get_adapter(adapter_kit)

        # Assert
        assert result["i7"]["N701"] == "TAAGGCGA"
        assert result["i5"]["S522"] == "TTATGCGA"

    # Adapter file with invalid format raises an exception
    def test_adapter_file_with_invalid_format(self):
        # Arrange
        adapter_kit = None
        i5_prefix = "S5"

        # Act and Assert
        with pytest.raises(Exception):
            get_adapter(adapter_kit, i5_prefix)
