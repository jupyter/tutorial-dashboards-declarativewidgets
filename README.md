
# Create a virtual device on IBM SoftLayer

Provision a new virtual device.

```
bin/create-vm.sh --hostname pydata0
```

Once it's running, add a DNS entry for the public IP.

```
bin/add-dns.sh --hostname pydata0
```
