import libvirt

# Connect to the local libvirt instance
conn = libvirt.open()

# Get a list of all running virtual machines
vms = conn.listDomainsID()

# Iterate through the list of running virtual machines
for vm_id in vms:
    vm = conn.lookupByID(vm_id)
    print("Name: ", vm.name())

    # Get the current CPU usage of the virtual machine
    cpu_stats = vm.getCPUStats(True)
    print("CPU usage: ", cpu_stats["cpu_time"])

    # Get the current memory usage of the virtual machine
    memory_stats = vm.memoryStats()
    print("Memory usage: ", memory_stats["rss"])

# Close the connection
conn.close()
