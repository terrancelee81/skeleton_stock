def test_imports():
    import forecaster
    from forecaster.data import interfaces, sources
    from forecaster.features import base, transforms, pipeline
    from forecaster.models import base as mbase, sklearn as msk
    from forecaster.evaluation import backtest, metrics
    from forecaster.services import pipeline as svc_pipeline

    assert True
