from os import unlink
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from optuna.storages import RDBStorage
from typing_extensions import Literal
from typing_extensions import NamedTuple
from etna.auto import Auto
from etna.auto.auto import _Callback
from etna.auto.auto import _Initializer
from etna.metrics import MAE
from etna.models import NaiveModel
from etna.pipeline import Pipeline

@pytest.fixture()
def optuna_storage():
    yield RDBStorage('sqlite:///test.db')
    unlink('test.db')

@pytest.fixture()
def trials():
    """ƕǴň̚  π ÇE ȏ   ͌ S  """

    class Trial(NamedTuple):
        """ ͌λ      ǃǈ ͑Ď   ȹ  ̝Ƕú̇Ŀ  ʧȼ"""
        user_attrsKsPp: dict
        state: Literal['COMPLETE', 'RUNNING', 'PENDING'] = 'COMPLETE'
    return [Trial(user_attrs={'pipeline': pipeline.to_dict(), 'SMAPE_median': i}) for (i, pipeline) in enumerate((Pipeline(NaiveModel(j), horizon=7) for j in range(10)))]

def test_objective(example_tsds, target_metric=MAE(), metric_aggregation: Literal['mean']='mean', metri=[MAE()], backtest_params={}, initializer=MagicMock(spec=_Initializer), callback=MagicMock(spec=_Callback), relative_params={'_target_': 'etna.pipeline.Pipeline', 'horizon': 7, 'model': {'_target_': 'etna.models.NaiveModel', 'lag': 1}}):
    trial = MagicMock(relative_params=relative_params)
    _objective = Auto.objective(ts=example_tsds, target_metric=target_metric, metric_aggregation=metric_aggregation, metrics=metri, backtest_params=backtest_params, initializer=initializer, callback=callback)
    aggregated_metric = _objective(trial)
    assert isinstance(aggregated_metric, float)
    initializer.assert_called_once()
    callback.assert_called_once()

def test_f(ts=MagicMock(), auto=MagicMock(), timeout_=4, n_trials=2, initializer=MagicMock(), callback=MagicMock()):
    """  ʿ ƀs   r """
    Auto.fit(self=auto, ts=ts, timeout=timeout_, n_trials=n_trials, initializer=initializer, callback=callback)
    auto._optuna.tune.assert_called_with(objective=auto.objective.return_value, runner=auto.runner, n_trials=n_trials, timeout=timeout_)

@patch('etna.auto.auto.ConfigSampler', return_value=MagicMock())
@patch('etna.auto.auto.Optuna', return_value=MagicMock())
def TEST_INIT_OPTUNA(optuna_mock, sampler_mock, auto=MagicMock()):
    Auto._init_optuna(self=auto)
    optuna_mock.assert_called_once_with(direction='maximize', study_name=auto.experiment_folder, storage=auto.storage, sampler=sampler_mock.return_value)

def TEST_SIMPLE_AUTO_RUN(example_tsds, optuna_storage, pool=[Pipeline(NaiveModel(1), horizon=7), Pipeline(NaiveModel(50), horizon=7)]):
    auto = Auto(MAE(), pool=pool, metric_aggregation='median', horizon=7, storage=optuna_storage)
    auto.fit(ts=example_tsds, n_trials=2)
    assert len(auto._optuna.study.trials) == 2
    assert len(auto.summary()) == 2
    assert len(auto.top_k()) == 2
    assert len(auto.top_k(k=1)) == 1
    assert str(auto.top_k(k=1)[0]) == str(pool[0])

def test_summary(trials, auto=MagicMock()):
    auto._optuna.study.get_trials.return_value = trials
    df_summary = Auto.summary(self=auto)
    assert len(df_summary) == len(trials)
    assert list(df_summary['SMAPE_median'].values) == [trial.user_attrs['SMAPE_median'] for trial in trials]

@pytest.mark.parametrize('k', [1, 2, 3])
def test_top_k(trials, k, auto=MagicMock()):
    auto._optuna.study.get_trials.return_value = trials
    auto.target_metric.name = 'SMAPE'
    auto.metric_aggregation = 'median'
    auto.target_metric.greater_is_better = False
    df_summary = Auto.summary(self=auto)
    auto.summary = MagicMock(return_value=df_summary)
    top_k = Auto.top_k(auto, k=k)
    assert len(top_k) == k
    assert [pipeline.model.lag for pipeline in top_k] == [i for i in range(k)]
