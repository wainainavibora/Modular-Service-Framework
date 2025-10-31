from abc import ABC
from typing import Protocol


class ServiceProtocol(Protocol):
    def start(self) -> None: ...
    def stop(self) -> None: ...


class ServiceRegistry(type(ABC)):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        # Avoid registering abstract base
        if name not in ("BaseService",):
            ServiceRegistry.registry[name] = new_class
        return new_class


class BaseService(metaclass=ServiceRegistry):
    """Base service with lifecycle hooks."""

    def __init__(self, config=None):
        self.config = config

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.stop()

    def __call__(self):
        return self.start()

    def start(self):
        self.on_startup()
        print(f"{self.__class__.__name__} started.")

    def stop(self):
        self.on_shutdown()
        print(f"{self.__class__.__name__} stopped.")

    def on_startup(self):
        pass

    def on_shutdown(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}Service>"


class TestService(BaseService):
    def on_startup(self):
        print("TestService is starting up...")

    def on_shutdown(self):
        print("TestService is shutting down...")


class LoggerMixin:
    def log(self, message):
        print(f"[LOG]: {message}")


class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.expected_type} for {self.name}")
        instance.__dict__[self.name] = value


class ServerConfig:
    """Simple configuration holder using Typed descriptors."""
    host = Typed("host", str)
    port = Typed("port", int)

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __repr__(self):
        return f"ServerConfig(host={self.host!r}, port={self.port!r})"


class EmailService(BaseService):
    def on_startup(self):
        print("Connecting to SMTP...")

    def on_shutdown(self):
        print("Closing SMTP...")


class NotificationService(BaseService, LoggerMixin):
    def __init__(self, config, email_service: ServiceProtocol):
        super().__init__(config)
        self.email_service = email_service

    def on_startup(self):
        self.log(
            f"Notification service running at {self.config.host}:{self.config.port}"
        )
        self.email_service.start()

    def on_shutdown(self):
        self.log("Notification stopping...")
        self.email_service.stop()


class ServiceManager:
    def __init__(self):
        self.instances = []

    @property
    def registry(self):
        return ServiceRegistry.registry

    def load_services(self, config):
        for name, service_cls in self.registry.items():
            # Pass dependency only to NotificationService........key factor
            if name == "NotificationService":
                email_svc = self.get_service("EmailService", config)
                instance = service_cls(config, email_svc)
            else:
                instance = service_cls(config)

            self.instances.append(instance)

    def get_service(self, name, config):
        cls = self.registry.get(name)
        if cls:
            return cls(config)
        raise KeyError(f"Service '{name}' not found")

    def start_all(self):
        for service in self.instances:
            service.start()

    def stop_all(self):
        for service in self.instances:
            service.stop()
