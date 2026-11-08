# gc-cameras-akmod

Fedora akmod for the cameras of the **Chuwi Hi10 Max** (Intel IPU6):

| Sensor | ACPI HID | Module | Position |
|--------|----------|--------|----------|
| GalaxyCore GC8034 (8 MP) | `GCTI8034` | `gc8034` | rear |
| GalaxyCore GC5035 (5 MP) | `GCTI5035` | `gti5035` | front |

None of these are in mainline. The package builds three modules for every
installed kernel (via akmods):

- `gti5035`, `gc8034` — Rockchip-derived sensor drivers, ported to IPU6/ACPI
  and updated for kernel 7.2.
- `ipu_bridge` — the in-tree bridge with `GCTI5035`/`GCTI8034` added to
  `ipu_supported_sensors[]`, so IPU6 links the sensors into the media graph.

It also ships:

- `depmod.d` overrides so the patched `ipu_bridge` wins over the in-tree one;
- `modules-load.d` entry to autoload the sensors;
- a `dracut.conf.d` snippet that keeps `ipu_bridge`/`intel_ipu6*` **out of the
  initramfs**. Without it, dracut can embed the stock `ipu_bridge` (e.g. when
  it runs before akmods on a kernel update), it binds at boot, and libcamera
  reports `No sensor found`.

With libcamera's simple pipeline (software ISP) both cameras are exposed to
PipeWire.

## Build and install

```sh
sudo dnf install rpm-build akmods kmodtool gcc make "kernel-devel-$(uname -r)"
./build-rpm.sh          # as normal user
sudo ./install.sh       # installs RPMs, builds kmod for running kernel, reloads modules
```

## Troubleshooting

```sh
rpm -q kmod-gc-cameras-$(uname -r)        # kmod built for this kernel?
cat /sys/module/ipu_bridge/taint          # "OE" = patched bridge; empty = stock one
sudo lsinitrd | grep -i ipu               # only firmware, no ipu modules
dmesg | grep 'Connected .* cameras'
cam -l
```

Build logs for failed akmod builds: `/var/cache/akmods/gc-cameras/`.

## License

GPL-2.0-only (same as the upstream kernel and Rockchip drivers).
