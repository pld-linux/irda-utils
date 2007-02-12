Summary:	IrDA Utilities
Summary(es.UTF-8):   Herramientas de IrDA
Summary(pl.UTF-8):   Narzędzia do IrDA
Name:		irda-utils
Version:	0.9.17
%define		_pre	pre3
Release:	0.%{_pre}
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/irda/%{name}-%{version}-%{_pre}.tar.gz
# Source0-md5:	3f3076c3ce86ec94bd15488d907a1bc3
Patch0:		%{name}-includes.patch
Patch1:		%{name}-gcc4.patch
URL:		http://irda.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	linux-libc-headers >= 2.4.0
BuildRequires:	pkgconfig
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

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

%description -l es.UTF-8
IrDA es una manera excitante de comunicar con dispositivos remotos.
IrDA usa comunicación inalámbrica infrarroja así que no hacen falta
ningunos cables. Las velocidades varian entre 9600 bps y 4 Mbps. Los
equipos que soportan IrDA son adaptadores de LAN, PDAs, impresoras,
portátiles, teléfonos móviles etc.

Linux-IrDA es una implementación GNU de las especificaciones de los
protocolos de IrDA. Linux-Irda soporta la mayoría de los protocolos:
IrLAP, IrLMP, IrIAP, IrTTP, IrLPT, IrLAN, IrCOMM y IrOBEX.

El paquete IrDA Utils es una colección de programas que permite el uso
de los protocolos de IrDA. Hay que configurar algunas cosas para hacer
IrDA funcionar en su máquina, y algunas cualidaded de IrDA están
implementadas en el espacio del usuario.

La mayoría de las cualidades es implementada en el núcleo, así que
tiene que habilitar el soporte de IrDA en el núcleo antes de poder
utilizar cualquiera de las herramientas y los programas aquí
mencionados.

%description -l pl.UTF-8
IrDA jest sposobem bezprzewodowej komunikacji z urządzeniami
zewnętrznymi przy użyciu podczerwieni. Szybkość od 9600bps do 4Mbps.
Rodzaje urządzeń obsługujących IrDA: interfejsy LAN, PDA, drukarki,
laptopy, telefony przenośne itp.

Linux-IrDA jest implementacją GNU protokołów IrDA napisaną od
początku. Obsługuje większość protokołów: IrLAP, IrLMP, IrIAP, IrTTP,
IrLPT, IrLAN, IrCOMM, IrOBEX.

Pakiet irda-utils jest zestawem programów pozwalających na używanie
protokołów IrDA. Część narzędzi jest wymaganych do uruchomienia IrDA,
część możliwości, jak np. IrOBEX, jest zaimplementowanych w
user-space.

Większość możliwości jest zaimplementowanych w jądrze, więc musisz
mieć jądro z obsługą IrDA zanim użyjesz jakiegokolwiek narzędzia z
tego pakietu.

%package devel
Summary:	IrDA header files
Summary(pl.UTF-8):   Pliki nagłówkowe IrDA
Group:		Development/Libraries

%description devel
IrDA header files to be used by IrDA applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe IrDA, do budowania aplikacji korzystających z IrDA.

%prep
%setup -q -n %{name}-%{version}-%{_pre}
%patch0 -p1
%patch1 -p1

%build
%ifarch %{ix86}
%{__make} -C findchip \
	RPM_OPT_FLAGS="%{rpmcflags}"
%endif

%{__make} -C irattach \
	RPM_OPT_FLAGS="%{rpmcflags}"

cd irdadump
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}
cd ..

%{__make} -C irdaping \
	RPM_OPT_FLAGS="%{rpmcflags}"

%{__make} -C irsockets \
	RPM_OPT_FLAGS="%{rpmcflags}" \
	SYS_INCLUDES=

%{__make} -C psion \
	RPM_OPT_FLAGS="%{rpmcflags}"

%{__make} -C tekram \
	RPM_OPT_FLAGS="%{rpmcflags}" \
	SYS_INCLUDES="-I../include"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_includedir}}

%ifarch %{ix86}
install findchip/findchip $RPM_BUILD_ROOT%{_sbindir}
%endif
install irattach/{irattach,dongle_attach} $RPM_BUILD_ROOT%{_sbindir}
install irattach/README README.irattach
install irdadump/shell/irdadump $RPM_BUILD_ROOT%{_sbindir}
install irdadump/README README.irdadump
install irdaping/irdaping $RPM_BUILD_ROOT%{_sbindir}
install irsockets/{ias_query,irdaspray,irprintf,irprintfx,irscanf,irscanfx,recv_ultra,send_ultra} $RPM_BUILD_ROOT%{_sbindir}
install irsockets/README README.irsockets
install psion/irpsion5 $RPM_BUILD_ROOT%{_bindir}
install tekram/irkbd $RPM_BUILD_ROOT%{_sbindir}
install tekram/README README.tekram
install include/irda.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* etc/modules.conf.irda
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
