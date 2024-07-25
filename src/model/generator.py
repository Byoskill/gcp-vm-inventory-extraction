from abc import ABC, abstractmethod
from model.infrastructure.gcp_infrastructure import GcpInfrastructure


class Generator(ABC):
    """Abstract base class for all generators."""

    @abstractmethod
    def export(self, gcp_infrastructure: GcpInfrastructure):
        """Exports the GCP infrastructure data to a specific format."""
        pass
