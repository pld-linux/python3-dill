#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Serialize all of Python
Summary(pl.UTF-8):	Serializacja całości Pythona
Name:		python-dill
# keep 0.3.5.x here for python2 support
Version:	0.3.5.1
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/dill/
Source0:	https://files.pythonhosted.org/packages/source/d/dill/dill-%{version}.tar.gz
# Source0-md5:	3f8757f3aaa394efa67764624ab87cfd
URL:		https://pypi.org/project/dill/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dill extends Python's pickle module for serializing and de-serializing
Python objects to the majority of the built-in Python types.
Serialization is the process of converting an object to a byte stream,
and the inverse of which is converting a byte stream back to a Python
object hierarchy.

%description -l pl.UTF-8
dill rozszerza moduł Pythona pickle do serializacji i deserializacji
obiektów pythonowych na większość wbudowanych typów Pythona.
Serializacja to proces przekształcania obiektu na strumień bajtów, a
deserializacja - odwrotność, czyli konwersja strumienia bajtów z
powrotem do hierarchii obiektów Pythona.

%package -n python3-dill
Summary:	Serialize all of Python
Summary(pl.UTF-8):	Serializacja całości Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.7

%description -n python3-dill
dill extends Python's pickle module for serializing and de-serializing
Python objects to the majority of the built-in Python types.
Serialization is the process of converting an object to a byte stream,
and the inverse of which is converting a byte stream back to a Python
object hierarchy.

%description -n python3-dill -l pl.UTF-8
dill rozszerza moduł Pythona pickle do serializacji i deserializacji
obiektów pythonowych na większość wbudowanych typów Pythona.
Serializacja to proces przekształcania obiektu na strumień bajtów, a
deserializacja - odwrotność, czyli konwersja strumienia bajtów z
powrotem do hierarchii obiektów Pythona.

%package apidocs
Summary:	API documentation for Python dill module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona dill
Group:		Documentation

%description apidocs
API documentation for Python dill module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona dill.

%prep
%setup -q -n dill-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python} tests/__main__.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} tests/__main__.py
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

for bin in get_objgraph undill ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${bin} $RPM_BUILD_ROOT%{_bindir}/${bin}-2
done

%py_postclean
%endif

%if %{with python3}
%py3_install

for bin in get_objgraph undill ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${bin} $RPM_BUILD_ROOT%{_bindir}/${bin}-3
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/get_objgraph-2
%attr(755,root,root) %{_bindir}/undill-2
%{py_sitescriptdir}/dill
%{py_sitescriptdir}/dill-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-dill
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/get_objgraph-3
%attr(755,root,root) %{_bindir}/undill-3
%{py3_sitescriptdir}/dill
%{py3_sitescriptdir}/dill-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/{_static,*.html,*.js}
%endif
