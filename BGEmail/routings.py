from channels.routing import route
from . import consumers

routing = [
    route("email.send", consumers.sendEmail),
]