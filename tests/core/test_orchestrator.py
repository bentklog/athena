"""Tests for the Orchestrator service."""

from typing import Any

import pytest

from athena.core.orchestrator import OrchestratorService, ServiceInterface


class MockService(ServiceInterface):
    """Mock service for testing."""
    
    def __init__(self):
        self.initialized_called = False
        self.shutdown_called = False
    
    def initialize(self) -> None:
        self.initialized_called = True
    
    def shutdown(self) -> None:
        self.shutdown_called = True
    
    def get_status(self) -> dict[str, Any]:
        return {"status": "running" if self.initialized_called else "stopped"}

@pytest.fixture
def config():
    """Test configuration fixture."""
    return {
        "log_level": "INFO",
        "data_dir": "/tmp/athena"
    }

@pytest.fixture
def orchestrator(config):
    """Orchestrator service fixture."""
    return OrchestratorService(config)

def test_orchestrator_initialization(config):
    """Test orchestrator initialization with valid config."""
    orchestrator = OrchestratorService(config)
    assert orchestrator.config == config
    assert orchestrator.services == {}
    assert orchestrator.session_context == {}

def test_orchestrator_invalid_config():
    """Test orchestrator initialization with invalid config."""
    with pytest.raises(ValueError):
        OrchestratorService({})

def test_register_service(orchestrator):
    """Test service registration."""
    service = MockService()
    orchestrator.register_service("test_service", service)
    assert "test_service" in orchestrator.services
    assert orchestrator.services["test_service"] == service

def test_register_duplicate_service(orchestrator):
    """Test registering duplicate service."""
    service = MockService()
    orchestrator.register_service("test_service", service)
    with pytest.raises(ValueError):
        orchestrator.register_service("test_service", service)

def test_get_service(orchestrator):
    """Test getting registered service."""
    service = MockService()
    orchestrator.register_service("test_service", service)
    assert orchestrator.get_service("test_service") == service
    assert orchestrator.get_service("nonexistent") is None

def test_session_management(orchestrator):
    """Test session management functionality."""
    session_id = "test_session"
    context = {"user": "test_user"}
    
    # Test starting session
    orchestrator.start_session(session_id, context)
    assert session_id in orchestrator.session_context
    assert orchestrator.session_context[session_id]["context"] == context
    
    # Test getting session context
    assert orchestrator.get_session_context(session_id) == context
    
    # Test ending session
    orchestrator.end_session(session_id)
    assert session_id not in orchestrator.session_context

def test_session_errors(orchestrator):
    """Test session management error cases."""
    session_id = "test_session"
    context = {"user": "test_user"}
    
    # Test starting duplicate session
    orchestrator.start_session(session_id, context)
    with pytest.raises(ValueError):
        orchestrator.start_session(session_id, context)
    
    # Test getting nonexistent session
    with pytest.raises(KeyError):
        orchestrator.get_session_context("nonexistent")
    
    # Test ending nonexistent session
    with pytest.raises(KeyError):
        orchestrator.end_session("nonexistent")

def test_service_lifecycle(orchestrator):
    """Test service lifecycle management."""
    service = MockService()
    orchestrator.register_service("test_service", service)
    
    # Test initialization
    orchestrator.initialize()
    assert service.initialized_called
    
    # Test shutdown
    orchestrator.shutdown()
    assert service.shutdown_called

def test_get_status(orchestrator):
    """Test status reporting."""
    service = MockService()
    orchestrator.register_service("test_service", service)
    
    status = orchestrator.get_status()
    assert "orchestrator" in status
    assert "services" in status
    assert "test_service" in status["services"]
    assert status["orchestrator"]["services"] == 1 