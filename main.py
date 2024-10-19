import eel
import core.controllers.user
import core.controllers.category

eel.init('ui')
eel.start(
    'templates/index.html',
    jinja_templates='templates'
)
