""""""

from imagen.server.app import app
from imagen.server.routes import image, search

app.include_router(image.router)
app.include_router(search.router)
