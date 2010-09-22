# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~
"""
config = {}

# Configuration for the 'tipfy' module.
config['tipfy'] = {
    # Enable debugger. It will be loaded only in development.
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
        'tipfy.ext.appstats.AppstatsMiddleware',

    ],
    # Set the active apps.
    'apps_installed': [
        'moe.users',
        'moe.wiki',
        'meat',
    ],
    # Set base paths for apps.
    'apps_entry_points': {
        'meat':  '/meat',
        'moe.wiki':  '/wiki',
    },
}

# Configuration for the 'tipfy.ext.session' module.
config['tipfy.ext.session'] = {
    # Important: set a random secret key for sessions!
    'secret_key': 'meaty-goodness',
}

# Configuration for the 'moe' module.
config['moe'] = {
    'sitename':       'Meatography',
    'admin_email':    'scotthernandez@gmail.com',
    'analytics_code': 'UA-18585999-1',
    'use_subdomain':  False,
}
