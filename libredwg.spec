%define oname LibreDWG
%define name %(echo %oname | tr [:upper:] [:lower:])

%define major 0
%define devname %mklibname %{name} -d
%define libname %mklibname %{name} %major

%define pyname	python-%{name}
%define plname	perl-%{name}

%bcond_without doc
%bcond_without perl
%bcond_without python
%bcond_with tests

Summary:	Free implementation of the DWG file format
Name:		libredwg
Version:	0.12.5
Release:	1
License:	GPLv3+
Group:		Development/C
URL:		https://savannah.gnu.org/projects/%{name}/
# take the source package fro ghithub mirror because tar from GNU is incomplete
#Source0:	https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source0:	https://github.com/LibreDWG/libredwg/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	gperf
BuildRequires:	jq
%if %{with perl}
BuildRequires:	perl
BuildRequires:  perl(Convert::Binary::C)
BuildRequires:  perl(ExtUtils::Embed)
%endif
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(libpcre2-16)
BuildRequires:	pkgconfig(libpcre2-32)
BuildRequires:	pkgconfig(libps)
BuildRequires:	pkgconfig(libwbxml2)
BuildRequires:	swig
%if %{with python}
BuildRequires:	pkgconfig(python3)
%endif
%if %{with doc}
BuildRequires:	doxygen
BuildRequires:	texinfo
%endif
%if %{with tests}
BuildRequires:	parallel
BuildRequires:	python3dist(lxml)
%endif


#- shellcheck to check shell scripts
#- rpmlint to check the spec validity
#- jinq with some svg11 relaxng to check SVG validity.
#  LaTeXML used to have a broken svg11-basic.rng. If so
#  the zip from http://yupotan.sppd.ne.jp/relax-ng/svg11/ is correct.
#  Needs to be installed into /usr/local/share/relaxng/svg11/
#- mapbox/geojsonhint as geojson linter
#  npm install -g @mapbox/geojsonhint
#- geojson-validation as 2nd geojson fallback linter
#  npm install -g geojson-validation
#- valgrind to find leaks and memory bugs
#- timeout to help tests with large or hanging DWG's
#- picat to find unknown fields, a better prolog. http://picat-lang.org/

%description
LibreDWG is a free C library to read and write DWG files.  This program is
part of the GNU project, released under the aegis of GNU.  It is licensed
under the terms of the GNU General Public License version 3 (or at you option
any later version).

DWG is a file format created in the 70's for the emerging CAD applications.
Currently it is the native file format of AutoCAD, a proprietary CAD program 
developed by AutoDesk.

LibreDWG is a fork from LibDWG due to its usage of Esperanto, which we
think is not the best strategy for a free software project which aims
to get lots of contributors.  LibreDWG is written in English.  At the
moment our decoder (i.e. reader) is done, just some very advanced
R2010+ and pre-R13 entities fail to read and are skipped over. The
writer is good enough for R2000.  Among the example applications we
wrote using LibreDWG is a reader, a writer, a rewriter (i.e. saveas),
an initial SVG and Postscript conversion, dxf and json converters,
dwggrep to search for text, and dwglayer to print the list of layers.
More are in the pipeline.

#---------------------------------------------------------------------------

%if %{with doc}
%package doc
Summary:	Includes html documentation for gdcm
BuildArch:	noarch

%description doc
LibreDWG is a free C library to read and write DWG files.  This program is
part of the GNU project, released under the aegis of GNU.  It is licensed
under the terms of the GNU General Public License version 3 (or at you option
any later version).

DWG is a file format created in the 70's for the emerging CAD applications.
Currently it is the native file format of AutoCAD, a proprietary CAD program 
developed by AutoDesk.

LibreDWG is a fork from LibDWG due to its usage of Esperanto, which we
think is not the best strategy for a free software project which aims
to get lots of contributors.  LibreDWG is written in English.  At the
moment our decoder (i.e. reader) is done, just some very advanced
R2010+ and pre-R13 entities fail to read and are skipped over. The
writer is good enough for R2000.  Among the example applications we
wrote using LibreDWG is a reader, a writer, a rewriter (i.e. saveas),
an initial SVG and Postscript conversion, dxf and json converters,
dwggrep to search for text, and dwglayer to print the list of layers.
More are in the pipeline.

You should install the libredwg-doc package if you would like to
access upstream documentation for libredwg.

%files doc
#{_datadir}/%{name}/doc/%{oname}.pdf
%{_datadir}/%{name}/doc/html
%endif

#---------------------------------------------------------------------------

%package applications
Summary:	Includes command line programs for GDCM
Requires:	%{libname} = %{EVRD}

%description applications
LibreDWG is a free C library to read and write DWG files.  This program is
part of the GNU project, released under the aegis of GNU.  It is licensed
under the terms of the GNU General Public License version 3 (or at you option
any later version).

DWG is a file format created in the 70's for the emerging CAD applications.
Currently it is the native file format of AutoCAD, a proprietary CAD program 
developed by AutoDesk.

