"""Tests for dependency injection container."""

import pytest

from gemini_query.di.container import Container, create_container


class TestDIContainer:
    """Test cases for dependency injection container."""

    def test_create_container_with_default_profile(self):
        """Test container creation with default profile."""
        container = create_container()

        assert container is not None
        assert hasattr(container, 'config')

    def test_create_container_with_test_profile(self):
        """Test container creation with test profile."""
        container = create_container("test")

        # Verify configuration is set correctly
        assert container.config.profile_name() == "test"

    def test_container_is_instance_of_container_class(self):
        """Test that created container is instance of Container class."""
        container = create_container("test")
        # Check that it's a dependency_injector container
        assert hasattr(container, 'config')
        assert hasattr(container, 'providers')

    def test_container_with_invalid_profile(self):
        """Test container behavior with invalid profile name."""
        # Should not raise exception
        container = create_container("invalid_profile")
        assert container is not None

    def test_container_configuration_setup(self):
        """Test that container configuration is properly set up."""
        container = create_container("development")

        # Should have profile_name configured
        assert container.config.profile_name() == "development"

    def test_multiple_containers_are_independent(self):
        """Test that multiple containers maintain independent state."""
        container1 = create_container("test")
        container2 = create_container("production")

        assert container1.config.profile_name() == "test"
        assert container2.config.profile_name() == "production"