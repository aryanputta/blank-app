"""Isolation Forest baseline for unsupervised anomaly scoring."""

from sklearn.ensemble import IsolationForest


def build_isolation_forest(random_state: int = 42) -> IsolationForest:
    return IsolationForest(
        n_estimators=300,
        contamination=0.08,
        random_state=random_state,
        n_jobs=-1,
    )
