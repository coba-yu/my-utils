import optuna
import xgboost as xgb
from sklearn.metrics import mean_squared_error

def optuna_xgboost(X_train, y_train, X_test, y_test):
    dtrain = xgb.DMatrix(X_train.drop(['AC', 'Dept'], axis=1), label=y_train_all)
    dtest = xgb.DMatrix(X_test.drop(['AC', 'Dept'], axis=1), label=y_test)
    evallist = [(dtest, 'eval'), (dtrain, 'train')]
    
    def objective(trial):
        params = dict(eta=trial.suggest_uniform('eta', 0.0, 1.0),
                      gamma=trial.suggest_loguniform('gamma', 1e-4, 1e-1),
                      #max_depth=trial.suggest_int('max_depth', 3, 30),
                      #min_child_weight=trial.suggest_loguniform('min_child_weight', 1e-5, 1e-1),
                      subsample=trial.suggest_uniform('subsample', 0, 1.0),
                      #colsample_bytree=trial.suggest_uniform('colsample_bytree', 0, 1.0),
                      alpha=trial.suggest_uniform('alpha', 0, 1.0), 
                      #tree_method=trial.suggest_categorical('tree_method', ['exact', 'approx', 'hist']), # gpu_hist
                      #sketch_epstrial.suggest_uniform('sketch_epstrial', 0, 1.0),
                      #scale_pos_weight, updater,refresh_leaf,process_type, grow_policy, 
                      #max_leaves=trial.suggest_int('max_depth', 0, 10),
                      #max_bin=trial.suggest_int('max_bin', 128, 512),
                      #predictor, num_parallel_tree,
                      )
        params['lambda'] = trial.suggest_uniform('lambda', 0, 1.0)
        num_round = 30
        bst = xgb.train(params, dtrain, num_round, evallist)
        y_pred = bst.predict(dtest)
        error = mean_squared_error(y_test, y_pred)
        return error
    study = optuna.create_study()  # Create a new study.
    study.optimize(objective, n_trials=100)  # Invoke optimization of the objective function. 
    print(study.best_params)
    
optuna_xgboost(X_train_all, y_train_all, X_test, y_test)
