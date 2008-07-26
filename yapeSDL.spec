Name: yapeSDL
Version: 0.32.4       
Release: 2%{?dist}
Summary: YAPE, yet another plus/4 emulator

Group: Applications/Emulators
License: GPLv2+
URL: http://yape.plus4.net/
Source: http://yape.homeserver.hu/download/%{name}-%{version}.tar.gz        
# OpenSUSE
Patch0: %{name}-0.32.4-gcc4_cflags.patch
# FreeBSD
Patch1: %{name}-0.32.4-homedir.patch
# Andrea Musuruane
Patch2: %{name}-0.32.4-loadfile.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: SDL-devel >= 0:1.2

%description
YAPE is a rather decent plus/4 emulator. It has been developed for 
several years by now and it is available in Windows and 
multiplatform editions, although the latter lags several versions 
behind the first. 

%prep
%setup -q -c -n %{name}-%{version}
%patch0 -p0
%patch1 -p1
%patch2 -p1

# Fix end-of-line-encoding
sed -i 's/\r//' *.{cpp,h} Changes README.SDL copying

# Fix UTF-8 encoding
iconv --from=ISO-8859-1 --to=UTF-8 README.SDL > README.SDL.utf8
mv README.SDL.utf8 README.SDL

# Fix spurious executable permissions
chmod 644 *.{cpp,h} Changes README.SDL copying


%build
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 yape %{buildroot}%{_bindir}/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Changes copying README.SDL
%defattr(-,root,root,0755)
%{_bindir}/yape

%changelog
* Tue Feb 26 2008 Andrea Musuruane <musuruan@gmail.com> 0.32.4-2
- Minor cleanup

* Sun Jan 27 2008 Andrea Musuruane <musuruan@gmail.com> 0.32.4-1
- Initial RPM release
- Used a patch from OpenSUSE to compile with GCC4 and to use RPM_OPT_FLAGS
- Used a patch from FreeBSD to change homedir to .yape
- Made a patch to fix loading tap and prg files supplied in the command line

