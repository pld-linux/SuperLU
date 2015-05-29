Summary:	Subroutines to solve a sparse linear system A*X=B
Summary(pl.UTF-8):	Procedury do rozwiązywania rzadkich układów równań liniowych A*X=B
Name:		SuperLU
Version:	4.3
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_%{version}.tar.gz
# Source0-md5:	b72c6309f25e9660133007b82621ba7c
Patch0:		%{name}-format.patch
Patch1:		%{name}-shared.patch
URL:		http://crd-legacy.lbl.gov/~xiaoye/SuperLU/
BuildRequires:	blas-devel
BuildRequires:	libtool >= 2:1.5
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

%description devel
Header files for SuperLU library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SuperLU.

%package static
Summary:	Static SuperLU library
Summary(pl.UTF-8):	Statyczna biblioteka SuperLU
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SuperLU library.

%description static -l pl.UTF-8
Statyczna biblioteka SuperLU.

%package apidocs
Summary:	SuperLU API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki SuperLU
Group:		Documentation

%description apidocs
API documentation for SuperLU library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki SuperLU.

%prep
%setup -q -n SuperLU_%{version}
%patch0 -p1
%patch1 -p1

%build
%{__make} -C SRC \
	SuperLUroot=$(pwd) \
	BLASLIB="-lblas" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -DPRNTlevel=0" \
	FFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/superlu}

libtool --mode=install install lib/libsuperlu.la $RPM_BUILD_ROOT%{_libdir}
cp -p SRC/slu_*.h SRC/super*.h $RPM_BUILD_ROOT%{_includedir}/superlu

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libsuperlu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsuperlu.so.0

%files devel
%defattr(644,root,root,755)
%doc DOC/ug.pdf
%attr(755,root,root) %{_libdir}/libsuperlu.so
%{_libdir}/libsuperlu.la
%{_includedir}/superlu

%files static
%defattr(644,root,root,755)
%{_libdir}/libsuperlu.a

%files apidocs
%defattr(644,root,root,755)
%doc DOC/html/*
