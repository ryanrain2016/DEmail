from channels.routing import route
from . import consumers

routing = [
    route("email.send", consumers.sendEmail),
    consumers.WebConsumer.as_route(path=r'^/email/'),
]