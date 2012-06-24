Summary:	IrDA Utilities
Summary(es):	Herramientas de IrDA
Summary(pl):	Narz�dzia do IrDA
Name:		irda-utils
Version:	0.9.16
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/irda/%{name}-%{version}.tar.gz
# Source0-md5:	2ff18f0571b5a331be7cd22fc3decd41
Patch0:		%{name}-gtk+2.patch
Patch1:		%{name}-includes.patch
URL:		http://irda.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	linux-libc-headers >= 2.4.0
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

%description -l es
IrDA es una manera excitante de comunicar con dispositivos remotos.
IrDA usa comunicaci�n inal�mbrica infrarroja as� que no hacen falta
ningunos cables. Las velocidades varian entre 9600 bps y 4 Mbps. Los
equipos que soportan IrDA son adaptadores de LAN, PDAs, impresoras,
port�tiles, tel�fonos m�viles etc.

Linux-IrDA es una implementaci�n GNU de las especificaciones de los
protocolos de IrDA. Linux-Irda soporta la mayor�a de los protocolos:
IrLAP, IrLMP, IrIAP, IrTTP, IrLPT, IrLAN, IrCOMM y IrOBEX.

El paquete IrDA Utils es una colecci�n de programas que permite el uso
de los protocolos de IrDA. Hay que configurar algunas cosas para hacer
IrDA funcionar en su m�quina, y algunas cualidaded de IrDA est�n
implementadas en el espacio del usuario.

La mayor�a de las cualidades es implementada en el n�cleo, as� que
tiene que habilitar el soporte de IrDA en el n�cleo antes de poder
utilizar cualquiera de las herramientas y los programas aqu�
mencionados.

%description -l pl
IrDA jest sposobem bezprzewodowej komunikacji z urz�dzeniami
zewn�trznymi przy u�yciu podczerwieni. Szybko�� od 9600bps do 4Mbps.
Rodzaje urz�dze� obs�uguj�cych IrDA: interfejsy LAN, PDA, drukarki,
laptopy, telefony przeno�ne itp.

Linux-IrDA jest implementacj� GNU protoko��w IrDA napisan� od
pocz�tku. Obs�uguje wi�kszo�� protoko��w: IrLAP, IrLMP, IrIAP, IrTTP,
IrLPT, IrLAN, IrCOMM, IrOBEX.

Pakiet irda-utils jest zestawem program�w pozwalaj�cych na u�ywanie
protoko��w IrDA. Cz�� narz�dzi jest wymaganych do uruchomienia IrDA,
cz�� mo�liwo�ci, jak np. IrOBEX, jest zaimplementowanych w
user-space.

Wi�kszo�� mo�liwo�ci jest zaimplementowanych w j�drze, wi�c musisz
mie� j�dro z obs�ug� IrDA zanim u�yjesz jakiegokolwiek narz�dzia z
tego pakietu.

%package devel
Summary:	IrDA header files
Summary(pl):	Pliki nag��wkowe IrDA
Group:		Development/Libraries

%description devel
IrDA header files to be used by IrDA applications.

%description devel -l pl
Pliki nag��wkowe IrDA, do budowania aplikacji korzystaj�cych z IrDA.

%prep
%setup -q
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
