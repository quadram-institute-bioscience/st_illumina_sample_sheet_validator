import streamlit as st
import io
import tempfile
import csv
from utils import validate_sample_sheet, ADAPTER_LIST


def app():
    st.set_page_config(page_icon="⚙️", page_title="NextSeq Sample Sheet Validator")
    st.title("NextSeq Sample Sheet Validator")
    st.info(
        "\
    This app validates and formats a NextSeq sample sheet.\n\n \
    - If the i7 and i5 sequences are not correct for demultiplexing. It will search the index name instead of the index sequence for validation.\n\n\
    - If the i7 and i5 sequences per sample are duplicated.\n\n\
    - If the sample IDs contains special characters that are not allowed.\n\n\
    - For now, only nextera_xt_v2 adapters are supported. \
    "
    )
    uploaded_file = st.file_uploader(
        "Upload Sample Sheet",
        type="csv",
        accept_multiple_files=False,
        key="uploaded_file",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

    st.selectbox("Adapter Kit", list(ADAPTER_LIST.keys()))

    if uploaded_file is not None:
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(uploaded_file.getvalue())
        tmp_file.flush()
        try:
            rs, duplicated_index = validate_sample_sheet(tmp_file.name)
            st.dataframe(rs)
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(rs)
            csv_data = buffer.getvalue()
            output_name = uploaded_file.name.split(".")[0]
            st.download_button(
                label="Download Validated Sample Sheet",
                data=csv_data.encode(),
                file_name=f"{output_name}_validated.csv",
            )
            tmp_file.close()
            if len(duplicated_index) > 0:
                st.warning(
                    f"Found duplicate index for sample {duplicated_index.get(list(duplicated_index.keys())[0])}"
                )
                st.info(
                    "Only the first sample is included in the processed sample sheet."
                )
        except Exception as e:
            st.error(e)


if __name__ == "__main__":
    app()
