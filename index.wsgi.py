import sae

from app.data_show import app

application = sae.create_wsgi_app(app)