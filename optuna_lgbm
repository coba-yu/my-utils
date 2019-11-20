import optuna
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error


def objective(trial):
    params = dict(colsample_bytree=trial.suggest_uniform('subsample', 0, 1.0),
                  learning_rate=trial.suggest_loguniform('learning_rate', 1e-4, 1e-1),
                  max_depth=trial.suggest_int('max_depth', 10, 30),
                  min_child_samples=trial.suggest_int('min_child_samples', 10, 50),
                  min_child_weight=trial.suggest_loguniform('min_child_weight', 1e-5, 1e-1),
                  min_split_gain=trial.suggest_uniform('min_split_gain', 0, 1.0),
                  n_estimators=trial.suggest_int('n_estimators', 100, 500),
                  num_leaves=trial.suggest_int('num_leaves', 20, 40),
                  reg_alpha=trial.suggest_uniform('reg_alpha', 0, 1.0), 
                  reg_lambda=trial.suggest_uniform('reg_lambda', 0, 1.0),
                  silent=trial.suggest_categorical('silent', [True, False]),
                  subsample=trial.suggest_uniform('subsample', 0, 1.0),
                  subsample_for_bin=trial.suggest_int('subsample_for_bin', 100000, 300000),
                  #subsample_freq
                  )
    regressor_obj = LGBMRegressor(**params)
    regressor_obj.fit(X_train_all, y_train_all)
    y_pred = regressor_obj.predict(X_test)
    error = mean_squared_error(y_test, y_pred)
    return error


study = optuna.create_study()  # Create a new study.
study.optimize(objective, n_trials=100)  # Invoke optimization of the objective function. 
print(study.best_params)
