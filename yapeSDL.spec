%global commit f34a47a03051

Name: yapeSDL
Version: 0.58.2
Release: 1%{?dist}
Summary: Yet another plus/4 emulator

License: GPLv2+
URL: http://yape.plus4.net/
Source: https://download-codeplex.sec.s-msft.com/Download/SourceControlFileDownload.ashx?ProjectName=yapesdl&changeSetId=%{commit}#/%{name}-%{version}.zip
Source1: %{name}.desktop
# Icon taken from
# http://ahlberg.deviantart.com/art/Commodore-Icons-70563314
# License:
# These icons are FREE! Feel free to use them in your applications, 
# on your site, signature on a forum or whatever.
Source2: Plus4.png

BuildRequires: SDL2-devel
BuildRequires: desktop-file-utils
Requires: hicolor-icon-theme


%description
YAPE is a rather decent plus/4 emulator. It has been developed for 
several years by now and it is available in Windows and 
multiplatform editions, although the latter lags several versions 
behind the first. 

%prep
%setup -q -c -n %{name}-%{version}

# Fix UTF-8 encoding
iconv --from=ISO-8859-1 --to=UTF-8 README.SDL > README.SDL.utf8
mv README.SDL.utf8 README.SDL

# Fix end-of-line encoding
for txtfile in COPYING README.SDL Changes
do
    sed -i 's/\r//' $txtfile
done

# Use RPM_OPT_FLAGS
sed -i 's/cflags = -O3 -w/cflags = $(RPM_OPT_FLAGS)/' Makefile

# Don't strip binary
sed -i 's/-o $(EXENAME) -s/-o $(EXENAME)/' Makefile


%build
make %{?_smp_mflags}


%install
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 yapesdl %{buildroot}%{_bindir}/

# install desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE1}

# install icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
cp %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/yapesdl
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc Changes COPYING README.SDL

%changelog
* Sat Oct 17 2015 Andrea Musuruane <musuruan@gmail.com> - 0.58.2-1
- Updated to upstream 0.58.2

* Sat Aug 15 2015 Andrea Musuruane <musuruan@gmail.com> - 0.58.1-1
- Updated to upstream 0.58.1

* Wed Jun 10 2015 Andrea Musuruane <musuruan@gmail.com> - 0.36.2-2
- Fixed BuildRequires

* Tue Jun 02 2015 Andrea Musuruane <musuruan@gmail.com> - 0.36.2-1
- Updated to upstream 0.36.2
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Dropped cleaning at the beginning of %%install
- Updated icon cache scriptlets to be compliant to new guidelines

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.32.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.32.5-5
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.32.5-4
- Rebuilt for c++ ABI breakage

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

