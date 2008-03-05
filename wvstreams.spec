%define name 	wvstreams
%define version 4.4

%define major	4.4
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define libname_orig lib%{name}

Name:		%{name}
Version: 	%{version}
Release: 	%mkrel 3
License: 	LGPLv2+
Group:          System/Libraries
Group:          Development/C
Summary: 	Network programming library written in C++
URL: 		http://open.nit.ca/wvstreams
Source: 	http://open.nit.ca/download/wvstreams-%{version}.tar.gz
# Install .ini file to /var/lib , not /var/lib/lib
Patch1:		wvstreams-4.3-ini-location.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: 	openssl-devel
BuildRequires: 	zlib-devel
BuildRequires:	libxplc-devel
BuildRequires:	readline-devel

%description
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%package -n uniconf
Group:		System/Configuration/Other
Summary:	Configuration system
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
Summary: 	Network programming library written in C++

%description -n %{libname}
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%package -n %{develname}
Summary: 	Development files for WvStreams
Group: 		Development/C
Requires: 	%{libname} = %{version}-%{release}
Provides: 	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}%{name}4.3-devel

%description -n %{develname}
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development. This package contains the files
needed for developing applications which use WvStreams.

%prep
%setup -q
#%patch0 -p1 -b .build
%patch1 -p1 -b .ini

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC" CXXFLAGS="$RPM_OPT_FLAGS -fPIC" %configure --with-openssl --with-zlib --with-qdbm=no --with-qt=no --with-pam=no --with-qt=no --with-telephony=no --with-tcl=no --with-swig=no --with-openslp=no

CFLAGS="$RPM_OPT_FLAGS -fPIC" CXXFLAGS="$RPM_OPT_FLAGS -fPIC" %make

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

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/wvstreams
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
