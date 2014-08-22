Summary:	C library for portable packet creation and injection
Name:		libnet
Version:	1.1.6
Release:	1%{?dist}
License:	BSD
Group:		System/Libraries
URL:		http://www.sourceforge.net/projects/libnet-dev/
Source:		%{name}-%{version}.tar.xz
BuildRequires:	autoconf, automake, libtool

%description
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network packet
writing and handling (use libnet in conjunction with libpcap and you can
write some really cool stuff). Libnet includes packet creation at the IP
layer and at the link layer as well as a host of supplementary and
complementary functionality.

%package devel
Summary:	Development files for the libnet library
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The libnet-devel package includes header files and libraries necessary
for developing programs which use the libnet library. Libnet is very handy
with which to write network tools and network test code. See the manpage
and sample test code for more detailed information.

%prep
%setup -q -n %{name}-%{version}/upstream/libnet

# Man pages cannot be built
sed -i 's/SUBDIRS\s*=\s*man html/SUBDIRS = html/' doc/Makefile.am

sh ./autogen.sh

# Keep the sample directory untouched by make
rm -rf __dist_sample
mkdir __dist_sample
cp -a sample __dist_sample

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.{a,la}

# Prepare samples directory and perform some fixes
rm -rf __dist_sample/sample/win32
rm -f __dist_sample/sample/Makefile.{am,in}
sed -e 's@#include "../include/libnet.h"@#include <libnet.h>@' \
  __dist_sample/sample/libnet_test.h > __dist_sample/sample/libnet_test.h.new
touch -c -r __dist_sample/sample/libnet_test.h{,.new}
mv -f __dist_sample/sample/libnet_test.h{.new,}

# Remove makefile relics from documentation
rm -f doc/html/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README doc/CHANGELOG doc/CONTRIB doc/COPYING
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/CHANGELOG doc/CONTRIB doc/COPYING doc/DESIGN_NOTES doc/MIGRATION doc/PACKET_BUILDING
%doc doc/RAWSOCKET_NON_SEQUITUR doc/TODO doc/html/ __dist_sample/sample/
%{_bindir}/%{name}-config
%{_libdir}/%{name}.so
%{_includedir}/libnet.h
%{_includedir}/%{name}/
#%{_mandir}/man3/%{name}*.3*
