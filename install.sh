#!/usr/bin/env bash
# Instala akmod-gc-cameras y reemplaza los .ko instalados a mano.
# Uso: sudo ./install.sh   (antes: ./build-rpm.sh como usuario normal)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KREL="$(uname -r)"
[ "$(id -u)" -eq 0 ] || { echo "Ejecutar con sudo" >&2; exit 1; }

echo "==> Instalando RPMs"
dnf install -y "$ROOT"/rpmbuild/RPMS/x86_64/akmod-gc-cameras-*.rpm \
               "$ROOT"/rpmbuild/RPMS/noarch/gc-cameras-*.rpm

echo "==> Compilando con akmods para $KREL"
akmods --force --kernels "$KREL" --akmod gc-cameras
rpm -q "kmod-gc-cameras-$KREL" >/dev/null || { echo "akmods no generó kmod-gc-cameras-$KREL; ver /var/cache/akmods/gc-cameras/" >&2; exit 1; }

echo "==> Quitando módulos instalados a mano (todos los kernels)"
for k in /lib/modules/*; do
	rm -fv "$k/extra/gti5035.ko" "$k/extra/gc8034.ko" "$k/updates/ipu-bridge.ko" \
	       "$k/updates/drivers/media/i2c/gc5035.ko"
done
rm -fv /etc/modules-load.d/gc-cameras.conf   # ahora lo provee el paquete en /usr/lib/modules-load.d
depmod -a "$KREL"

echo "==> Recargando cámaras"
modprobe -r gc8034 gti5035 intel_ipu6_isys intel_ipu6 ipu_bridge 2>/dev/null || true
modprobe gti5035; modprobe gc8034; modprobe intel_ipu6_isys
sleep 2
modinfo -F filename ipu_bridge gti5035 gc8034
dmesg | grep -E 'Connected [0-9]+ cameras' | tail -1
