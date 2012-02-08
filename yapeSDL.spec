Name: yapeSDL
Version: 0.32.5       
Release: 3%{?dist}
Summary: Yet another plus/4 emulator

Group: Applications/Emulators
License: GPLv2+
URL: http://yape.plus4.net/
Source: http://yape.homeserver.hu/download/%{name}-%{version}.tar.gz        
Source1: %{name}.desktop
# Icon taken from
# http://ahlberg.deviantart.com/art/Commodore-Icons-70563314
# License:
# These icons are FREE! Feel free to use them in your applications, 
# on your site, signature on a forum or whatever.
Source2: Plus4.png
# Andrea Musuruane
Patch0: %{name}-0.32.5-cflags.patch
Patch1: %{name}-0.32.5-homedir.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: SDL-devel >= 0:1.2
BuildRequires: desktop-file-utils
Requires: hicolor-icon-theme


%description
YAPE is a rather decent plus/4 emulator. It has been developed for 
several years by now and it is available in Windows and 
multiplatform editions, although the latter lags several versions 
behind the first. 

%prep
%setup -q -c -n %{name}-%{version}
%patch0 -p0
%patch1 -p0

# Fix end-of-line-encoding
sed -i 's/\r//' *.{cpp,h} Changes README.SDL COPYING

# Fix UTF-8 encoding
iconv --from=ISO-8859-1 --to=UTF-8 README.SDL > README.SDL.utf8
mv README.SDL.utf8 README.SDL

# Fix spurious executable permissions
chmod 644 *.{cpp,h} Changes README.SDL COPYING


%build
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 yape %{buildroot}%{_bindir}/

# install desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor '' \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE1}

# install icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
cp %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/yape
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc Changes COPYING README.SDL

%changelog
* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.32.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.32.5-2
- rebuild for new F11 features

* Wed Dec 03 2008 Andrea Musuruane <musuruan@gmail.com> 0.32.5-1
- Updated to upstream 0.32.5
- Version 0.32.5 ships a small GUI - added a desktop entry and an icon
- Removed the name from the summary

* Tue Feb 26 2008 Andrea Musuruane <musuruan@gmail.com> 0.32.4-2
- Minor cleanup

* Sun Jan 27 2008 Andrea Musuruane <musuruan@gmail.com> 0.32.4-1
- Initial RPM release
- Used a patch from OpenSUSE to compile with GCC4 and to use RPM_OPT_FLAGS
- Used a patch from FreeBSD to change homedir to .yape
- Made a patch to fix loading tap and prg files supplied in the command line

