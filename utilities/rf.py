'''
Class I created to apply the entire RF pipeline to the data. 
'''

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV


class RFAnalysis():
    def __init__(self, n_estimators = [*range(50,501,100)], cv_folds = 5):
        ''' RF hyperparamaeter initializations'''
        self.n_estimators = n_estimators
        self.cv_folds = cv_folds

    def train_test_split(self, X, y):
        # Focusing on the inbound text
        # Splitting, with stratify param for class balance
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.33, 
                                                            random_state = 25, stratify = y)
        return X_train, X_test, y_train, y_test
    
    def rf_pipeline(self, X_train, y_train):
        ''' Using the training data to train my Random Forest model '''
        # Initializing my pipeline
        estimators = [('model', RandomForestClassifier())]

        pipe = Pipeline(estimators)

        # These are the hyperparamaters and models I want to tune
        param_grid = [{'model': [RandomForestClassifier()], 
                    'model__n_estimators': self.n_estimators}, 
                    ]

        # 5 fold cross validation
        grid = GridSearchCV(pipe, param_grid, cv = self.cv_folds, verbose = 3)

        return grid.fit(X_train, y_train)

    def save_model(self, fitted_grid, save_directory_path: str):
        from sklearn.externals import joblib
        import datetime

        # getting string of now
        now = str(datetime.datetime.now())[:16]

        # Saving it because it took some time to run
        joblib.dump(fitted_grid, f'{save_directory_path}/{now}.pkl', compress=1)
    
    def get_results(self, fitted_grid):
        ''' Here we have a dataframe of all the fits under the different hyperparamaters '''
        return pd.DataFrame(fitted_grid.cv_results_).sort_values('mean_test_score', ascending = False)

    def get_best_model(self, fitted_grid):
        ''' Here we get the best model from the grid '''
        return fitted_grid.best_estimator_


    def evaluate_model(self, X_train, y_train, X_test, y_test, fitted_grid):
        ''' Here we evaluate the model:
        Prints out the classification report and displays a confusion matrix.
         '''
        from sklearn.metrics import ConfusionMatrixDisplay
        from sklearn.metrics import classification_report
        from sklearn.metrics import f1_score
        from sklearn.metrics import confusion_matrix
        import matplotlib.pyplot as plt

        plt.style.use('default')

        # We use the best estimator of the grid for evaluatoin
        best_model = fitted_grid.best_estimator_[0]

            # Scoring the model
        print(f'Score on train: {best_model.score(X_train, y_train)}')
        print(f'Score on test: {best_model.score(X_test, y_test)}')

        y_pred = best_model.predict(X_test)
        
        print('\nConfusion Matrix:')
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize = (10,8))
        ConfusionMatrixDisplay(cm, display_labels = y_test.unique()).plot(xticks_rotation = 'vertical', 
                            values_format = 'd')
        plt.show()
        print('\nClassification Report:')
        print(classification_report(y_test, y_pred))
        print('\nF1 Score:')
        print(f1_score(y_test, y_pred, average = None))

    def get_feature_importances(self, fitted_grid, save_directory_path: str, feature_names: list) -> pd.DataFrame:
        ''' Here we get the feature importances of the model and store it into a dataframe'''
        best_estimator = fitted_grid.best_estimator_[0]
        importances = pd.DataFrame({"Feature": feature_names, "Feature Importance": best_estimator.feature_importances_})
        importances = importances.sort_values('Feature Importance', ascending = False)

        # save the importances df
        import datetime

        # getting string of now
        now = str(datetime.datetime.now())[:16]

        importances.to_csv(save_directory_path + f"{now}.csv")

        return importances

    def visualize_feature_importances(self, importances: pd.DataFrame, topn: int = 30, title = "Feature Importances") -> None:
        import plotly.graph_objects as go
        import plotly.offline as pyo
        
        def bar(x, y, color ="#FFD700", title = "Bar Plot") -> None:
            trace1 = go.Bar(x=x,y=y, marker=dict(color=color))
            data = [trace1]
            layout = go.Layout(title=title, barmode="stack",
                        xaxis = dict(tickangle = 90,
                                    showticklabels = True,
                                    type = "category",
                                    dtick = 1))
            fig = go.Figure(data = data, layout = layout)
            fig.show()
        bar(x = importances.head(topn).Feature, y = importances.head(topn)['Feature Importance'],
            title = title)

    def example_usage(self, df, feature_names, target_name):
        ''' Here we apply the common pipeline to the data '''
        # Get the features
        X = df[feature_names]

        # Get the target
        y = df[target_name]

        # Split the data
        X_train, X_test, y_train, y_test = self.train_test_split(X, y)

        # Train the model
        fitted_grid = self.rf_pipeline(X_train, y_train)

        # Save the model
        self.save_model(fitted_grid, f'/data/models')

        # Evaluate the model
        self.evaluate_model(X_train, y_train, X_test, y_test, fitted_grid)

        # Get the feature importances
        importances = self.get_feature_importances(fitted_grid)

        return importances
