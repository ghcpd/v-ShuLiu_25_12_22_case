from collections import Counter

_metrics = Counter()

def inc(metric, n=1):
    _metrics[metric] += n

def get(metric):
    return _metrics.get(metric, 0)

def snapshot():
    return dict(_metrics)
