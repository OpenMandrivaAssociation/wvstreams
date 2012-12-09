%define major		4.6
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d
%define libname_orig	lib%{name}

Name:		wvstreams
Version:	4.6.1
Release:	8
License:	LGPLv2+
Group:		System/Libraries
Group:		Development/C
Summary:	Network programming library written in C++
URL:		http://code.google.com/p/wvstreams
Source0:	http://wvstreams.googlecode.com/files/%{name}-%{version}.tar.gz
Patch1:		wvstreams-4.2.2-multilib.patch
Patch2:		wvstreams-4.5-noxplctarget.patch
Patch3:		wvstreams-4.6.1-glibc212.patch
Patch4:		wvstreams-4.6.1-parallel-make.patch
Patch5:		wvstreams-4.6.1-openssl-1.0.0.patch
Patch6:		wvstreams-4.6.1-gcc47.patch
BuildRequires:	pkgconfig(openssl)
BuildRequires:	zlib-devel
BuildRequires:	libxplc-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(dbus-1)

%description
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%package -n uniconf
Group:		System/Configuration/Other
Summary:	Configuration system
Requires:	%{libname} = %{version}-%{release}

%description -n uniconf
UniConf is a configuration system that can serve as the centrepiece among 
many other, existing configuration systems. UniConf can also be accessed over 
the network, with authentication, allowing easy replication of configuration 
data via the UniReplicateGen. This package contains the server that accepts 
incoming TCP or Unix connections, and gets or sets UniConf elements at the 
request of a UniConf client. 

%package -n %{libname}
Group:		System/Libraries
Summary:	Network programming library written in C++

%description -n %{libname}
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development.

%package -n %{develname}
Summary:	Development files for WvStreams
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
WvStreams aims to be an efficient, secure, and easy-to-use library for
doing network applications development. This package contains the files
needed for developing applications which use WvStreams.

%prep
%setup -q
%patch1 -p1 -b .multilib
%patch2 -p1 -b .xplctarget
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p0

%build
CFLAGS="%{optflags} -fPIC -fpermissive" CXXFLAGS="%{optflags} -fPIC -fpermissive" %configure2_5x \
	--disable-static \
	--with-dbus=yes --with-pam \
	--with-openssl \
	--with-zlib \
	--with-qt=no \
	--with-pam=no \
	--with-tcl=no
%make

%install
%makeinstall_std

%files -n uniconf
%{_sysconfdir}/uniconf.conf
%{_bindir}/uni
%{_sbindir}/uniconfd
%{_mandir}/man8/*
%dir %{_localstatedir}/lib/uniconf
%{_localstatedir}/lib/uniconf/uniconfd.ini

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{develname}
%doc README
%{_bindir}/wsd
%{_bindir}/wvtestrun
%{_includedir}/wvstreams
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/valgrind/*.supp



%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 4.6.1-5mdv2011.0
+ Revision: 670817
- mass rebuild

* Sat Dec 04 2010 Funda Wang <fwang@mandriva.org> 4.6.1-4mdv2011.0
+ Revision: 609522
- add gentoo patches to fix build

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Fri Apr 09 2010 Ahmad Samir <ahmadsamir@mandriva.org> 4.6.1-3mdv2010.1
+ Revision: 533282
- rebuild for openssl-1.0.0

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 4.6.1-2mdv2010.1
+ Revision: 511661
- rebuilt against openssl-0.9.8m

* Sat Oct 03 2009 Funda Wang <fwang@mandriva.org> 4.6.1-1mdv2010.0
+ Revision: 453248
- New version 4.6.1

* Wed Feb 25 2009 Thierry Vignaud <tv@mandriva.org> 4.5-2mdv2009.1
+ Revision: 344806
- rebuild for new libreadline

* Sat Dec 20 2008 Adam Williamson <awilliamson@mandriva.org> 4.5-1mdv2009.1
+ Revision: 316380
- add gcc43.patch (couple of GCC 4.3 build fixes)
- drop ini-location.patch (localstatedir is now what it expects)
- new release 4.5
- misc spec cleanups

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 4.4-3mdv2008.1
+ Revision: 179668
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
    - kill re-definition of %%buildroot on Pixel's request
    - fix summary-ended-with-dot

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Sep 06 2007 Adam Williamson <awilliamson@mandriva.org> 4.4-1mdv2008.0
+ Revision: 80590
- use Fedora license policy
- drop patch2 (superseded upstream)
- new release 4.4

* Tue Jul 03 2007 Adam Williamson <awilliamson@mandriva.org> 4.3.90-2mdv2008.0
+ Revision: 47439
- rejig the fPIC stuff to (hopefully) make it stick
- new devel policy
- build against libreadline
- drop patch0 (merged upstream)
- new release 4.3.90 (test for 4.4 from mailing list)

* Thu May 03 2007 Adam Williamson <awilliamson@mandriva.org> 4.3-3mdv2008.0
+ Revision: 20813
- add conflict on previous -devel package (thanks gb and misc)

* Fri Apr 27 2007 Olivier Blin <oblin@mandriva.com> 4.3-2mdv2008.0
+ Revision: 18773
- drop xplc removal hack

* Fri Apr 27 2007 Adam Williamson <awilliamson@mandriva.org> 4.3-1mdv2008.0
+ Revision: 18449
- 4.3, rebuild for new era
- introduce new patches to fix build
- drop all old patches (no longer useful)
- don't build against db1 any more
- clean spec


* Sun Jan 14 2007 Olivier Blin <oblin@mandriva.com> 3.74.0-7mdv2007.0
+ Revision: 108656
- fix build by removing extra qualification
- remove dot in summary
- bunzip2 patches
- remove ssl 0.9.7 patch and rebuild with ssl 0.9.8 (#26240)

  + Jérôme Soyer <saispo@mandriva.org>
    - Rebuild with new openssl
    - Import wvstreams

* Thu Sep 08 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 3.74.0-5mdk
- fixes for new OpenSSL API (from wvstreams 4.0.2)

* Sat Jul 10 2004 Olivier Blin <blino@mandrake.org> 3.74.0-4mdk
- Patch2: gcc34 fixes

* Fri Apr 16 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.74.0-3mdk
- build fixes

* Sun Jan 18 2004 Olivier Blin <blino@mandrake.org> 3.74.0-2mdk
- buildrequires db1-devel
- disable unneeded options in configure (thanks to Charles A Edwards)

