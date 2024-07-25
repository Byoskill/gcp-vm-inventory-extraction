from model.infrastructure.gcp_infrastructure import GcpInfrastructure
from model.generator import Generator


class JSONGenerator(Generator):
    """Generates a JSON file from the GCP infrastructure data."""

    def export(self, gcp_infrastructure: GcpInfrastructure):
        # Implement JSON export logic here
        print("Exporting to JSON...")
