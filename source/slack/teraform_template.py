#!/bin/python




e=ddb.engine()
results=e.query("SELECT FROM etmeta.table WHERE node='{0}'".format())

dc_name
datastore_cluster
cluster
network
vm_name
cpu_count
memory
guest_id
disk_array=[]
for disk in disks:
    disk_array.append("""disk {{
        label = "{0}"
        size  = {1}
    }}""".format(disk['name'],disk['size']))

vmware_template="""data "vsphere_datacenter" "dc" {{
  name = "{0}"
}}

data "vsphere_datastore_cluster" "datastore_cluster" {{
  name          = "{1}"
  datacenter_id = "${{data.vsphere_datacenter.dc.id}}"
}}

data "vsphere_compute_cluster" "cluster" {{
  name          = "{2}"
  datacenter_id = "${{data.vsphere_datacenter.dc.id}}"
}}

data "vsphere_network" "network" {{
  name          = "{3}"
  datacenter_id = "${{data.vsphere_datacenter.dc.id}}"
}}

resource "vsphere_virtual_machine" "vm" {{
  name                 = "{4}"
  resource_pool_id     = "${{data.vsphere_compute_cluster.cluster.resource_pool_id}}"
  datastore_cluster_id = "${{data.vsphere_datastore_cluster.datastore_cluster.id}}"

  num_cpus = {5}
  memory   ={6}
  guest_id = "{7}"

  network_interface {{
    network_id = "${{data.vsphere_network.network.id}}"
  }}

  {8}

}}""".format(dc_name,datastore_cluster,cluster,network,vm_name,cpu_count,memory,guest_id,"\n".join(disk_array))

