Summary:	Subroutines to solve a sparse linear system A*X=B
Summary(pl.UTF-8):	Procedury do rozwiązywania rzadkich układów równań liniowych A*X=B
Name:		SuperLU
Version:	7.0.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/xiaoyeli/superlu/releases
Source0:	https://github.com/xiaoyeli/superlu/archive/v%{version}/superlu-%{version}.tar.gz
# Source0-md5:	855cb57eb725535fd757564f220cd61e
Patch0:		%{name}-shared.patch
URL:		https://portal.nersc.gov/project/sparse/superlu/
BuildRequires:	blas-devel
BuildRequires:	cmake >= 3.12
BuildRequires:	gcc-fortran
BuildRequires:	metis-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SuperLU contains a set of subroutines to solve a sparse linear system
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP). The
columns of A may be preordered before factorization; the preordering
for sparsity is completely separate from the factorization.

%description -l pl.UTF-8
SuperLU zawiera zbiór procedur do rozwiązywania rzadkich układów
równań liniowych A*X=B. Wykorzystuje eliminację Gaussa z częściowym
wyborem elementu głównego (GEPP). Kolumny A mogą być wstępnie
uporządkowane przed rozkładem; ustalanie kolejności pod kątem
rzadkości jest całkowicie odrębne od samego rozkładu.

%package devel
Summary:	Header files for SuperLU library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SuperLU
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	blas-devel%{?_isa}
Requires:	metis-devel%{?_isa}
Obsoletes:	SuperLU-static < 5

%description devel
Header files for SuperLU library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SuperLU.

%package fortran
Summary:	Fortran interface for SuperLU library
Summary(pl.UTF-8):	Interfejs Fortrana do biblioteki SuperLU
Group:		Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description fortran
Fortran subroutines to solve a sparse linear system A*X=B.

%description fortran -l pl.UTF-8
Procedury Fortrana do rozwiązywania rzadkich układów równań liniowych
A*X=B.

%package fortran-devel
Summary:	Fortran interface for SuperLU library - development files
Summary(pl.UTF-8):	Interfejs Fortrana do biblioteki SuperLU - pliki programistyczne
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	%{name}-fortran%{?_isa} = %{version}-%{release}

%description fortran-devel
Fortran interface for SuperLU library - development files.

%description fortran-devel -l pl.UTF-8
Interfejs Fortrana do biblioteki SuperLU - pliki programistyczne.

%package apidocs
Summary:	SuperLU API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki SuperLU
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for SuperLU library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki SuperLU.

%prep
%setup -q -n superlu-%{version}
%patch -P0 -p1

%build
install -d build
cd build
# .pc file generation expects relative CMAKE_INSTALL_{INCLUDE,LIB}DIR
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include/superlu \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DTPL_ENABLE_METISLIB=ON \
	-DTPL_METIS_LIBRARIES=%{_libdir}/libmetis.so \
	-DTPL_METIS_INCLUDE_DIRS=%{_includedir} \
	-Denable_fortran=ON \
	-Denable_internal_blaslib=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# be consistent - base static lib is not built
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsuperlu_fortran.a

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc License.txt README
%{_libdir}/libsuperlu.so.*.*.*
%ghost %{_libdir}/libsuperlu.so.7

%files devel
%defattr(644,root,root,755)
%doc DOC/ug.pdf
%{_libdir}/libsuperlu.so
%dir %{_includedir}/superlu
%{_includedir}/superlu/*.h
%{_pkgconfigdir}/superlu.pc
%{_libdir}/cmake/superlu

%files fortran
%defattr(644,root,root,755)
%{_libdir}/libsuperlu_fortran.so.*.*.*
%ghost %{_libdir}/libsuperlu_fortran.so.7

%files fortran-devel
%defattr(644,root,root,755)
%{_libdir}/libsuperlu_fortran.so
%{_includedir}/superlu/superlu_config.fh
# FIXME: *.mod files are not created in 7.0.x?

%files apidocs
%defattr(644,root,root,755)
%doc DOC/html/*
