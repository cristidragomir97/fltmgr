from importlib import import_module

robots = import_module('.robots', __name__)
fleet = import_module('.fleet', __name__)
portainer = import_module('.portainer', __name__)
introspect = import_module('.introspect', __name__)
apps = import_module('.apps', __name__)
hosts = import_module('.hosts', __name__)
deployments = import_module('.deployments', __name__)
auth = import_module('.auth', __name__)
notifications = import_module('.notifications', __name__)

__all__ = ['robots', 'fleet', 'portainer', 'introspect', 'apps', 'hosts', 'deployments', 'auth', 'notifications']
