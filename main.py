import eel
import core.controllers.user

eel.init('ui')
eel.start(
    'templates/index.html',
    jinja_templates='templates'
)
