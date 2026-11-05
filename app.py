
import io
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="DataClean Studio",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        font-weight: 600;
    }

    [data-testid="stMetric"] {
        background-color: rgba(128,128,128,0.08);
        padding: 18px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.18);
    }

    .hero {
        padding: 25px;
        border-radius: 12px;
        background: linear-gradient(
            120deg,
            rgba(40,90,150,0.20),
            rgba(90,60,150,0.15)
        );
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 25px;
    }

    .hero p {
        color: #9CA3AF;
        font-size: 15px;
    }

    .section-gap {
        margin-top: 20px;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>DataClean Studio</h1>
    <p>
        A professional platform for data cleaning,
        preprocessing, analysis and visualization.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def load_data(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    elif file_name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)

    else:
        raise ValueError("Unsupported file format.")


def export_csv(data):
    return data.to_csv(index=False).encode("utf-8")


def export_excel(data):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        data.to_excel(
            writer,
            index=False,
            sheet_name="Cleaned Data"
        )

    return output.getvalue()


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

st.subheader("Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is None:

    st.info("Upload a dataset to start cleaning.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Data Inspection")
        st.write(
            "Explore dataset structure, columns, "
            "data types and statistical information."
        )

    with col2:
        st.markdown("### Data Cleaning")
        st.write(
            "Handle missing values, remove duplicates "
            "and transform data."
        )

    with col3:
        st.markdown("### Data Export")
        st.write(
            "Download your cleaned dataset in CSV "
            "or Excel format."
        )

    st.stop()


# --------------------------------------------------
# LOAD DATA INTO SESSION STATE
# --------------------------------------------------

try:

    if (
        "file_name" not in st.session_state
        or st.session_state.file_name != uploaded_file.name
    ):

        data = load_data(uploaded_file)

        st.session_state.original_df = data.copy()
        st.session_state.df = data.copy()
        st.session_state.file_name = uploaded_file.name
        st.session_state.clean_log = []

except Exception as error:

    st.error(f"Unable to load dataset: {error}")
    st.stop()


df = st.session_state.df


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("DataClean Studio")

    st.caption("Data Processing Dashboard")

    st.divider()

    st.write("Current Dataset")
    st.code(uploaded_file.name)

    st.write(f"Total Rows: {len(df)}")
    st.write(f"Total Columns: {len(df.columns)}")

    st.divider()

    if st.button("Reset to Original", use_container_width=True):

        st.session_state.df = (
            st.session_state.original_df.copy()
        )

        st.session_state.clean_log = []

        st.rerun()

    st.caption(
        "All changes are applied to a working copy "
        "of your original dataset."
    )


# --------------------------------------------------
# DASHBOARD TABS
# --------------------------------------------------

overview, cleaning, visualization, history, export = st.tabs([
    "Overview",
    "Data Cleaning",
    "Visualization",
    "Cleaning History",
    "Export Data"
])


# ==================================================
# TAB 1: OVERVIEW
# ==================================================

with overview:

    st.header("Dataset Overview")

    missing_count = int(df.isna().sum().sum())

    duplicate_count = int(df.duplicated().sum())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Rows", f"{len(df):,}")

    col2.metric("Total Columns", f"{len(df.columns):,}")

    col3.metric("Missing Values", f"{missing_count:,}")

    col4.metric("Duplicate Rows", f"{duplicate_count:,}")

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True
    )

    left, right = st.columns(2)

    with left:

        st.subheader("Column Information")

        column_info = pd.DataFrame({
            "Column": df.columns.astype(str),
            "Data Type": df.dtypes.astype(str).values,
            "Non-Null Values": df.notna().sum().values,
            "Missing Values": df.isna().sum().values,
            "Unique Values": df.nunique().values
        })

        st.dataframe(
            column_info,
            use_container_width=True,
            hide_index=True
        )

    with right:

        st.subheader("Statistical Summary")

        st.dataframe(
            df.describe(include="all").transpose(),
            use_container_width=True
        )


# ==================================================
# TAB 2: DATA CLEANING
# ==================================================

with cleaning:

    st.header("Data Cleaning")

    # ----------------------------------------------
    # MISSING VALUES
    # ----------------------------------------------

    st.subheader("1. Handle Missing Values")

    missing_values = df.isna().sum()

    missing_values = missing_values[
        missing_values > 0
    ]

    if missing_values.empty:

        st.success("No missing values found.")

    else:

        st.dataframe(
            missing_values.rename(
                "Missing Values"
            ).to_frame(),
            use_container_width=True
        )

        with st.form("missing_form"):

            selected_column = st.selectbox(
                "Select Column",
                missing_values.index.tolist()
            )

            strategy = st.selectbox(
                "Select Cleaning Method",
                [
                    "Drop Rows",
                    "Fill with Mean",
                    "Fill with Median",
                    "Fill with Mode",
                    "Fill with Custom Value"
                ]
            )

            custom_value = st.text_input(
                "Custom Value"
            )

            submit_missing = st.form_submit_button(
                "Apply Cleaning"
            )

        if submit_missing:

            updated_df = df.copy()

            try:

                if strategy == "Drop Rows":

                    updated_df = updated_df.dropna(
                        subset=[selected_column]
                    )

                elif strategy == "Fill with Mean":

                    if not pd.api.types.is_numeric_dtype(
                        updated_df[selected_column]
                    ):
                        st.error(
                            "Mean requires a numeric column."
                        )
                        st.stop()

                    updated_df[selected_column] = (
                        updated_df[selected_column].fillna(
                            updated_df[selected_column].mean()
                        )
                    )

                elif strategy == "Fill with Median":

                    if not pd.api.types.is_numeric_dtype(
                        updated_df[selected_column]
                    ):
                        st.error(
                            "Median requires a numeric column."
                        )
                        st.stop()

                    updated_df[selected_column] = (
                        updated_df[selected_column].fillna(
                            updated_df[selected_column].median()
                        )
                    )

                elif strategy == "Fill with Mode":

                    modes = updated_df[
                        selected_column
                    ].mode(dropna=True)

                    if modes.empty:
                        st.error("No mode is available.")
                        st.stop()

                    updated_df[selected_column] = (
                        updated_df[selected_column].fillna(
                            modes.iloc[0]
                        )
                    )

                elif strategy == "Fill with Custom Value":

                    updated_df[selected_column] = (
                        updated_df[selected_column].fillna(
                            custom_value
                        )
                    )

                st.session_state.df = updated_df

                st.session_state.clean_log.append(
                    f"{strategy} applied to {selected_column}"
                )

                st.success("Missing values handled successfully.")

                st.rerun()

            except Exception as error:

                st.error(f"Cleaning failed: {error}")

    st.divider()

    # ----------------------------------------------
    # DUPLICATES
    # ----------------------------------------------

    st.subheader("2. Remove Duplicate Rows")

    duplicate_count = int(df.duplicated().sum())

    st.write(
        f"Detected duplicate rows: {duplicate_count}"
    )

    if st.button(
        "Remove Duplicate Rows",
        disabled=duplicate_count == 0
    ):

        st.session_state.df = (
            df.drop_duplicates().reset_index(drop=True)
        )

        st.session_state.clean_log.append(
            f"Removed {duplicate_count} duplicate rows"
        )

        st.success("Duplicate rows removed.")

        st.rerun()

    st.divider()

    # ----------------------------------------------
    # COLUMN MANAGEMENT
    # ----------------------------------------------

    st.subheader("3. Column Management")

    with st.form("column_form"):

        selected_column = st.selectbox(
            "Select Column",
            df.columns.tolist()
        )

        new_name = st.text_input(
            "New Column Name"
        )

        delete_column = st.checkbox(
            "Delete Selected Column"
        )

        submit_column = st.form_submit_button(
            "Apply Column Changes"
        )

    if submit_column:

        updated_df = df.copy()

        if delete_column:

            if len(df.columns) == 1:

                st.error(
                    "At least one column must remain."
                )

            else:

                updated_df = updated_df.drop(
                    columns=[selected_column]
                )

                st.session_state.clean_log.append(
                    f"Deleted column {selected_column}"
                )

                st.session_state.df = updated_df

                st.success("Column deleted.")

                st.rerun()

        elif new_name.strip():

            new_name = new_name.strip()

            if (
                new_name in updated_df.columns
                and new_name != selected_column
            ):

                st.error(
                    "This column name already exists."
                )

            else:

                updated_df = updated_df.rename(
                    columns={
                        selected_column: new_name
                    }
                )

                st.session_state.df = updated_df

                st.session_state.clean_log.append(
                    f"Renamed {selected_column} to {new_name}"
                )

                st.success("Column renamed.")

                st.rerun()

    st.divider()

    # ----------------------------------------------
    # DATA TYPE CONVERSION
    # ----------------------------------------------

    st.subheader("4. Data Type Conversion")

    with st.form("dtype_form"):

        type_column = st.selectbox(
            "Select Column",
            df.columns.tolist(),
            key="type_column"
        )

        target_type = st.selectbox(
            "Target Data Type",
            [
                "String",
                "Integer",
                "Float",
                "Datetime"
            ]
        )

        submit_type = st.form_submit_button(
            "Convert Data Type"
        )

    if submit_type:

        updated_df = df.copy()

        try:

            if target_type == "String":

                updated_df[type_column] = (
                    updated_df[type_column].astype("string")
                )

            elif target_type == "Integer":

                updated_df[type_column] = (
                    pd.to_numeric(
                        updated_df[type_column],
                        errors="raise"
                    ).astype("Int64")
                )

            elif target_type == "Float":

                updated_df[type_column] = (
                    pd.to_numeric(
                        updated_df[type_column],
                        errors="raise"
                    ).astype(float)
                )

            elif target_type == "Datetime":

                updated_df[type_column] = pd.to_datetime(
                    updated_df[type_column],
                    errors="raise"
                )

            st.session_state.df = updated_df

            st.session_state.clean_log.append(
                f"Converted {type_column} to {target_type}"
            )

            st.success("Data type converted successfully.")

            st.rerun()

        except Exception as error:

            st.error(f"Conversion failed: {error}")

    st.divider()

    # ----------------------------------------------
    # OUTLIER DETECTION
    # ----------------------------------------------

    st.subheader("5. Outlier Detection using IQR")

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if not numeric_columns:

        st.info("No numeric columns available.")

    else:

        outlier_column = st.selectbox(
            "Select Numeric Column",
            numeric_columns
        )

        values = df[outlier_column].dropna()

        if len(values) >= 4:

            q1 = values.quantile(0.25)

            q3 = values.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr

            upper_bound = q3 + 1.5 * iqr

            outlier_mask = (
                (df[outlier_column] < lower_bound)
                | (df[outlier_column] > upper_bound)
            )

            outlier_count = int(outlier_mask.sum())

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Detected Outliers",
                outlier_count
            )

            col2.metric(
                "Lower Bound",
                f"{lower_bound:.3f}"
            )

            col3.metric(
                "Upper Bound",
                f"{upper_bound:.3f}"
            )

            if st.button(
                "Remove Detected Outliers",
                disabled=outlier_count == 0
            ):

                st.session_state.df = (
                    df.loc[~outlier_mask].reset_index(drop=True)
                )

                st.session_state.clean_log.append(
                    f"Removed {outlier_count} outliers from {outlier_column}"
                )

                st.success("Outliers removed.")

                st.rerun()

        else:

            st.info(
                "At least four numeric values are required."
            )


