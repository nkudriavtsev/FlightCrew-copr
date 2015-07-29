Name:           FlightCrew
Version:        0.7.2
Release:        18%{?dist}
Summary:        EPUB validation library

Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://code.google.com/p/flightcrew/
Source0:        http://flightcrew.googlecode.com/files/%{name}-%{version}-Code.zip
Patch1:         0001-add-versioning-information-to-the-shared-library.patch
Patch2:         0002-fix-building-as-a-shared-library-on-Unix.patch
Patch3:         0003-use-system-zlib-if-available.patch
Patch4:         0004-use-system-boost-libraries-if-available.patch
Patch5:         0005-fix-build-with-boost-1.48.patch
Patch6:         0006-use-system-xerces-c-if-available.patch
Patch7:         0007-install-FlightCrew-library-and-headers.patch
Patch8:         0008-don-t-build-googlemock-when-NO_TEST_EXE-is-specified.patch
Patch9:         0009-Add-a-FindFlightCrew.cmake-cmake-module.patch
Patch10:        0010-allow-building-XercesExtensions-as-a-shared-lib.patch
Patch11:        0011-move-zipextraction-under-FlightCrew.patch
Patch12:        0012-use-system-zipios-library-if-available.patch

BuildRequires:  cmake
BuildRequires:  zlib-devel
BuildRequires:  boost-devel
BuildRequires:  xerces-c-devel >= 3.1
BuildRequires:  zipios++-devel


%description
FlightCrew is a C++, cross-platform, native code epub validator.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -c
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

# Fix EOL encoding for %%doc
for i in COPYING*.txt ChangeLog.txt; do
    sed -i.old 's/\r//' "$i"
    touch -r "$i.old" "$i"
done

# remove unbundled stuff
rm -rf src/BoostParts src/zlib src/Xerces src/zipios
# remove test framework
rm -rf src/googlemock

# fix permissions
chmod a-x src/utf8-cpp/utf8/*.h


%build
mkdir build
cd build
%{cmake} -DBUILD_SHARED_LIBS:BOOL=OFF -DBUILD_SHARED_FC=1 -DBUILD_SHARED_XE=1 -DSKIP_FC_GUI=1 -DNO_TEST_EXE=1 ..
make %{?_smp_mflags}


%install
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING*.txt ChangeLog.txt
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}/
%{_includedir}/XercesExtensions/
%{_libdir}/*.so
%{_libdir}/cmake


%changelog
* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-18
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.7.2-17
- rebuild for Boost 1.58

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.7.2-15
- Rebuilt for GCC 5 C++11 ABI change

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.7.2-14
- Rebuild for boost 1.57.0

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.7.2-11
- Rebuild for boost 1.55.0

* Wed Mar 19 2014 Dan Horák <dan[at]danny.cz> - 0.7.2-10
- Build with system zipios++ library (#1077716)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 0.7.2-8
- Rebuild for boost 1.54.0

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.7.2-7
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.7.2-6
- Rebuild for Boost-1.53.0

* Sun Aug 12 2012 Kevin Fenzi <kevin@scrye.com> - 0.7.2-5
- Rebuild for new boost

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Hans de Goede <hdegoede@redhat.com> - 0.7.2-2
- Make -devel package Requires on main package include isa
- Drop buildroot and defattr boilerplate (no longer needed with recent rpm)
- Split the use-system-libs patch into its sub patches
- Add a FindFlightCrew cmake module
- Build XercesExtensions as a shared lib (including a Find... cmake module)

* Sat Dec 24 2011 Dan Horák <dan[at]danny.cz> - 0.7.2-1
- initial Fedora version
