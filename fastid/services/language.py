from ..trace import decorator_trace
from . import models

LANGUAGE = [
    {'value': 'en-us', 'name': 'English (United States)'},
    {'value': 'en-gb', 'name': 'English (United Kingdom)'},
    {
        'value': 'en-au',
        'name': 'English (Australia)',
    },
    {'value': 'en-ie', 'name': 'English (Ireland)'},
    {'value': 'en-il', 'name': 'English (Israel)'},
    {'value': 'en-in', 'name': 'English (India)'},
    {'value': 'en-nz', 'name': 'English (New Zealand)'},
    {'value': 'en-sg', 'name': 'English (Singapore)'},
    {'value': 'ru', 'name': 'Русский (Russian)'},
]


@decorator_trace(name='services.language.get_all')
async def get_all() -> list[models.Language]:
    return [models.Language(name=item['name'], value=item['value']) for item in LANGUAGE]
