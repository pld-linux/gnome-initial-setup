# TODO: gnome-initial-setup user (see data/gnome-initial-setup.conf)?
#
# Conditional build:
%bcond_with	krb5		# MIT Kerberos 5 instead of Heimdal
%bcond_without	malcontent	# parental control via malcontent
#
Summary:	GNOME Initial Setup utility
Summary(pl.UTF-8):	GNOME Initial Setup - narzędzie do wstępnej konfiguracji środowiska
Name:		gnome-initial-setup
Version:	45.3
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-initial-setup/45/%{name}-%{version}.tar.xz
# Source0-md5:	2b6cc0fa6de4e54d43a5038ad62902f8
Patch0:		%{name}-heimdal.patch
URL:		https://wiki.gnome.org/Design/OS/InitialSetup
BuildRequires:	NetworkManager-devel >= 2:1.2
BuildRequires:	accountsservice-devel
BuildRequires:	fontconfig-devel
BuildRequires:	gdm-devel >= 3.8.3
BuildRequires:	geoclue2-devel >= 2.3.1
BuildRequires:	geocode-glib2-devel >= 3.26
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.63.1
BuildRequires:	gnome-desktop4-devel >= 42
BuildRequires:	gnome-online-accounts-devel >= 3.0
BuildRequires:	gsettings-desktop-schemas-devel >= 3.37.1
BuildRequires:	gtk4-devel >= 4.6
BuildRequires:	gtk-webkit6-devel >= 2.40.0
%{!?with_krb5:BuildRequires:	heimdal-devel}
BuildRequires:	ibus-devel >= 1.4.99
BuildRequires:	iso-codes
BuildRequires:	json-glib-devel
%{?with_krb5:BuildRequires:	krb5-devel}
BuildRequires:	libadwaita-devel >= 1.2
BuildRequires:	libgweather4-devel >= 4.0
%if %{with malcontent}
BuildRequires:	libmalcontent-devel >= 0.6.0
BuildRequires:	libmalcontent-ui-devel >= 0.11.0
%endif
BuildRequires:	libnma-gtk4-devel >= 1.0
BuildRequires:	libpwquality-devel
BuildRequires:	libsecret-devel >= 0.18.8
BuildRequires:	meson >= 0.53.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pango-devel >= 1:1.32.5
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.103
BuildRequires:	rest1-devel >= 0.9
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	systemd-units >= 1:242
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	NetworkManager >= 2:1.2
Requires:	NetworkManager-gtk-lib >= 1.0
Requires:	gdm >= 3.8.3
Requires:	geoclue2 >= 2.3.1
Requires:	glib2 >= 1:2.63.1
Requires:	gnome-desktop4 >= 42
Requires:	gnome-online-accounts >= 3.0
Requires:	gnome-session >= 1:44
%ifarch %{ix86} %{x8664} aarch64
# where available
Requires:	gnome-tour >= 3.38
%endif
Requires:	gsettings-desktop-schemas >= 3.37.1
Requires:	gtk4 >= 4.6
Requires:	gtk-webkit6 >= 2.40.0
Requires:	ibus >= 1.4.99
Requires:	iso-codes
Requires:	libadwaita >= 1.2
Requires:	libgweather4 >= 4.0
Requires:	libsecret >= 0.18.8
%if %{with malcontent}
Requires:	libmalcontent-ui >= 0.11.0
Requires:	malcontent >= 0.6.0
%endif
Requires:	pango >= 1:1.32.5
Requires:	polkit >= 0.103
Requires:	rest1 >= 0.9
Requires:	systemd-units >= 1:242
Requires:	tecla
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
%meson build \
	%{!?with_malcontent:-Dparental_controls=disabled}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md
/etc/xdg/autostart/gnome-initial-setup-copy-worker.desktop
/etc/xdg/autostart/gnome-initial-setup-first-login.desktop
%attr(755,root,root) %{_libexecdir}/gnome-initial-setup
%attr(755,root,root) %{_libexecdir}/gnome-initial-setup-copy-worker
%attr(755,root,root) %{_libexecdir}/gnome-initial-setup-goa-helper
%{_datadir}/dconf/profile/gnome-initial-setup
%{_datadir}/gnome-initial-setup
%{_datadir}/gnome-session/sessions/gnome-initial-setup.session
%{_datadir}/gnome-shell/modes/initial-setup.json
%{_datadir}/polkit-1/rules.d/20-gnome-initial-setup.rules
%{_desktopdir}/gnome-initial-setup.desktop
%{systemduserunitdir}/gnome-session.target.wants/gnome-initial-setup-copy-worker.service
%{systemduserunitdir}/gnome-session.target.wants/gnome-initial-setup-first-login.service
%{systemduserunitdir}/gnome-session@gnome-initial-setup.target.d
%{systemduserunitdir}/gnome-initial-setup-copy-worker.service
%{systemduserunitdir}/gnome-initial-setup-first-login.service
#%{_prefix}/lib/sysusers.d/gnome-initial-setup.conf
