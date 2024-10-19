import eel
import core.controllers.user
import core.controllers.category
import core.controllers.product

from core.lib.db import get_db

get_db()

eel.init('ui')
eel.start(
    'templates/index.html',
    jinja_templates='templates'
)
