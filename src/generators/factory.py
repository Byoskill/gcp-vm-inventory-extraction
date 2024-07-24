from typing import Dict

from generators.csv_generator import CSVGenerator
from generators.json_generator import JSONGenerator
from generators.yaml_generator import YAMLGenerator
from model.infrastructure.gcp_infrastructure import GcpInfrastructure
from model.generator import Generator

GENERATORS: Dict[str, Generator] = {
    "csv": CSVGenerator(),
    "json": JSONGenerator(),
    "yaml": YAMLGenerator(),
}


def get_generator(generator_name: str) -> Generator:
    """Factory method to obtain a Generator from its name."""
    if generator_name in GENERATORS:
        return GENERATORS[generator_name]
    else:
        raise ValueError(f"Invalid generator name: {generator_name}")
