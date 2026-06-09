import os
import pickle

import mlflow
import optuna
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


def get_best_model(experiment_id):
    runs = mlflow.search_runs(experiment_id)
    best_run_id = runs.sort_values("metrics.valid_f1", ascending=False)["run_id"].iloc[0]
    best_model = mlflow.sklearn.load_model("runs:/" + best_run_id + "/model")
    return best_model


def optimize_model():
    # Cargar datos y split
    df = pd.read_csv("water_potability.csv")
    X_train, X_valid, y_train, y_valid = train_test_split(
        df.drop("Potability", axis=1),
        df["Potability"],
        test_size=0.2,
        random_state=42,
    )

    # Desactivar autolog para evitar conflictos con el registro manual
    mlflow.autolog(disable=True)

    exp = mlflow.set_experiment("XGBoost_WaterPotability")
    experiment_id = exp.experiment_id

    def objective_function(trial):
        # Definir hiperparámetros a optimizar
        params = {
            "objective": "binary:logistic",
            "eval_metric": "auc",
            "max_depth": trial.suggest_int("max_depth", 3, 8),
            "learning_rate": trial.suggest_float("learning_rate", 0.001, 0.1, log=True),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 7),
            "gamma": trial.suggest_float("gamma", 0, 1),
            "n_estimators": trial.suggest_int("n_estimators", 10, 300),
        }

        run_name = (
            f"XGBoost con lr={params['learning_rate']:.4f} depth={params['max_depth']} n_est={params['n_estimators']}"
        )

        # Nombrar los runs para facilitar su identificación
        with mlflow.start_run(run_name=run_name, experiment_id=experiment_id):
            try:
                model = XGBClassifier(seed=42, **params)
                model.fit(
                    X_train,
                    y_train,
                    eval_set=[(X_train, y_train), (X_valid, y_valid)],
                    verbose=False,
                )

                f1 = f1_score(y_valid, model.predict(X_valid))

                # Registrar métrica e hiperparámetros manualmente
                mlflow.log_params(params)
                mlflow.log_metric("valid_f1", f1)

                # Loggear el modelo para que get_best_model pueda cargarlo
                mlflow.sklearn.log_model(model, "model")

            # Hacer que optuna maneje el pruning correctamente
            except optuna.exceptions.TrialPruned:
                raise

        return f1

    # Crear estudio Optuna con storage persistente
    storage = optuna.storages.RDBStorage("sqlite:///optuna_lab8.db")
    study = optuna.create_study(
        direction="maximize",
        study_name="xgb_optimization_water_potability",
        sampler=optuna.samplers.TPESampler(seed=42),
        storage=storage,
        load_if_exists=True,
    )

    # Guardar gráficos de Optuna en la carpeta plots/
    os.makedirs("plots", exist_ok=True)

    # graficar historial de optimización
    fig_op = optuna.visualization.plot_optimization_history(study)
    fig_op.write_image("plots/optimization_history.png")

    # graficar la importancia de hiperparametros
    fig_imp = optuna.visualization.plot_param_importances(study)
    fig_imp.write_image("plots/feature_importance.png")

    # graficar comportamiento de los hiperparametros
    fig_com = optuna.visualization.plot_parallel_coordinate(study)
    fig_com.write_image("plots/parallel_coordinate.png")

    study.optimize(objective_function, n_trials=30, show_progress_bar=True)

    # Obtener mejor modelo y serializar
    best_model = get_best_model(experiment_id)

    os.makedirs("models", exist_ok=True)
    model_path = "models/best_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(best_model, f)

    print(f"Mejor valid_f1: {study.best_value:.4f}")
    print(f"Modelo guardado en {model_path}")

    return best_model


if __name__ == "__main__":
    optimize_model()
