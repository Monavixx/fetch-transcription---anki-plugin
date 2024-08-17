from aqt import mw


CONFIG_KEY_ORIGIN = 'origin'
DEFAULT_VALUE_ORIGIN = 'tophonetics'
VARIANTS_ORIGIN = ['tophonetics', 'cambridge', 'oxford']

def set_config_origin(value):
    if value in VARIANTS_ORIGIN:
        config = mw.addonManager.getConfig(__name__)
        config[CONFIG_KEY_ORIGIN] = value
        mw.addonManager.writeConfig(__name__, config)

def get_config_origin():
    return mw.addonManager.getConfig(__name__).get(CONFIG_KEY_ORIGIN, DEFAULT_VALUE_ORIGIN)

