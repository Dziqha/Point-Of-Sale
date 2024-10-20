import eel
import core.controllers.user
import core.controllers.category
import core.controllers.product
import core.controllers.promo
import core.controllers.stock_movement
import core.controllers.voucher
import core.controllers.customer
import core.controllers.transaction
import core.controllers.transaction_item

from core.lib.db import get_db

get_db()

eel.init('ui')
eel.start(
    'templates/index.html',
    jinja_templates='templates'
)
