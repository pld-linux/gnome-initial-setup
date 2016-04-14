#
# Conditional build:
%bcond_with	krb5	# MIT Kerberos 5 instead of Heimdal
#
Summary:	GNOME Initial Setup utility
Summary(pl.UTF-8):	GNOME Initial Setup - narzędzie do wstępnej konfiguracji środowiska
Name:		gnome-initial-setup
Version:	3.20.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-initial-setup/3.20/%{name}-%{version}.tar.xz
# Source0-md5:	3730652bc69c0dc4479dbe049c469291
Patch0:		%{name}-heimdal.patch
URL:		https://wiki.gnome.org/Design/OS/InitialSetup
BuildRequires:	NetworkManager-devel >= 0.9.6.4
BuildRequires:	NetworkManager-gtk-lib-devel >= 0.9.6.4
BuildRequires:	accountsservice-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	cheese-devel >= 3.3.5
BuildRequires:	fontconfig-devel
BuildRequires:	gdm-devel >= 3.8.3
BuildRequires:	geoclue2-devel >= 2.1.2
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gnome-common
BuildRequires:	gnome-desktop-devel >= 3.8.0
BuildRequires:	gnome-online-accounts-devel >= 3.0
BuildRequires:	gtk+3-devel >= 3.12.0
BuildRequires:	gtk-webkit4-devel >= 2.6.0
%{!?with_krb5:BuildRequires:	heimdal-devel}
BuildRequires:	ibus-devel >= 1.4.99
BuildRequires:	intltool >= 0.40
BuildRequires:	iso-codes
BuildRequires:	json-glib-devel
%{?with_krb5:BuildRequires:	krb5-devel}
BuildRequires:	libgweather-devel >= 3.0
BuildRequires:	libpwquality-devel
BuildRequires:	libsecret-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pango-devel >= 1:1.32.5
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.103
BuildRequires:	rest-devel >= 0.7
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	NetworkManager >= 0.9.6.4
Requires:	NetworkManager-gtk-lib >= 0.9.6.4
Requires:	cheese >= 3.3.5
Requires:	gdm >= 3.8.3
Requires:	geoclue2 >= 2.1.2
Requires:	glib2 >= 1:2.36.0
Requires:	gnome-desktop >= 3.8.0
Requires:	gnome-online-accounts >= 3.0
Requires:	gtk+3 >= 3.12.0
Requires:	gtk-webkit4 >= 2.6.0
Requires:	ibus >= 1.4.99
Requires:	iso-codes
Requires:	libgweather >= 3.0
Requires:	pango >= 1:1.32.5
Requires:	polkit >= 0.103
Requires:	rest >= 0.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
After acquiring or installing a new system there are a few essential
things to set up before use. gnome-initial-setup aims to provide a
simple, easy, and safe way to prepare a new system.

%description -l pl.UTF-8
Po zainstalowaniu nowego systemu należy skonfigurować kilka
podstawowych elementów. gnome-initial-setup zapewnia prosty, łatwy i
bezpieczny sposób przygotowania nowego systemu.

%prep
%setup -q
%{!?with_krb5:%patch0 -p1}

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
/etc/xdg/autostart/gnome-initial-setup-copy-worker.desktop
/etc/xdg/autostart/gnome-initial-setup-first-login.desktop
/etc/xdg/autostart/gnome-welcome-tour.desktop
%attr(755,root,root) %{_libexecdir}/gnome-initial-setup
%attr(755,root,root) %{_libexecdir}/gnome-initial-setup-copy-worker
%attr(755,root,root) %{_libexecdir}/gnome-welcome-tour
%{_datadir}/gdm/greeter/applications/gnome-initial-setup.desktop
%{_datadir}/gdm/greeter/applications/setup-shell.desktop
%{_datadir}/gnome-session/sessions/gnome-initial-setup.session
%{_datadir}/gnome-shell/modes/initial-setup.json
%{_datadir}/polkit-1/rules.d/20-gnome-initial-setup.rules