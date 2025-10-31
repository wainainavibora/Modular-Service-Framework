⚙️ Modular Service Framework

This repository implements a lightweight service management system in Python that supports:

🧩 Automatic service registration

🔄 Lifecycle management (start, stop, on_startup, on_shutdown)

🔗 Dependency injection

🧱 Typed configuration

🪶 Mixin extensibility

🧭 Context management support (with statements)

🧰 Dynamic service loading and orchestration

📦 Overview

This framework provides a simple yet powerful way to define and manage application services, similar in spirit to dependency injection containers and microservice orchestrators.

It allows developers to:

Define reusable services with lifecycle hooks.

Automatically register and manage them via a ServiceRegistry.

Pass configurations using type-enforced descriptors.

Start and stop all services in a controlled manner through the ServiceManager.

🧠 Core Concepts
1️⃣ Service Registration

All classes inheriting from BaseService are automatically registered through the ServiceRegistry metaclass.

class EmailService(BaseService):
    def on_startup(self):
        print("Connecting to SMTP...")

2️⃣ Lifecycle Hooks

Each service defines startup and shutdown behavior:

class TestService(BaseService):
    def on_startup(self):
        print("TestService starting...")
    def on_shutdown(self):
        print("TestService stopping...")

3️⃣ Configuration via Typed Descriptors

The Typed descriptor ensures configuration values are of expected types:

class ServerConfig:
    host = Typed("host", str)
    port = Typed("port", int)

🧩 Example Services

EmailService — Simulates connecting to and closing an SMTP connection.

NotificationService — Depends on EmailService, logs startup messages, and delegates email sending.

🧠 Example Usage
if __name__ == "__main__":
    config = ServerConfig("localhost", 8080)
    manager = ServiceManager(config)

    # Load and initialize all registered services
    manager.load_services(config)

    # Start all
    print("🚀 Starting all services...")
    manager.start_all()

    # Stop all
    print("🛑 Stopping all services...")
    manager.stop_all()

🖥️ Output Example
🚀 Starting all services...
Connecting to SMTP...
[LOG]: Notification service running at localhost:8080
EmailService started.
NotificationService started.
🛑 Stopping all services...
[LOG]: Notification stopping...
Closing SMTP...
EmailService stopped.
NotificationService stopped.

🧱 Class Overview
Class	Description
ServiceProtocol	Defines required methods (start, stop) for any service-like component.
ServiceRegistry	Metaclass that auto-registers concrete service classes.
BaseService	Provides base lifecycle methods and context manager support.
LoggerMixin	Adds simple logging functionality to services.
Typed	Enforces type safety in configuration attributes.
ServerConfig	Example configuration holder using Typed.
ServiceManager	Discovers, instantiates, and orchestrates all registered services.
🧩 Extending the Framework

To create a new service:

class MyCustomService(BaseService):
    def on_startup(self):
        print("Custom setup logic here.")
    def on_shutdown(self):
        print("Cleanup logic here.")


It will automatically appear in the registry and be loaded by the ServiceManager.

🧰 Requirements

Python ≥ 3.9

No external dependencies (uses only the standard library)

⚖️ License

MIT License © 2025