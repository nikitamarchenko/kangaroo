# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'kangaroo.manager.api.controllers.root.RootController',
    'modules': ['kangaroo.manager.api'],
#    'static_root': '%(confdir)s/public',
#    'template_path': '%(confdir)s/${package}/templates',
    'debug': True,
    'errors': {
        '404': '/error/404',
        '__force_dict__': True
    }
}

logging = {
    'loggers': {
        'root' : {'level': 'INFO', 'handlers': ['console']},
        'kangaroo': {'level': 'DEBUG', 'handlers': ['console']}
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        }
    }
}
