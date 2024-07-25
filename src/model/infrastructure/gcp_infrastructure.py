from model.infrastructure.virtual_machine import VirtualMachine

# Represent the GCP Infrastructure
class GcpInfrastructure:
    # Attrs
    vm_instances : list[VirtualMachine]= []
    containers = []
    
    
    def add_new_virtual_machine(self, vm: VirtualMachine):
        self.vm_instances.append(vm)

    def add_new_virtual_machines(self, vms: list ):
        self.vm_instances.extend(vms)
