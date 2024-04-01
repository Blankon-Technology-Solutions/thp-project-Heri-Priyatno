# import os
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     # Create a log handler that prints logs to the terminal
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     # Define the root logger's settings
#     'root': {
#         'handlers': ['console'],
#         'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
#     },
#     # Define the django log module's settings
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
#             'propagate': False,
#         },
#     },
# }
