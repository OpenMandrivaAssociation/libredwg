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
Version:	0.12.5.6517
Release:	1
License:	GPLv3+
Group:		Development/C
URL:		https://savannah.gnu.org/projects/%{name}/
# source package from GNU is incomplete, so for now use the github mirror
#Source0:	https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source0:	https://github.com/LibreDWG/libredwg/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Patch0:		libredwg-0.12.5.6517-clang.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	gperf
BuildRequires:	jq
BuildRequires:	jsmn-devel
BuildRequires:	git-core
%if %{with perl}
BuildRequires:	perl
#BuildRequires:	perl(Convert::Binary::C)
BuildRequires:	perl(ExtUtils::Embed)
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

%files
%license COPYING
%doc README AUTHORS NEWS
%{_bindir}/*
%{_mandir}/man1/*.1.*
%{_mandir}/man5/dwg*
%{_infodir}/LibreDWG.info*
%{_datadir}/%{name}

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

%files -n %{libname}
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
%package -n %{pyname}
Summary:	Python binding for %{oname}
%{?python_provide:%python_provide python-%{name}}
%{?python_provide:%python_provide python3dist(%{name})}
Requires:	%{libname} = %{EVRD}

%description -n %{pyname}
You should install this package if you would like to used this %{oname} with
python.

%files -n %{pyname}
%{python_sitelib}/%{oname}.py
%{python_sitelib}/__pycache__/%{oname}.*
%{python_sitearch}/_%{oname}.so*
%endif

#---------------------------------------------------------------------------

%if %{with perl}
%package -n %{plname}
Summary:	Perl binding for %{oname}
%{?perl_provide:%perl_provide perl-%{name}}

Requires:	%{libname} = %{EVRD}

%description -n %{plname}
You should install this package if you would like to used this %{oname} with
perl.

%files -n %{plname}
%{_libdir}/perl5/LibreDWG.pm
%{perl_vendorarch}/auto/LibreDWG/LibreDWG.so
%endif

#---------------------------------------------------------------------------

%if %{with doc}
%package doc
Summary:	Includes html documentation for %{oname}
BuildArch:	noarch

%description doc
You should install the this package if you would like to access upstream
documentation for %{oname}.

%files doc
#{_datadir}/%{name}/doc/%{oname}.pdf
%{_datadir}/%{name}/doc/html
%endif

#---------------------------------------------------------------------------

%prep
%autosetup -p1

# fix version
sed -i -e "s|m4_esyscmd(\[build-aux/git-version-gen .tarball-version\])|[%{version}]|" configure.ac

# use system jsmn
sed -i -e 's|"../jsmn/jsmn.h"|<jsmn.h>|' src/in_json.c

%build
#autoreconf -fiv
%configure \
	--enable-write
%make_build

%if %{with doc}
make html #pdf
%endif

%install
%make_install

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
