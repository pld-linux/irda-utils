Summary:	IrDA Utilities
Summary(pl):	Narzêdzia do IrDA
Name:		irda-utils
Version:	0.9.10
Release:	1
Source0:	http://www.cs.uit.no/~dagb/irda/irda-utils/%{name}-%{version}.tar.gz
Patch0:		%{name}-noirda.patch
Url:		http://www.cs.uit.no/~dagb/irda/irda-utils/
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IrDA is an exciting way of communicating with remote devices. IrDA
uses infrared wireless communication so no cables are required. Speeds
range from 9600bps to 4Mbps. The types of devices that support IrDA
are LAN adapters, PDA's, printers, laptops, mobile phones etc.

Linux-IrDA is a GNU implementation of the IrDA protocols
specifications written from scratch. Linux-IrDA supports most of the
IrDA protocols like IrLAP, IrLMP, IrIAP, IrTTP, IrLPT, IrLAN, IrCOMM
and IrOBEX.

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
%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT" -C irmanager

pushd irdalib ; {
	CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" ./autogen.sh --prefix=%{_prefix}
	%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"
} ; popd

pushd irdadump ; {
	CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" ./autogen.sh --prefix=%{_prefix}
	%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"
	cd gtk
	CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" ./configure --prefix=%{_prefix}
	%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"
} ; popd

pushd irdaping ; {
	%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"
} ; popd

pushd obex ; {
	CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" ./autogen.sh --prefix=%{_prefix}
	%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"
} ; popd

pushd obex_apps ; {
	%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"
} ; popd

pushd gnobex ; {
	CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" ./autogen.sh --prefix=%{_prefix}
	%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"
} ; popd

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_prefix}/X11R6/bin

%{__make} install -C irmanager \
	ROOT="$RPM_BUILD_ROOT" 	DESTDIR=$RPM_BUILD_ROOT
%{__make} install -C irdalib \
	ROOT="$RPM_BUILD_ROOT" 	DESTDIR=$RPM_BUILD_ROOT
%{__make} install -C irdaping \
	ROOT="$RPM_BUILD_ROOT" 	DESTDIR=$RPM_BUILD_ROOT
%{__make} install -C obex \
	ROOT="$RPM_BUILD_ROOT" 	DESTDIR=$RPM_BUILD_ROOT
%{__make} install -C obex_apps \
	ROOT="$RPM_BUILD_ROOT"	DESTDIR=$RPM_BUILD_ROOT

cp -f irdadump/nox/irdadump $RPM_BUILD_ROOT%{_bindir}
cp -f irdadump/gtk/irdadump $RPM_BUILD_ROOT%{_prefix}/X11R6/bin/irdadump-X11
cp -f gnobex/gnobex/gnobex $RPM_BUILD_ROOT%{_prefix}/X11R6/bin/gnobex

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%{_prefix}/X11R6/bin/*
%{_includedir}/irda
%{_includedir}/obex
%{_libdir}/*

%clean
rm -rf $RPM_BUILD_ROOT
