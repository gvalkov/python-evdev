Name:           python-evdev
Version:        0.6.1
Release:        1%{?dist}
Summary:        Python bindings for the Linux input handling subsystem

License:        BSD
URL:            https://python-evdev.readthedocs.io
Source0:        https://github.com/gvalkov/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  kernel-headers
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  python2-setuptools
BuildRequires:  python3-setuptools


%global _description \
This package provides python bindings to the generic input event interface in \
Linux. The evdev interface serves the purpose of passing events generated in \
the kernel directly to userspace through character devices that are typically \
located in /dev/input/. \
 \
This package also comes with bindings to uinput, the userspace input subsystem. \
Uinput allows userspace programs to create and handle input devices that can \
inject events directly into the input subsystem. \
 \
In other words, python-evdev allows you to read and write input events on Linux. \
An event can be a key or button press, a mouse movement or a tap on a \
touchscreen.


%description %{_description}


%package -n python2-evdev
Summary:        %{summary}
%{?python_provide:%python_provide python2-evdev}
%description -n python2-evdev %{_description}


%package -n python3-evdev
Summary:        %{summary}
%{?python_provide:%python_provide python3-evdev}
%description -n python3-evdev %{_description}


#------------------------------------------------------------------------------
%prep
%autosetup

#------------------------------------------------------------------------------
%build
%py2_build
%py3_build

#------------------------------------------------------------------------------
%install
%py2_install
%py3_install

#------------------------------------------------------------------------------
%files -n python2-evdev
%license LICENSE
%doc README.rst
%{python2_sitearch}/evdev/
%{python2_sitearch}/evdev-%{version}-py%{python2_version}.egg-info/

%files -n python3-evdev
%license LICENSE
%doc README.rst
%{python3_sitearch}/evdev/
%{python3_sitearch}/evdev-%{version}-py%{python3_version}.egg-info/


#------------------------------------------------------------------------------
%changelog
* Sun Jun 05 2016 Georgi Valkov <georgi.t.valkov@gmail.com> - 0.6.1-1
- Initial RPM Release