LibreDWG is a fork from LibDWG due to its usage of Esperanto, which we
think is not the best strategy for a free software project which aims
to get lots of contributors.  LibreDWG is written in English.  At the
moment our decoder (i.e. reader) is done, just some very advanced
R2010+ and pre-R13 entities fail to read and are skipped over. The
writer is good enough for R2000.  Among the example applications we
wrote using LibreDWG is a reader, a writer, a rewriter (i.e. saveas),
an initial SVG and Postscript conversion, dxf and json converters,
dwggrep to search for text, and dwglayer to print the list of layers.
More are in the pipeline.

You should install the gdcm-applications package if you would like to
use command line programs part of GDCM. Includes reader, a writer, a
re-writer (i.e. SaveAS), an initial basic SVG and Postscript
conversion, experimental dxf and json converters, dwggrep to search
for text, dwglayer to print the list of layers, and dwgfilter to use
JQ expressions to query or change a DWG.

%files applications
%license COPYING
%doc README AUTHORS NEWS
%{_bindir}/*
%{_mandir}/man1/*.1.*
%{_mandir}/man5/dwg*
%{_infodir}/LibreDWG.info*
%{_datadir}/%{name}/examples/*

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	Free implementation of the DWG file format
Group:		System/Libraries

%description -n %{libname}
LibreDWG is a free C library to read and write DWG files.  This program is
part of the GNU project, released under the aegis of GNU.  It is licensed
under the terms of the GNU General Public License version 3 (or at you option
any later version).

DWG is a file format created in the 70's for the emerging CAD applications.
Currently it is the native file format of AutoCAD, a proprietary CAD program 
developed by AutoDesk.

LibreDWG is a fork from LibDWG due to its usage of Esperanto, which we
think is not the best strategy for a free software project which aims
to get lots of contributors.  LibreDWG is written in English.  At the
moment our decoder (i.e. reader) is done, just some very advanced
R2010+ and pre-R13 entities fail to read and are skipped over. The
writer is good enough for R2000.  Among the example applications we
wrote using LibreDWG is a reader, a writer, a rewriter (i.e. saveas),
an initial SVG and Postscript conversion, dxf and json converters,
dwggrep to search for text, and dwglayer to print the list of layers.
More are in the pipeline.

%files -n %libname
%{_libdir}/%{name}.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development libraries for %{oname}
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Libraries and headers required to develop software with %{oname}.

%files -n %{devname}
%doc TODO
%{_includedir}/*.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

#---------------------------------------------------------------------------

%if %{with python}
%package -n %pyname
Summary:	Python binding for %{oname}
%{?python_provide:%python_provide python-%{name}}
%{?python_provide:%python_provide python3dist(%{name})}
Requires:	%{libname} = %{EVRD}

%description -n %pyname
You should install this package if you would like to used this %{oname} with
python.

%files -n %pyname
%{python_sitelib}/%{oname}.py
%{python_sitelib}/__pycache__/%{oname}.*
%{python_sitearch}/_%{oname}.so*
%endif

#---------------------------------------------------------------------------

%if %{with perl}
%package -n %plname
Summary:	Perl binding for %{oname}
%{?perl_provide:%perl_provide perl-%{name}}

Requires:	%{libname} = %{EVRD}

%description -n %plname
You should install this package if you would like to used this %{oname} with
perl.

%files -n %plname
%{_libdir}/perl5/LibreDWG.pm
%{perl_vendorarch}/auto/LibreDWG/LibreDWG.so
%endif

#---------------------------------------------------------------------------

%prep
%autosetup

# fix version
sed -i -e "s|m4_esyscmd(\[build-aux/git-version-gen .tarball-version\])|[%{version}]|" configure.ac

# use system jsmn
sed -i -e 's|"../jsmn/jsmn.h"|<jsmn.h>|' src/in_json.c

%build
#autoreconf -fiv
%configure
%make_build

%if %{with doc}
make html #pdf
%endif

%install
%make_install

# Remove static libraries
find %{buildroot} -name '*.la' -delete

# fix examples path
install -dm 0755 %{buildroot}%{_datadir}/%{name}/examples
for e in dwgadd.example load_dwg.py
do
	mv %{buildroot}%{_datadir}/$e %{buildroot}%{_datadir}/%{name}/examples
done

# fix perl module path
%if %{with perl}
# Remove perllocal.pod and packlist files.
rm -f %{buildroot}/%{_libdir}/perl5/perllocal.pod
#rm %{buildroot}/%{perl_vendorarch}/auto/LibreDWG/.packlist

install -dm 0755 %{buildroot}/%{perl_vendorarch}/auto/%{oname}
mv %{buildroot}/%{_prefix}/local/%{_lib}/perl5/%{oname}.pm %{buildroot}%{_libdir}/perl5
mv %{buildroot}/%{_prefix}/local/%{_lib}/perl5/auto/%{oname}/*so %{buildroot}%{perl_vendorarch}/auto/%{oname}
chmod u+w %{buildroot}/%{perl_vendorarch}/auto/LibreDWG/LibreDWG.so
rm -rf %{buildroot}/%{_prefix}/local
%endif

# docs
%if %{with doc}
install -dm 0755 %{buildroot}%{_datadir}/%{name}/doc/html
install -pm 0644 doc/%{oname}.html/* %{buildroot}%{_datadir}/%{name}/doc/html
#install -pm 0644 doc/%{oname}.pdf %{buildroot}%{_datadir}/%{name}/doc
%endif

