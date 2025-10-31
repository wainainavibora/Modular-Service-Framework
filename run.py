from app import ServiceManager, ServerConfig, TestService, EmailService, NotificationService  

config = ServerConfig("localhost", 8000)
manager = ServiceManager()

print("Registered Services:", manager.registry)  

manager.load_services(config)

print("\nStarting all services:")
manager.start_all()

print("\nStopping all services:")
manager.stop_all()
