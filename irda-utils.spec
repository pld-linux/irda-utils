Summary:	IrDA Utilities
Summary(pl):	Narzêdzia do IrDA
Name:		irda-utils
Version:	0.9.15
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://prdownloads.sourceforge.net/irda/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://irda.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	glib-devel
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:		/sbin/chkconfig

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

%description -l pl
IrDA jest sposobem bezprzewodowej komunikacji z urz±dzeniami
zewnêtrznymi przy u¿yciu podczerwieni. Szybko¶æ od 9600bps do 4Mbps.
Rodzaje urz±dzeñ obs³uguj±cych IrDA: interfejsy LAN, PDA, drukarki,
laptopy, telefony przeno¶ne itp.

Linux-IrDA jest implementacj± GNU protoko³ów IrDA napisan± od
pocz±tku. Obs³uguje wiêkszo¶æ protoko³ów: IrLAP, IrLMP, IrIAP, IrTTP,
IrLPT, IrLAN, IrCOMM, IrOBEX.

Pakiet irda-utils jest zestawem programów pozwalaj±cych na u¿ywanie
protoko³ów IrDA. Czê¶æ narzêdzi jest wymaganych do uruchomienia IrDA,
czê¶æ mo¿liwo¶ci, jak np. IrOBEX, jest zaimplementowanych w
user-space.

Wiêkszo¶æ mo¿liwo¶ci jest zaimplementowanych w j±drze, wiêc musisz
mieæ j±dro z obs³ug± IrDA zanim u¿yjesz jakiegokolwiek narzêdzia z
tego pakietu.

%package devel
Summary:	IrDA header files
Summary(pl):	Pliki nag³ówkowe IrDA
Group:		Development/Libraries

%description devel
IrDA header files to be used by IrDA applications.

%description devel -l pl
Pliki nag³ówkowe IrDA, do budowania aplikacji korzystaj±cych z IrDA.

%prep
%setup -q

%build
cd findchip
%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"
# %{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT" gfindchip

cd ../irattach
%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"

cd ../irdadump
%{__libtoolize}
aclocal
%{__autoconf}
%{__automake}
%configure
%{__make}

cd ../irdaping
%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"

# cd ../irsockets
# %{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"

cd ../psion
%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"

cd ../tekram
%{__make} RPM_OPT_FLAGS="%{rpmcflags}" ROOT="$RPM_BUILD_ROOT"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_includedir}} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

install findchip/findchip $RPM_BUILD_ROOT%{_sbindir}
# install findchip/gfindchip $RPM_BUILD_ROOT%{_prefix}/X11R6/bin
install irattach/irattach $RPM_BUILD_ROOT%{_sbindir}
install irattach/dongle_attach $RPM_BUILD_ROOT%{_sbindir}
install irattach/README README.irattach
install irdadump/shell/irdadump $RPM_BUILD_ROOT%{_sbindir}/irdadump
install irdadump/README README.irdadump
install irdaping/irdaping $RPM_BUILD_ROOT%{_sbindir}/irdaping
install psion/irpsion5 $RPM_BUILD_ROOT%{_bindir}
install tekram/irkbd $RPM_BUILD_ROOT%{_sbindir}
install tekram/README README.tekram
install include/irda.h $RPM_BUILD_ROOT%{_includedir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/irda
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/irda

gzip -9nf README* etc/modules.conf.irda

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add irda

if [ -f /var/lock/subsys/irda ]; then
	/etc/rc.d/init.d/irda restart >&2
fi

%preun
if [ "$1" = 0 ]; then
	if [ -f /var/lock/subsys/irda ]; then
		/etc/rc.d/init.d/irda stop >&2
	fi
	/sbin/chkconfig --del irda
fi

%files
%defattr(644,root,root,755)
%doc *.gz etc/*.gz
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/irda
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/irda

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
