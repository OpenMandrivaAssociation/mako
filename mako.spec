Name:       mako
Version:	1.4.1
Release:	2
Summary:    Lightweight Wayland notification daemon
Provides:   desktop-notification-daemon

License:    MIT
URL:        https://github.com/emersion/%{name}
Source0:    https://github.com/emersion/mako/archive/v%{version}.tar.gz
# Add dbus-activated systemd unit as required by the packaging guidelines. To
# be upstreamed as discussed in RHBZ#1689634.
Source1:    %{name}.service

Patch0: add-systemd-service-dbus.patch
Patch1: meson-disable-werror.patch

BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.14
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  scdoc
Requires:       dbus

%description
mako is a lightweight notification daemon for Wayland compositors that support
the layer-shell protocol.

%prep
%autosetup

%build
%meson -Dzsh-completions=true
%meson_build

%install
%meson_install

# Install dbus-activated systemd unit
install -m0644 -Dt %{buildroot}%{_userunitdir}/ %{SOURCE1}

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/mako
%{_bindir}/makoctl
%{_mandir}/man1/mako.1*
%{_mandir}/man1/makoctl.1*
%{_mandir}/man5/%{name}.5.*
%{_userunitdir}/%{name}.service
%{_datadir}/dbus-1/services/fr.emersion.mako.service
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_mako*
