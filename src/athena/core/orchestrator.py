"""
Orchestrator service for Athena.

This module implements the central coordinator that manages interactions between
all Athena components, including request routing, session management, and
operation scheduling.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ServiceInterface(ABC):
    """Base interface for all Athena services."""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the service."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the service gracefully."""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the service."""
        pass

class OrchestratorService(ServiceInterface):
    """Central coordinator for Athena components.
    
    The Orchestrator manages the interaction between all components, including
    request routing, session management, and operation scheduling.
    
    Attributes:
        config: Configuration dictionary
        services: Dictionary of registered services
        session_context: Current session context
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the orchestrator service.
        
        Args:
            config: Configuration dictionary containing service settings
            
        Raises:
            ValueError: If required configuration is missing
        """
        self.config = config
        self.services: Dict[str, ServiceInterface] = {}
        self.session_context: Dict[str, Any] = {}
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate the configuration dictionary.
        
        Raises:
            ValueError: If required configuration is missing
        """
        required_keys = ["log_level", "data_dir"]
        missing_keys = [key for key in required_keys if key not in self.config]
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {missing_keys}")
    
    def initialize(self) -> None:
        """Initialize the orchestrator and all registered services."""
        logger.info("Initializing Orchestrator service")
        self._setup_logging()
        self._initialize_services()
        logger.info("Orchestrator service initialized successfully")
    
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        log_level = getattr(logging, self.config["log_level"].upper())
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    def _initialize_services(self) -> None:
        """Initialize all registered services."""
        for service_name, service in self.services.items():
            try:
                logger.info(f"Initializing service: {service_name}")
                service.initialize()
            except Exception as e:
                logger.error(f"Failed to initialize service {service_name}: {e}")
                raise
    
    def shutdown(self) -> None:
        """Shutdown the orchestrator and all registered services gracefully."""
        logger.info("Shutting down Orchestrator service")
        for service_name, service in reversed(self.services.items()):
            try:
                logger.info(f"Shutting down service: {service_name}")
                service.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down service {service_name}: {e}")
        logger.info("Orchestrator service shut down complete")
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the orchestrator and all services.
        
        Returns:
            Dictionary containing status information for the orchestrator
            and all registered services
        """
        status = {
            "orchestrator": {
                "status": "running",
                "services": len(self.services),
                "session_active": bool(self.session_context)
            },
            "services": {
                name: service.get_status()
                for name, service in self.services.items()
            }
        }
        return status
    
    def register_service(self, name: str, service: ServiceInterface) -> None:
        """Register a new service with the orchestrator.
        
        Args:
            name: Unique identifier for the service
            service: Service instance implementing ServiceInterface
            
        Raises:
            ValueError: If service name is already registered
        """
        if name in self.services:
            raise ValueError(f"Service {name} is already registered")
        self.services[name] = service
        logger.info(f"Registered service: {name}")
    
    def get_service(self, name: str) -> Optional[ServiceInterface]:
        """Get a registered service by name.
        
        Args:
            name: Name of the service to retrieve
            
        Returns:
            Service instance if found, None otherwise
        """
        return self.services.get(name)
    
    def start_session(self, session_id: str, context: Dict[str, Any]) -> None:
        """Start a new session with the given context.
        
        Args:
            session_id: Unique identifier for the session
            context: Session context data
            
        Raises:
            ValueError: If session_id is already active
        """
        if session_id in self.session_context:
            raise ValueError(f"Session {session_id} is already active")
        self.session_context[session_id] = {
            "start_time": datetime.now(),
            "context": context
        }
        logger.info(f"Started session: {session_id}")
    
    def end_session(self, session_id: str) -> None:
        """End an active session.
        
        Args:
            session_id: ID of the session to end
            
        Raises:
            KeyError: If session_id is not found
        """
        if session_id not in self.session_context:
            raise KeyError(f"Session {session_id} not found")
        del self.session_context[session_id]
        logger.info(f"Ended session: {session_id}")
    
    def get_session_context(self, session_id: str) -> Dict[str, Any]:
        """Get the context for an active session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Session context dictionary
            
        Raises:
            KeyError: If session_id is not found
        """
        if session_id not in self.session_context:
            raise KeyError(f"Session {session_id} not found")
        return self.session_context[session_id]["context"] 