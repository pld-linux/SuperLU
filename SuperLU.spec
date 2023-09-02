Summary:	Subroutines to solve a sparse linear system A*X=B
Summary(pl.UTF-8):	Procedury do rozwiązywania rzadkich układów równań liniowych A*X=B
Name:		SuperLU
Version:	5.3.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/xiaoyeli/superlu/releases
Source0:	https://github.com/xiaoyeli/superlu/archive/v%{version}/superlu-%{version}.tar.gz
# Source0-md5:	3a5123b86bd517fe28c830ae7d12cb25
Patch0:		%{name}-shared.patch
URL:		https://portal.nersc.gov/project/sparse/superlu/
BuildRequires:	blas-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gcc-fortran
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
Requires:	%{name} = %{version}-%{release}
Requires:	blas-devel
Obsoletes:	SuperLU-static < 5

%description devel
Header files for SuperLU library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SuperLU.

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
%patch0 -p1

%build
install -d build
cd build
# .pc file generation expects relative CMAKE_INSTALL_{INCLUDE,LIB}DIR
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include/superlu \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-Denable_internal_blaslib=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc License.txt README
%attr(755,root,root) %{_libdir}/libsuperlu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsuperlu.so.5

%files devel
%defattr(644,root,root,755)
%doc DOC/ug.pdf
%attr(755,root,root) %{_libdir}/libsuperlu.so
%{_includedir}/superlu
%{_pkgconfigdir}/superlu.pc
%{_libdir}/cmake/superlu

%files apidocs
%defattr(644,root,root,755)
%doc DOC/html/*
