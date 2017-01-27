Name:           FlightCrew
Version:        0.9.1
Release:        5%{?dist}
Summary:        EPUB validator
License:        LGPLv3+
URL:            https://sigil-ebook.com/
Source0:        https://github.com/Sigil-Ebook/flightcrew/releases/download/%{version}/FlightCrew-%{version}-Code.zip
Source1:        flightcrew-sigil-plugin.metainfo.xml
Patch1:         0001-use-system-zlib-if-available.patch
Patch2:         0002-use-system-boost-libraries-if-available.patch
Patch3:         0003-use-system-xerces-c-if-available.patch
Patch4:         0004-don-t-build-googlemock-when-NO_TEST_EXE-is-specified.patch
Patch5:         0005-move-zipextraction-under-FlightCrew.patch
Patch6:         0006-use-system-zipios-library-if-available.patch
Patch7:         0007-FlightCrew-plugin-Make-FlightCrew-plugin-work-on-uni.patch
BuildRequires:  cmake libappstream-glib
BuildRequires:  zlib-devel
BuildRequires:  boost-devel
BuildRequires:  xerces-c-devel >= 3.1
BuildRequires:  zipios++-devel
BuildRequires:  python3-devel

%description
FlightCrew is a C++ epub validator.


%package        sigil-plugin
Summary:        Sigil FlightCrew epub validator plugin
Requires:       sigil
# Older versions of FlightCrew were directly linked into sigil, we
# hacked up the FlightCrew build to produce a dynamic-lib to make this
# work, but upstream never intended FlightCrew to be used this way and
# with the plugin this is no longer necessary
Obsoletes:      %{name} <= 0.8
Obsoletes:      %{name}-devel <= 0.8

%description    sigil-plugin
Sigil FlightCrew epub validator plugin.


%package        cli
Summary:        FlightCrew cli epub validator

%description    cli
FlightCrew cli epub validator.


%prep
%setup -q -c
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# Fix EOL encoding for %%doc
for i in COPYING*.txt ChangeLog.txt README.txt; do
    sed -i.old 's/\r//' "$i"
    touch -r "$i.old" "$i"
done

# remove unbundled stuff
rm -rf src/BoostParts src/zlib src/Xerces src/zipios
# remove test framework
rm -rf src/googlemock

# fix permissions
chmod a-x src/utf8-cpp/utf8/*.h

# Fix python shebang
sed -i '1s=^#!/usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' src/FlightCrew-plugin/plugin.py

%build
mkdir build
pushd build
%{cmake} -DBUILD_SHARED_LIBS:BOOL=OFF -DSKIP_FC_GUI=1 -DNO_TEST_EXE=1 ..
make %{?_smp_mflags}
popd


%install
pushd build
%make_install
popd
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sigil/plugins/%{name}
install -p -m 755 src/FlightCrew-plugin/plugin.py \
  $RPM_BUILD_ROOT%{_datadir}/sigil/plugins/%{name}
install -p -m 644 src/FlightCrew-plugin/plugin.xml \
  $RPM_BUILD_ROOT%{_datadir}/sigil/plugins/%{name}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/appdata
appstream-util validate-relax --nonet \
  $RPM_BUILD_ROOT%{_datadir}/appdata/flightcrew-sigil-plugin.metainfo.xml


%files sigil-plugin
%doc ChangeLog.txt README.txt
%license COPYING*.txt
%{_bindir}/flightcrew-plugin
%{_datadir}/appdata/flightcrew-sigil-plugin.metainfo.xml
%{_datadir}/sigil/plugins/%{name}

%files cli
%doc ChangeLog.txt README.txt
%license COPYING*.txt
%{_bindir}/flightcrew-cli


%changelog
* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.9.1-5
- Rebuilt for Boost 1.63

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-4
- Rebuild for Python 3.6

* Tue Aug 09 2016 Lumir Balhar <lbalhar@redhat.com> - 0.9.1-3
- Added `sed` to specfile to change shebang to python3

* Mon May 16 2016 Jonathan Wakely <jwakely@redhat.com> - 0.9.1-2
- Rebuilt for linker errors in boost (#1331983)

* Thu Feb 25 2016 Hans de Goede <hdegoede@redhat.com> - 0.9.1-1
- Update to 0.9.1
- No longer build as a library for use in sigil, instead
  provide a -sigil-plugin sub-package for sigil
- Make -sigil-plugin obsolete the old main (lib) and devel package
- Add -cli sub-package with the cli version of FlightCrew

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Jonathan Wakely <jwakely@redhat.com> - 0.7.2-20
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.7.2-19
- Rebuilt for Boost 1.59

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