# ==================================================
# TAB 3: VISUALIZATION
# ==================================================

with visualization:

    st.header("Data Visualization")

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if numeric_columns:

        selected_chart_column = st.selectbox(
            "Select Numeric Column",
            numeric_columns,
            key="visual_column"
        )

        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Histogram",
                "Box Plot",
                "Line Chart"
            ]
        )

        if chart_type == "Histogram":

            fig = px.histogram(
                df,
                x=selected_chart_column,
                title=f"Distribution of {selected_chart_column}"
            )

        elif chart_type == "Box Plot":

            fig = px.box(
                df,
                y=selected_chart_column,
                title=f"Box Plot of {selected_chart_column}"
            )

        else:

            fig = px.line(
                df.reset_index(),
                x="index",
                y=selected_chart_column,
                title=f"{selected_chart_column} by Row"
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No numeric columns available for visualization."
        )

    st.divider()

    st.subheader("Missing Values Analysis")

    missing_data = df.isna().sum().reset_index()

    missing_data.columns = [
        "Column",
        "Missing Values"
    ]

    if missing_data["Missing Values"].sum() > 0:

        fig = px.bar(
            missing_data,
            x="Column",
            y="Missing Values",
            title="Missing Values by Column"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.success("No missing values found.")


# ==================================================
# TAB 4: CLEANING HISTORY
# ==================================================

with history:

    st.header("Cleaning History")

    if st.session_state.clean_log:

        for index, operation in enumerate(
            st.session_state.clean_log,
            start=1
        ):

            st.write(f"{index}. {operation}")

    else:

        st.info(
            "No cleaning operations have been performed yet."
        )


# ==================================================
# TAB 5: EXPORT DATA
# ==================================================

with export:

    st.header("Export Cleaned Dataset")

    st.write(
        "Review your cleaned dataset before downloading."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Final Rows",
            f"{len(df):,}"
        )

    with col2:

        st.metric(
            "Final Columns",
            f"{len(df.columns):,}"
        )

    st.divider()

    st.subheader("Final Dataset Preview")

    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="Download CSV",
            data=export_csv(df),
            file_name="cleaned_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:

        st.download_button(
            label="Download Excel",
            data=export_excel(df),
            file_name="cleaned_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "DataClean Studio | Data Cleaning and Preprocessing Platform"
)
