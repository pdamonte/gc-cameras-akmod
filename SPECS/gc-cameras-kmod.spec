# akmod package for the GalaxyCore GC5035/GC8034 camera sensors on Intel IPU6
# (Chuwi Hi10 Max). Builds gti5035, gc8034 and a patched ipu_bridge.
%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:           gc-cameras-kmod
Version:        0.2
Release:        3%{?dist}
Summary:        Kernel modules for GalaxyCore GC5035/GC8034 cameras on Intel IPU6
License:        GPL-2.0-only
URL:            https://github.com/pdamonte/gc-cameras-akmod
Source0:        gc-cameras-%{version}.tar.gz

BuildRequires:  kmodtool
%{!?kernels:BuildRequires: gcc, make, elfutils-libelf-devel}

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Out-of-tree kernel modules for the GalaxyCore GC5035 (front, ACPI GCTI5035)
and GC8034 (rear, ACPI GCTI8034) camera sensors, plus a patched ipu_bridge
that registers those sensors with the Intel IPU6 ISYS.

%prep
%{?kmodtool_check}
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
%setup -q -c
for kernel_version in %{?kernel_versions}; do
    cp -a gc-cameras-%{version} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    %{make_build} -C "${kernel_version##*___}" M="${PWD}/_kmod_build_${kernel_version%%___*}" modules
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    install -m 0755 _kmod_build_${kernel_version%%___*}/*.ko \
        %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Sun Nov 08 2026 pdamonte <pdamonte@users.noreply.github.com> - 0.2-3
- Rebuild alongside gc-cameras 0.2-3.

* Mon Nov 02 2026 pdamonte <pdamonte@users.noreply.github.com> - 0.2-2
- Fix camera facing for Chuwi Hi10 Max: GC8034 is back, GC5035 is front;
  gc8034 now exposes camera_orientation/rotation controls.

* Mon Nov 02 2026 pdamonte <pdamonte@users.noreply.github.com> - 0.2-1
- Proper kmodtool-based akmod with gti5035, gc8034 and ipu_bridge.
- gti5035: drop linux/of_gpio.h and manual gpio_free() (removed in 7.2;
  GPIOs are devm-managed).
