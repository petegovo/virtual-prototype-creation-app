"""
Test cases for the main FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "virtual-prototype-api"


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_fmi_list_endpoint():
    """Test the FMI list endpoint"""
    response = client.get("/api/fmi/list")
    assert response.status_code == 200
    data = response.json()
    assert "fmus" in data
    assert "total_count" in data
    assert isinstance(data["fmus"], list)
    assert isinstance(data["total_count"], int)


def test_ssp_list_endpoint():
    """Test the SSP list endpoint"""
    response = client.get("/api/ssp/list")
    assert response.status_code == 200
    data = response.json()
    assert "packages" in data
    assert "total_count" in data
    assert isinstance(data["packages"], list)
    assert isinstance(data["total_count"], int)


def test_projects_list_endpoint():
    """Test the projects list endpoint"""
    response = client.get("/api/projects/list")
    assert response.status_code == 200
    data = response.json()
    assert "projects" in data
    assert "total_count" in data
    assert isinstance(data["projects"], list)
    assert isinstance(data["total_count"], int)


def test_openapi_docs():
    """Test that OpenAPI documentation is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data


def test_docs_endpoint():
    """Test that Swagger UI is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_invalid_endpoint():
    """Test that invalid endpoints return 404"""
    response = client.get("/invalid/endpoint")
    assert response.status_code == 404