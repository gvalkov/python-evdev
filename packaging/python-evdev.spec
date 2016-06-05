%global gittag0 v0.6.1
%global _summary Python bindings for the Linux input handling subsystem

Name:           python-evdev
Version:        0.6.1
Release:        1%{?dist}
Summary:        %{_summary}

License:        BSD
URL:            https://python-evdev.readthedocs.io
Source0:        https://github.com/gvalkov/%{name}/archive/%{gittag0}.tar.gz#/%{name}-%{version}.tar.gz
Group:          Development/Libraries

BuildRequires:  kernel-headers python3-devel python3-setuptools
BuildRequires:  python2-devel python-setuptools

%description
This package provides bindings to the Linux generic input event interface.


%package -n python2-evdev
Summary:        %{_summary}
Group:          Development/Libraries
%{?python_provide:%python_provide python2-evdev}

%description -n python2-evdev

This package provides bindings to the generic input event interface in Linux.
The evdev interface serves the purpose of passing events generated in the kernel
directly to userspace through character devices that are typically located in
/dev/input/.

This package also comes with bindings to uinput, the userspace input subsystem.
Uinput allows userspace programs to create and handle input devices that can
inject events directly into the input subsystem.

In other words, python-evdev allows you to read and write input events on Linux.
An event can be a key or button press, a mouse movement or a tap on a
touchscreen.


%package -n python3-evdev
Summary:        %{_summary}
Group:          Development/Libraries
%{?python_provide:%python_provide python3-evdev}

%description -n python3-evdev
This package provides bindings to the generic input event interface in Linux.
The evdev interface serves the purpose of passing events generated in the kernel
directly to userspace through character devices that are typically located in
/dev/input/.

This package also comes with bindings to uinput, the userspace input subsystem.
Uinput allows userspace programs to create and handle input devices that can
inject events directly into the input subsystem.

In other words, python-evdev allows you to read and write input events on Linux.
An event can be a key or button press, a mouse movement or a tap on a
touchscreen.


#------------------------------------------------------------------------------
%prep
%autosetup -n %{name}-%{version}

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
%{python2_sitearch}/*

%files -n python3-evdev
%license LICENSE
%doc README.rst
%{python3_sitearch}/*


#------------------------------------------------------------------------------
%changelog
* Sun Jun 05 2016 Georgi Valkov <georgi.t.valkov@gmail.com> - 0.6.1-1
- Initial RPM Release
