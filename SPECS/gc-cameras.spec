Name:           gc-cameras
Version:        0.2
Release:        3%{?dist}
Summary:        Common files for the gc-cameras kernel modules
License:        GPL-2.0-only
URL:            https://github.com/pdamonte/gc-cameras-akmod
BuildArch:      noarch
Source0:        gc-cameras-modules-load.conf
Source1:        gc-cameras-depmod.conf
Source2:        gc-cameras-dracut.conf

Provides:       %{name}-kmod-common = %{version}
Requires:       %{name}-kmod >= %{version}

%description
Module autoload and depmod override configuration for the GalaxyCore
GC5035/GC8034 camera modules (gti5035, gc8034, patched ipu_bridge).

%prep

%build

%install
install -D -m 0644 %{SOURCE0} %{buildroot}%{_modulesloaddir}/gc-cameras.conf
install -D -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/depmod.d/gc-cameras.conf
install -D -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/90-gc-cameras.conf

%files
%{_modulesloaddir}/gc-cameras.conf
%{_prefix}/lib/depmod.d/gc-cameras.conf
%{_prefix}/lib/dracut/dracut.conf.d/90-gc-cameras.conf

%posttrans
# Rebuild the running kernel's initramfs without the in-tree IPU6 modules.
dracut -f --kver "$(uname -r)" >/dev/null 2>&1 || :

%changelog
* Sun Nov 08 2026 pdamonte <pdamonte@users.noreply.github.com> - 0.2-3
- Ship a dracut config that omits ipu_bridge/intel_ipu6* from the initramfs,
  so the stock ipu_bridge cannot bind before the patched one; rebuild the
  running kernel's initramfs on install.

* Mon Nov 02 2026 pdamonte <pdamonte@users.noreply.github.com> - 0.2-2
- Rebuild alongside gc-cameras-kmod 0.2-2.

* Mon Nov 02 2026 pdamonte <pdamonte@users.noreply.github.com> - 0.2-1
- Initial common package.
