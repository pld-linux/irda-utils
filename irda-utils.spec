Summary: IrDA Utilities
Name: irda-utils
Version: 0.9.4
Release: 1
Source: http://www.cs.uit.no/~dagb/irda/irda-utils/irda-utils-0.9.4.tar.gz
Patch0: irda-utils-0.9.4-noirda.patch
Url: http://www.cs.uit.no/~dagb/irda/irda-utils/
Copyright: GPL
Group: Applications/System
BuildRoot: /var/tmp/%{name}-root

%description
IrDA is an exciting way of communicating with remote devices. IrDA
uses infrared wireless communication so no cables are required. Speeds
range from 9600bps to 4Mbps. The types of devices that support IrDA
are LAN adapters, PDA's, printers, laptops, mobile phones etc.

Linux-IrDA is a GNU implementation of the IrDA protocols specifications
written from scratch. Linux-IrDA supports most of the IrDA protocols
like IrLAP, IrLMP, IrIAP, IrTTP, IrLPT, IrLAN, IrCOMM and IrOBEX.

The IrDA Utils package is a collection of programs, that enables the
use of the IrDA protocols. Some user-space configuration is required
in order to make IrDA work for your machine, and some IrDA features
like IrOBEX is actually implemented in user-space.

Most of the features are implemented in the kernel, so you must enable
IrDA support in the kernel before you can use any of the tools and
programs mentioned in this document.

%prep
%setup -q
%patch0 -p1 -b .noirda

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ROOT="$RPM_BUILD_ROOT" -C irmanager

pushd irdalib ; {
  CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=/usr
  make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ROOT="$RPM_BUILD_ROOT"
} ; popd

pushd irdadump ; {
  CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=/usr
  make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ROOT="$RPM_BUILD_ROOT"
  cd gtk
  CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr
  make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ROOT="$RPM_BUILD_ROOT"
} ; popd

pushd irdaping ; {
  make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ROOT="$RPM_BUILD_ROOT"
} ; popd


pushd obex ; {
  CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=/usr
  make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ROOT="$RPM_BUILD_ROOT"
} ; popd

pushd obex_apps ; {
  make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ROOT="$RPM_BUILD_ROOT"
} ; popd

pushd gnobex ; {
  CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=/usr
  make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ROOT="$RPM_BUILD_ROOT"
} ; popd


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/bin $RPM_BUILD_ROOT/usr/X11R6/bin

make install -C irmanager \
	ROOT="$RPM_BUILD_ROOT" 	DESTDIR=$RPM_BUILD_ROOT
make install -C irdalib \
	ROOT="$RPM_BUILD_ROOT" 	DESTDIR=$RPM_BUILD_ROOT
make install -C irdaping \
	ROOT="$RPM_BUILD_ROOT" 	DESTDIR=$RPM_BUILD_ROOT
make install -C obex \
	ROOT="$RPM_BUILD_ROOT" 	DESTDIR=$RPM_BUILD_ROOT
make install -C obex_apps \
	ROOT="$RPM_BUILD_ROOT"	DESTDIR=$RPM_BUILD_ROOT

cp irdadump/nox/irdadump $RPM_BUILD_ROOT/usr/bin
cp irdadump/gtk/irdadump $RPM_BUILD_ROOT/usr/X11R6/bin/irdadump-X11
cp gnobex/gnobex/gnobex $RPM_BUILD_ROOT/usr/X11R6/bin/gnobex

%files
%defattr(-,root,root)
/usr/sbin/*
/usr/bin/*
/usr/X11R6/bin/*
/usr/include/irda
/usr/include/obex
/usr/lib/*

%changelog
* Fri Sep 17 1999 Cristian Gafton <gafton@redhat.com>
- build for RH 6.1
- add pacth to make the damn package compile without any IrDA installed.
