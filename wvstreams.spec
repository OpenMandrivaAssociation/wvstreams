%define major		4.6
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d
%define libname_orig	lib%{name}

Name:		wvstreams
Version: 	4.6.1
Release: 	%mkrel 2
License: 	LGPLv2+
Group:          System/Libraries
Group:          Development/C
Summary: 	Network programming library written in C++
URL: 		http://code.google.com/p/wvstreams
Source0: 	http://wvstreams.googlecode.com/files/%{name}-%{version}.tar.gz
Patch1:		wvstreams-4.2.2-multilib.patch
Patch2:		wvstreams-4.5-noxplctarget.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: 	openssl-devel
BuildRequires: 	zlib-devel
BuildRequires:	libxplc-devel
BuildRequires:	readline-devel
BuildRequires:	dbus-devel

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
%patch1 -p1 -b .multilib
%patch2 -p1 -b .xplctarget

%build
CFLAGS="%{optflags} -fPIC -fpermissive" CXXFLAGS="%{optflags} -fPIC -fpermissive" %configure2_5x \
	--disable-static \
	--with-dbus=yes --with-pam \
	--with-openssl \
	--with-zlib \
	--with-qt=no \
	--with-pam=no \
	--with-tcl=no
make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n uniconf
%defattr(-,root,root)
%{_sysconfdir}/uniconf.conf
%{_bindir}/uni
%{_sbindir}/uniconfd
%{_mandir}/man8/*
%dir %{_localstatedir}/lib/uniconf
%{_localstatedir}/lib/uniconf/uniconfd.ini

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%doc README
%defattr(-,root,root)
%{_bindir}/wsd
%{_bindir}/wvtestrun
%{_includedir}/wvstreams
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/valgrind/*.supp

