from .base import env
ASGI_APPLICATION = 'thp.asgi.application'

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     },
# }

CHANNEL_REDIS = env.tuple('CHANNEL_REDIS', default=("127.0.0.1", 6379))
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [CHANNEL_REDIS],
        },
    },
}