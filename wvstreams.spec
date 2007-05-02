%define name 	wvstreams
%define version 4.3
%define release %mkrel 3

%define major	4.3
%define libname %mklibname %{name} %{major}
%define libname_orig lib%{name}

Name:		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	LGPL
Group:          System/Libraries
Group:          Development/C
Summary: 	WvStreams is a network programming library written in C++
URL: 		http://open.nit.ca/wvstreams
Source: 	http://open.nit.ca/download/wvstreams-%{version}.tar.bz2
# Adapted from Ubuntu patch in 4.2.2-2.2ubuntu2
Patch0:		wvstreams-4.3-build.patch
# Install .ini file to /var/lib , not /var/lib/lib
Patch1:		wvstreams-4.3-ini-location.patch
# Change 'unsigned' to 'unsigned long' to fix x86-64 build
Patch2:		wvstreams-4.3-x86_64build.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: 	openssl-devel
BuildRequires: 	zlib-devel
BuildRequires:	libxplc-devel

%description
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%package -n uniconf
Group:		System/Configuration/Other
Summary:	UniConf is a configuration system
Requires: 	%{libname} = %{version}-%{release}

%description -n uniconf
UniConf is a configuration system that can serve as the centrepiece among 
many other, existing configuration systems. UniConf can also be accessed over 
the network, with authentication, allowing easy replication of configuration 
data via the UniReplicateGen. This package contains the server that accepts 
incoming TCP or Unix connections, and gets or sets UniConf elements at the 
request of a UniConf client. 

%package -n %{libname}
Group:          System/Libraries
Summary: 	WvStreams is a network programming library written in C++

%description -n %{libname}
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%package -n %{libname}-devel
Summary: 	Development files for WvStreams.
Group: 		Development/C
Requires: 	%{libname} = %{version}-%{release}
Provides: 	%{libname_orig}-devel = %{version}-%{release}
Provides: 	%{name}-devel = %{version}-%{release}
Conflicts:	libwvstreams3.74-devel

%description -n %{libname}-devel
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development. This package contains the files
needed for developing applications which use WvStreams.

%prep
%setup -q
%patch0 -p1 -b .build
%patch1 -p1 -b .ini
%patch2 -p1 -b .x86_64

%build
%configure --with-openssl --with-zlib --with-qdbm=no --with-qt=no --with-pam=no --with-qt=no --with-telephony=no --with-tcl=no --with-swig=no --with-openslp=no

%make COPTS="$RPM_OPT_FLAGS -fPIC" CXXOPTS="$RPM_OPT_FLAGS -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n uniconf
%defattr(-,root,root)
%{_sysconfdir}/uniconf.conf
%{_bindir}/uni
%{_sbindir}/uniconfd
%{_mandir}/man8/*
%dir %{_localstatedir}/uniconf
%{_localstatedir}/uniconf/uniconfd.ini

%files -n %{libname}
%doc COPYING.LIB README
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/wvstreams
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
