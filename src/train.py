import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import HillClimbSearch, BIC, ExpertKnowledge, MaximumLikelihoodEstimator

def learn_structure(train_df: pd.DataFrame, target: str, max_indegree: int = 4):
    feature_cols = [c for c in train_df.columns if c != target]
    forbidden = [(target, f) for f in feature_cols]
    expert_knowledge = ExpertKnowledge(forbidden_edges=forbidden)

    hc = HillClimbSearch(train_df)
    dag = hc.estimate(
        scoring_method=BIC(train_df),
        max_indegree=max_indegree,
        expert_knowledge=expert_knowledge,
    )
    return dag

def fit_bn(train_df: pd.DataFrame, dag):
    model = DiscreteBayesianNetwork(dag.edges())
    model.fit(train_df, estimator=MaximumLikelihoodEstimator)
    return model
