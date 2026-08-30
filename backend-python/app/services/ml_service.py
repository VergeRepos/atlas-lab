"""
Machine Learning Service
Supports classification, regression, and clustering with scikit-learn
"""

import time
import hashlib
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, KMeans
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, mean_squared_error, mean_absolute_error, r2_score,
    silhouette_score, confusion_matrix
)
from sklearn.decomposition import PCA

from ..models.database import MLMetrics, MLResult, MLExperiment


class MLService:
    """Service for running ML experiments."""

    def __init__(self):
        self.supported_classifiers = {
            'logistic_regression': LogisticRegression,
            'random_forest': RandomForestClassifier,
            'decision_tree': DecisionTreeClassifier,
            'svm': SVC,
            'knn': KNeighborsClassifier,
        }

        self.supported_regressors = {
            'linear_regression': LinearRegression,
            'random_forest_regressor': RandomForestRegressor,
            'decision_tree_regressor': DecisionTreeRegressor,
            'ridge': Ridge,
            'svr': SVR,
            'knn_regressor': KNeighborsRegressor,
        }

        self.supported_clustering = {
            'kmeans': KMeans,
            'agglomerative': AgglomerativeClustering,
        }

    def run_experiment(
        self,
        experiment: MLExperiment,
        dataset_path: str,
    ) -> MLResult:
        """Run an ML experiment and return results."""
        # Load data
        df = pd.read_csv(dataset_path)

        # Prepare features and target
        feature_cols = experiment.feature_columns
        target_col = experiment.target_column

        X = df[feature_cols].copy()
        y = df[target_col].copy() if target_col in df.columns else None

        # Handle missing values
        X = X.fillna(X.mean(numeric_only=True))
        if y is not None:
            y = y.fillna(y.mode()[0] if y.dtype == 'object' else y.mean())

        # Encode categorical features
        label_encoders = {}
        for col in X.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Run appropriate task
        if experiment.task_type == 'classification':
            result = self._run_classification(
                X_scaled, y, experiment.algorithm, experiment.parameters
            )
        elif experiment.task_type == 'regression':
            result = self._run_regression(
                X_scaled, y, experiment.algorithm, experiment.parameters
            )
        elif experiment.task_type == 'clustering':
            result = self._run_clustering(
                X_scaled, experiment.algorithm, experiment.parameters
            )
        else:
            raise ValueError(f"Unknown task type: {experiment.task_type}")

        # Feature importance and confusion matrix are already set in _run_classification

        return result

    def _run_classification(
        self,
        X: np.ndarray,
        y: pd.Series,
        algorithm: str,
        params: Dict[str, Any]
    ) -> MLResult:
        """Run a classification experiment."""
        start_time = time.time()

        # Use stratify only when y has at least 2 unique values
        unique_count = len(np.unique(y)) if hasattr(y, '__len__') else y.nunique()
        stratify_arg = y if unique_count > 1 else None

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=stratify_arg
        )

        # Encode labels
        le = LabelEncoder()
        y_train = le.fit_transform(y_train)
        y_test = le.transform(y_test)

        # Create model
        model_class = self.supported_classifiers.get(algorithm)
        if not model_class:
            raise ValueError(f"Unsupported classification algorithm: {algorithm}")

        # Get default param names without instantiating the model
        try:
            valid_param_names = model_class().get_params().keys()
        except Exception:
            valid_param_names = params.keys()
        model_params = {k: v for k, v in params.items() if k in valid_param_names}
        model = model_class(**model_params)

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None

        # Calculate metrics
        metrics = MLMetrics(
            accuracy=float(accuracy_score(y_test, y_pred)),
            precision=float(precision_score(y_test, y_pred, average='weighted', zero_division=0)),
            recall=float(recall_score(y_test, y_pred, average='weighted', zero_division=0)),
            f1=float(f1_score(y_test, y_pred, average='weighted', zero_division=0)),
        )

        if y_proba is not None and len(le.classes_) == 2:
            metrics.roc_auc = float(roc_auc_score(y_test, y_proba[:, 1]))

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        # Feature importance (for tree-based models)
        feature_importance = {}
        if hasattr(model, 'feature_importances_'):
            feature_importance = {f"feature_{i}": float(imp) for i, imp in enumerate(model.feature_importances_)}

        training_time = time.time() - start_time

        return MLResult(
            experiment_id=str(uuid.uuid4()),
            metrics=metrics,
            model_params=params,
            feature_importance=feature_importance,
            confusion_matrix=cm.tolist(),
            created_at=datetime.now(timezone.utc),
        )

    def _run_regression(
        self,
        X: np.ndarray,
        y: pd.Series,
        algorithm: str,
        params: Dict[str, Any]
    ) -> MLResult:
        """Run a regression experiment."""
        start_time = time.time()

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Create model
        model_class = self.supported_regressors.get(algorithm)
        if not model_class:
            raise ValueError(f"Unsupported regression algorithm: {algorithm}")

        # Safely get valid params without double instantiation
        try:
            valid_params = model_class().get_params().keys()
        except Exception:
            valid_params = params.keys()
        model_params = {k: v for k, v in params.items() if k in valid_params}
        model = model_class(**model_params)

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Calculate metrics
        metrics = MLMetrics(
            rmse=float(np.sqrt(mean_squared_error(y_test, y_pred))),
            mae=float(mean_absolute_error(y_test, y_pred)),
            r2=float(r2_score(y_test, y_pred)),
        )

        training_time = time.time() - start_time

        return MLResult(
            experiment_id=str(uuid.uuid4()),
            metrics=metrics,
            model_params=params,
            created_at=datetime.now(timezone.utc),
        )

    def _run_clustering(
        self,
        X: np.ndarray,
        algorithm: str,
        params: Dict[str, Any]
    ) -> MLResult:
        """Run a clustering experiment."""
        start_time = time.time()

        # Create model
        model_class = self.supported_clustering.get(algorithm)
        if not model_class:
            raise ValueError(f"Unsupported clustering algorithm: {algorithm}")

        # Safely get valid params without double instantiation
        try:
            valid_params = model_class().get_params().keys()
        except Exception:
            valid_params = params.keys()
        model_params = {k: v for k, v in params.items() if k in valid_params}
        model = model_class(**model_params)

        # Fit and predict
        labels = model.fit_predict(X)

        # Calculate metrics
        metrics = MLMetrics()
        if len(set(labels)) > 1:
            metrics.silhouette_score = float(silhouette_score(X, labels))
            metrics.inertia = float(model.inertia_) if hasattr(model, 'inertia_') else 0.0

        training_time = time.time() - start_time

        return MLResult(
            experiment_id=str(uuid.uuid4()),
            metrics=metrics,
            model_params=params,
            created_at=datetime.now(timezone.utc),
        )

    def compare_experiments(
        self, experiment_ids: List[str]
    ) -> Dict[str, Any]:
        """Compare multiple experiments side-by-side."""
        # Placeholder - would fetch experiments from database and compare
        return {
            'experiments': experiment_ids,
            'comparison': {},
        }

    def list_algorithms(self) -> Dict[str, List[str]]:
        """List all supported algorithms."""
        return {
            'classification': list(self.supported_classifiers.keys()),
            'regression': list(self.supported_regressors.keys()),
            'clustering': list(self.supported_clustering.keys()),
        }