from .test import TestConfig
from .production import ProdConfig

try:
    from .development import DevConfig
except Exception as e:
    DevConfig = None

__all__ = ['DevConfig', 'TestConfig', 'ProdConfig']
