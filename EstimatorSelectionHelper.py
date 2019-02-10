# http://www.davidsbatista.net/blog/2018/02/23/model_optimization/


import numpy as np
import pandas as pd

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import TruncatedSVD, PCA


class EstimatorSelectionHelper:

    def __init__(self, models_dict, params_dict):
        # if not set(models_dict.keys()).issubset(set(params_dict.keys())):
        #     missing_params = list(set(models.keys()) - set(params_dict.keys()))
        #     raise ValueError(
        #         "Some estimators are missing parameters: %s" % missing_params)
        self.models = models_dict
        self.params = params_dict
        self.keys = models_dict.keys()
        #print(self.keys)
        self.best_ = {
            'estimator': [None],
            'params': {},
            'y_pred': [],
            'r': [],
        }

    def tune(self, X_train, y_train, X_test, y_test, **grid_kwargs):
        max_r = -1
        for key in self.keys:
            print("\tRunning GridSearchCV for %s." % key)
            model = self.models[key]
            params = self.params[key]

            #Pipeline the estimators
            pipeline = Pipeline([
                ('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('svd', TruncatedSVD()),
                ('clf', model),
            ])
            
            gs = GridSearchCV(pipeline, params, **grid_kwargs)
            gs.fit(X_train, y_train)

            print("\tPredicting for %s." % key)
            y_pred = gs.predict(X_test)
            r = np.corrcoef(y_pred, y_test)[0, 1]
            
            if (r > max_r):
                self.best_['estimator'] = model
                self.best_['params'] = gs.best_params_
                self.best_['r'] = r
                self.best_['y_pred'] = y_pred
            
            print('\tTuning for %s Done.' % key)
        #print(self.best_)

    

    # def score_summary(self, sort_by='mean_test_score'):
    #     frames = []
    #     for name, grid_search in self.grid_searches.items():
    #         frame = pd.DataFrame(grid_search.cv_results_)
    #         frame = frame.filter(regex='^(?!.*param_).*$')
    #         frame['estimator'] = len(frame)*[name]
    #         frames.append(frame)
    #     df = pd.concat(frames)

    #     df = df.sort_values([sort_by], ascending=False)
    #     df = df.reset_index()
    #     #df = df.drop(['rank_test_score', 'index'], 1)

    #     columns = df.columns.tolist()
    #     columns.remove('estimator')
    #     columns = ['estimator']+columns
    #     df = df[columns]
    #     return df
