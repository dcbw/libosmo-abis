Name:           libosmo-abis
Version:        2.0.1
Release:        1.dcbw%{?dist}
Summary:        A-bis interface between BTS and BSC
License:        AGPLv3

URL:            https://osmocom.org/projects/libosmo-abis/wiki/Libosmo-abis

BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  doxygen
BuildRequires:  ortp-devel
BuildRequires:  openssl-devel
BuildRequires:  libtalloc-devel
BuildRequires:  libosmocore-devel >= 1.11.0
BuildRequires:  libosmo-netif-devel >= 1.6.0
BuildRequires:  osmo-e1d-devel >= 0.7

Source0: %{name}-%{version}.tar.bz2


%description
A-bis interface between BTS and BSC. It implements
drivers for mISDN and DAHDI based E1 cards, as well
as some A-bis/IP dialects.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.


%prep
echo "%{version}" >.tarball-version
%autosetup -p1
# new ortp
sed -i '/ortp_set_memory_functions/d' src/trau/osmo_ortp.c
sed -i '/OrtpMemoryFunctions/,/\}\;/d' src/trau/osmo_ortp.c


%build
%global optflags %(echo %optflags | sed 's|-Wp,-D_GLIBCXX_ASSERTIONS||g')
autoreconf -fi
%configure --enable-shared \
           --disable-static \
           --disable-dahdi \
           --enable-e1d

# Fix unused direct shlib dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# Remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} \;
sed -i -e 's|UNKNOWN|%{version}|g' %{buildroot}/%{_libdir}/pkgconfig/*.pc


%check
make check


%ldconfig_scriptlets


%files
%doc README.md
%license COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/osmocom/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Jun  8 2025 Dan Williams <dan@ioncontrol.co> - 2.0.1
- Update to 2.0.1

* Sun Aug 26 2018 Cristian Balint <cristian.balint@gmail.com>
- github update releases
