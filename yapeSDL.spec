Name: yapeSDL
Version: 0.80.1
Release: 2%{?dist}
Summary: A Commodore 264 family (C16, plus/4 etc.) emulator

License: GPL-2.0-or-later
URL: https://github.com/calmopyrin/yapesdl
Source: https://github.com/calmopyrin/yapesdl/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: %{name}.desktop
Source2: %{name}.appdata.xml
# Force switch when dialog window fails to show
# https://github.com/calmopyrin/yapesdl/commit/f28839b5d51c9a86bfe850b2278db06daba42709
Patch0: %{name}-0.80.1-force_machine_switch.patch

BuildRequires: gcc-c++
BuildRequires: SDL2-devel
BuildRequires: minizip-compat-devel
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
Requires: hicolor-icon-theme


%description
yapeSDL is a decent no-nonsense Commodore 264 family (C16, plus/4 etc.)
emulator.

Features:
 - full, cycle exact MOS 6502/6510/7501/8501 CPU emulation
 - almost full MOS 7360/8360 aka 'TED' chip emulation
 - almost complete MOS 6569 aka 'VIC-II' chip emulation
 - reasonable MOS 6581/8580 aka 'SID' chip emulation
 - somewhat incomplete CIA 6526 aka 'CIA' emulation
 - real 1541 drive emulation (Read/Write)
 - full ROM banking on +4
 - almost full tape emulation
 - joystick emulation via cursor keys and gamepads
 - PRG, P00, T64, D64 and TAP file format support
 - partial CRT emulation
 - serial IEC disk LOAD/SAVE to the file system
 - snapshots / savestates

%prep
%autosetup -n yapesdl-%{version} -p1

# Fix UTF-8 encoding
iconv --from=ISO-8859-1 --to=UTF-8 README.SDL > README.SDL.utf8
mv README.SDL.utf8 README.SDL

# Remove bundled libs
rm -rf zlib

# Fix unzip.h include path
sed -i 's!#include "zlib/unzip.h"!#include "minizip/unzip.h"!' archdep.cpp

# Use CFLAGS
# Define ZIP_SUPPORT for preliminary ZIP file support
sed -i 's/cflags = -O3 -w/cflags = $(CFLAGS) -DZIP_SUPPORT/' Makefile

# Use LDFLAGS
# Add libminizip to libs
sed -i 's/libs = /libs = $(LDFLAGS) -lminizip /' Makefile

# Don't strip binary
sed -i 's/-o $(EXENAME) -s/-o $(EXENAME)/' Makefile


%build
%set_build_flags macro
%make_build


%install
install -d %{buildroot}%{_bindir}
install -p -m 755 yapesdl %{buildroot}%{_bindir}/

# Install desktop file
install -d %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE1}

# Install icon
install -d %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 plus4.xcassets/MacAppIcon.appiconset/icon_32x32.png \
   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

# Install AppData file
install -d %{buildroot}%{_metainfodir}
install -p -m 644 %{SOURCE2} %{buildroot}%{_metainfodir}
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%{_bindir}/yapesdl
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_metainfodir}/%{name}.appdata.xml
%doc Changes README.SDL
%license COPYING

%changelog
* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.80.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jul 30 2024 Andrea Musuruane <musuruan@gmail.com> - 0.80.1-1
- Updated to upstream 0.80.1

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.71.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.71.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 10 2023 Andrea Musuruane <musuruan@gmail.com> - 0.71.2-1
- Updated to upstream 0.71.2

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.70.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.70.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.70.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.70.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.70.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.70.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.70.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 07 2019 Andrea Musuruane <musuruan@gmail.com> - 0.70.2-8
- Updated BR to minizip-compat-devel for F30+
- Used %%set_build_flags macro

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.70.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.70.2-6
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Sat Jul 28 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 0.70.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 17 2018 Andrea Musuruane <musuruan@gmail.com> - 0.70.2-4
- Added gcc dependency
- Fixed AppData file
- Added license tag

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.70.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 14 2018 Andrea Musuruane <musuruan@gmail.com> - 0.70.2-2
- Fixed missing AppData file

* Sun Jan 14 2018 Andrea Musuruane <musuruan@gmail.com> - 0.70.2-1
- Updated to upstream 0.70.2
- Updated description
- Fixed LDFLAGS usage
- Added AppData file
- Removed obsolete scriptlets
- Cleanup

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.70.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.70.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 25 2016 Andrea Musuruane <musuruan@gmail.com> - 0.70.1-1
- Updated to upstream 0.70.1
- Updated summary and description

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

