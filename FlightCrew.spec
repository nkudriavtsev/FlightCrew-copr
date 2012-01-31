Name:           FlightCrew
Version:        0.7.2
Release:        2%{?dist}
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
Patch11:        0011-allow-building-zipios-as-a-shared-lib.patch

BuildRequires:  cmake
BuildRequires:  zlib-devel
BuildRequires:  boost-devel
BuildRequires:  xerces-c-devel >= 3.1


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

# Fix EOL encoding for %%doc
for i in COPYING*.txt ChangeLog.txt; do
    sed -i.old 's/\r//' "$i"
    touch -r "$i.old" "$i"
done

# remove unbundled stuff
rm -rf src/BoostParts src/zlib src/Xerces
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
* Thu Jan 12 2012 Hans de Goede <hdegoede@redhat.com> - 0.7.2-2
- Make -devel package Requires on main package include isa
- Drop buildroot and defattr boilerplate (no longer needed with recent rpm)
- Split the use-system-libs patch into its sub patches
- Add a FindFlightCrew cmake module
- Build XercesExtensions as a shared lib (including a Find... cmake module)

* Sat Dec 24 2011 Dan Horák <dan[at]danny.cz> - 0.7.2-1
- initial Fedora version
