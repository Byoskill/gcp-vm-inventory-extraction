from google.cloud import compute_v1

class Disk:
    def __init__(self, name: str, mode: str, type: str, disk_size_gb: int, licences: list[str] ):
        
        self.name = name
        self.mode = mode
        self.type = type
        self.disk_size_gb = disk_size_gb
        
        if licences is None:
            self.licences = []
        else:
            self.licences = licences
    def __str__(self):
        """Returns a string representation of the Disk object."""
        license_str = ", ".join([str(license) for license in self.licences])
        return f"Disk(name='{self.name}', mode='{self.mode}', type='{self.type}', disk_size_gb={self.disk_size_gb}, licences=[{license_str}])"  
    def add_license(self, licence: str):
        self.licences.append(licence)
        pass