"""
Data Analysis Service
CSV analysis with statistics, correlations, and automatic visualization
"""

import hashlib
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pathlib import Path
import uuid

import pandas as pd
import numpy as np
from scipy import stats

from ..models.database import (
    ColumnInfo, ColumnStatistics, CorrelationPair,
    MissingValueAnalysis, OutlierAnalysis, ChartConfig, DatasetAnalysis, Dataset
)


class DataAnalysisService:
    """Service for analyzing CSV datasets."""

    def _load_dataset(self, file_path: str) -> pd.DataFrame:
        """Load a CSV file into a pandas DataFrame."""
        return pd.read_csv(file_path)

    def analyze_dataset(
        self,
        file_path: str,
        dataset_name: str,
        project_id: str
    ) -> DatasetAnalysis:
        """Perform complete dataset analysis."""
        df = self._load_dataset(file_path)

        # Calculate checksum
        checksum = self._calculate_checksum(file_path)

        # Create dataset metadata
        columns = self._analyze_columns(df)

        # Create Dataset
        dataset = Dataset(
            id=str(uuid.uuid4()),
            project_id=project_id,
            name=dataset_name,
            file_path=file_path,
            file_type='csv',
            row_count=len(df),
            column_count=len(df.columns),
            columns=columns,
            checksum=checksum,
        )

        # Perform analysis
        summary = self._calculate_summary(df)
        statistics = self._calculate_statistics(df)
        correlations = self._calculate_correlations(df)
        missing_values = self._analyze_missing_values(df)
        outliers = self._detect_outliers(df)
        charts = self._generate_charts(df)

        return DatasetAnalysis(
            id=str(uuid.uuid4()),
            dataset_id=dataset.id,
            summary=summary,
            statistics=statistics,
            correlations=correlations,
            missing_values=missing_values,
            outliers=outliers,
            charts=charts,
            created_at=datetime.now(timezone.utc),
        )

    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA-256 checksum of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _analyze_columns(self, df: pd.DataFrame) -> List[ColumnInfo]:
        """Analyze each column and determine its type."""
        columns = []

        for col_name in df.columns:
            col = df[col_name]
            dtype = col.dtype

            # Determine column type
            if pd.api.types.is_numeric_dtype(dtype):
                if pd.api.types.is_integer_dtype(dtype):
                    col_type = 'numeric'
                else:
                    col_type = 'numeric'
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                col_type = 'datetime'
            elif pd.api.types.is_bool_dtype(dtype):
                col_type = 'boolean'
            else:
                unique_ratio = col.nunique() / len(col) if len(col) > 0 else 0
                if unique_ratio > 0.5:
                    col_type = 'text'
                else:
                    col_type = 'categorical'

            column_info = ColumnInfo(
                name=col_name,
                type=col_type,
                nullable=col.isnull().any(),
                unique_count=col.nunique(),
                null_count=col.isnull().sum(),
                sample_values=col.head(5).tolist(),
            )
            columns.append(column_info)

        return columns

    def _calculate_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate dataset summary statistics."""
        return {
            'row_count': len(df),
            'column_count': len(df.columns),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist(),
            'total_missing': int(df.isnull().sum().sum()),
            'memory_usage_bytes': int(df.memory_usage(deep=True).sum()),
            'duplicate_rows': int(df.duplicated().sum()),
        }

    def _calculate_statistics(self, df: pd.DataFrame) -> List[ColumnStatistics]:
        """Calculate statistics for each column."""
        statistics = []

        for col_name in df.columns:
            col = df[col_name]
            is_numeric = pd.api.types.is_numeric_dtype(col.dtype)

            stat = ColumnStatistics(
                column=col_name,
                type=str(col.dtype),
                count=len(col),
                null_count=int(col.isnull().sum()),
                unique_count=col.nunique(),
            )

            if is_numeric:
                # Convert to numeric, handling non-numeric strings
                numeric_col = pd.to_numeric(col, errors='coerce').dropna()

                if len(numeric_col) > 0:
                    stat.mean = float(numeric_col.mean())
                    stat.std = float(numeric_col.std())
                    stat.min = float(numeric_col.min())
                    stat.max = float(numeric_col.max())
                    stat.median = float(numeric_col.median())

                    # Calculate distribution type based on skewness
                    if len(numeric_col) > 2:
                        skewness = float(stats.skew(numeric_col))
                        if abs(skewness) < 0.5:
                            stat.distribution = 'normal'
                        elif skewness > 0:
                            stat.distribution = 'right_skewed'
                        else:
                            stat.distribution = 'left_skewed'

                    # Mode
                    if len(numeric_col) > 0:
                        mode_val = numeric_col.mode()
                        if len(mode_val) > 0:
                            stat.mode = float(mode_val.iloc[0])

            statistics.append(stat)

        return statistics

    def _calculate_correlations(
        self, df: pd.DataFrame, max_pairs: int = 20
    ) -> List[CorrelationPair]:
        """Calculate correlations between numeric columns."""
        correlations = []

        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.shape[1] < 2:
            return correlations

        # Get correlation matrix
        corr_matrix = numeric_df.corr()

        # Get column pairs
        cols = numeric_df.columns.tolist()

        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                col1, col2 = cols[i], cols[j]
                corr_value = corr_matrix.loc[col1, col2]
                if pd.notna(corr_value):
                    # Calculate p-value
                    valid_data = df[[col1, col2]].dropna()
                    if len(valid_data) > 2:
                        try:
                            _, p_value = stats.pearsonr(valid_data[col1], valid_data[col2])
                        except Exception:
                            p_value = 1.0
                    else:
                        p_value = 1.0

                    correlations.append(CorrelationPair(
                        column1=col1,
                        column2=col2,
                        correlation=float(corr_value),
                        p_value=float(p_value),
                        significant=p_value < 0.05,
                    ))

                    if len(correlations) >= max_pairs:
                        return correlations

        return correlations

    def _analyze_missing_values(self, df: pd.DataFrame) -> MissingValueAnalysis:
        """Analyze missing values in the dataset."""
        missing_columns = []
        total_missing = 0

        for col_name in df.columns:
            col = df[col_name]
            missing_count = int(col.isnull().sum())
            total_missing += missing_count

            if missing_count > 0:
                missing_columns.append({
                    'column': col_name,
                    'missing_count': missing_count,
                    'missing_percent': float(missing_count / len(df) * 100),
                })

        return MissingValueAnalysis(
            total_missing=total_missing,
            columns=missing_columns,
        )

    def _detect_outliers(self, df: pd.DataFrame) -> OutlierAnalysis:
        """Detect outliers in numeric columns using IQR method."""
        numeric_df = df.select_dtypes(include=[np.number])
        outliers_by_column = []
        total_outliers = 0

        for col_name in numeric_df.columns:
            col = pd.to_numeric(numeric_df[col_name], errors='coerce').dropna()

            if len(col) < 4:
                continue

            # IQR method
            q1 = col.quantile(0.25)
            q3 = col.quantile(0.75)
            iqr = q3 - q1

            if iqr > 0:
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                outliers = col[(col < lower_bound) | (col > upper_bound)]
                if len(outliers) > 0:
                    outliers_by_column.append({
                        'column': col_name,
                        'outlier_count': int(len(outliers)),
                        'outlier_percent': float(len(outliers) / len(col) * 100),
                        'lower_bound': float(lower_bound),
                        'upper_bound': float(upper_bound),
                    })
                    total_outliers += len(outliers)

        return OutlierAnalysis(
            method='iqr',
            total_outliers=total_outliers,
            by_column=outliers_by_column,
        )

    def _generate_charts(self, df: pd.DataFrame) -> List[ChartConfig]:
        """Generate chart configurations for visualizations."""
        charts = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # Histograms for numeric columns
        for col in numeric_cols[:10]:  # Limit to 10
            charts.append(ChartConfig(
                type='histogram',
                title=f'Distribution of {col}',
                x_column=col,
                config={'bins': 30, 'color': '#3b82f6'},
            ))

        # Scatter plots for correlated pairs
        if len(numeric_cols) >= 2:
            for i in range(min(5, len(numeric_cols) - 1)):
                charts.append(ChartConfig(
                    type='scatter',
                    title=f'{numeric_cols[i]} vs {numeric_cols[i+1]}',
                    x_column=numeric_cols[i],
                    y_column=numeric_cols[i+1] if i + 1 < len(numeric_cols) else numeric_cols[0],
                    config={'color': '#3b82f6'},
                ))

        # Bar charts for categorical columns
        for col in categorical_cols[:5]:
            charts.append(ChartConfig(
                type='bar',
                title=f'{col} Frequency',
                x_column=col,
                config={'color': '#10b981'},
            ))

        return charts

    def get_preview(
        self, file_path: str, n_rows: int = 10
    ) -> Dict[str, Any]:
        """Get a preview of the dataset."""
        df = pd.read_csv(file_path, nrows=n_rows + 1)
        total_rows = len(pd.read_csv(file_path, usecols=[0]))  # Quick row count

        columns = []
        for col_name in df.columns:
            col = df[col_name]
            columns.append({
                'name': col_name,
                'dtype': str(col.dtype),
                'sample': col.head(3).tolist(),
                'non_null_count': int(col.iloc[:n_rows].notna().sum()),
            })

        return {
            'columns': columns,
            'row_count': total_rows,
            'preview_rows': df.head(n_rows).to_dict('records'),
        }