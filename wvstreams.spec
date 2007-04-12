%define name 	wvstreams
%define version 3.74.0
%define release 7

%define major	3.74
%define libname %mklibname %{name} %{major}
%define libname_orig lib%{name}

Name:		%{name}
Version: 	%{version}
Release: 	%mkrel %release
License: 	LGPL
Group:          System/Libraries
Group:          Development/C
Summary: 	WvStreams is a network programming library written in C++
URL: 		http://open.nit.ca/wvstreams
Source: 	http://open.nit.ca/download/wvstreams-%{version}.tar.bz2
Patch0:		%{name}-%{version}-db1.patch
Patch1:		wvstreams-3.74.0-libs.patch
Patch2:		wvstreams-3.74.0-gcc34.patch
Patch3:		wvstreams-3.74.0-extra.patch
Patch4:		wvstreams-3.74.0-64bit-fixes.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: 	openssl-devel
BuildRequires: 	zlib-devel
BuildRequires:	db1-devel

%description
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%package -n %{libname}
Group:          System/Libraries
Summary: 	WvStreams is a network programming library written in C++.

%description -n %{libname}
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%package -n %{libname}-devel
Summary: Development files for WvStreams.
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: %{libname_orig}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development. This package contains the files
needed for developing applications which use WvStreams.

%prep
%setup -q
%patch0 -p1 -b .db1
%patch1 -p1 -b .libs
%patch2 -b .gcc34
%patch3 -p1 -b .extra
%patch4 -p1 -b .64bit-fixes

%build
%configure --with-bdb --with-openssl --with-zlib --with-fam=no --with-fftw=no --with-gdbm=no --with-gtk=no --with-ogg=no --with-pam=no --with-qt=no --with-speex=no --with-vorbis=no --with-xplc=no

%make COPTS="$RPM_OPT_FLAGS -fPIC" CXXOPTS="$RPM_OPT_FLAGS -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING.LIB README
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/wvstreams
%{_libdir}/*.a
%{_libdir}/*.so

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


