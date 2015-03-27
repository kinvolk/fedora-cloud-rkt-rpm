%global __os_install_post %{_rpmconfigdir}/brp-compress

%global debug_package %{nil}
%global provider github
%global provider_tld com
%global project coreos
%global repo rocket

%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit 58bd354961a54c841c9b0ea7a5cea5716e74c29a 
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name: %{repo}
Version: 0.5.1
Release: 1.git%{shortcommit}%{?dist}
Summary: CLI for running app containers
License: ASL 2.0
URL: https://%{import_path}
ExclusiveArch: x86_64
Source0: https://%{import_path}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
BuildRequires: glibc-static
BuildRequires: golang >= 1.3.3
BuildRequires: go-bindata >= 3.0.7-1
BuildRequires: squashfs-tools
BuildRequires: golang(github.com/appc/spec/schema/types)
BuildRequires: libgcrypt-devel
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: gperf
BuildRequires: libcap-devel

%description
%{summary}

%prep
%setup -qn %{name}-%{commit}

%build
# using RKT_STAGE1_USR_FROM=src doesn't fetch coreos pxe image
# but builds systemd from source
# TODO: eliminate the build process perhaps and fetch systemd stuff from rpms
GOPATH=$GOPATH:%{gopath}:$(pwd)/Godeps/_workspace RKT_STAGE1_USR_FROM=src ./build

%install
# install binaries
install -dp %{buildroot}{%{_bindir},%{_libexecdir}/rocket/stage1}
install -p -m 755 bin/rkt %{buildroot}%{_bindir}

%pre
getent group %{name} > /dev/null || %{_sbindir}/groupadd -r %{name}

%files
%doc CONTRIBUTING.md DCO LICENSE NOTICE README.md
%doc Documentation/getting-started-guide.md Documentation/hacking.md
%{_bindir}/rkt

%changelog
* Fri Mar 27 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.1-1.git58bd354
- update to latest upstream master

* Mon Feb 02 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.2.0-1.git29d53af
- use latest master commit
- mkrootfs uses fedora docker base image from koji
via Václav Pavlin <vpavlin@redhat.com>

* Tue Dec 02 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1.0-1.git553023e
- Initial package
- install init in libexec/rocket/stage1
https://github.com/coreos/rocket/issues/173
thanks Jonathan Boulle <https://github.com/jonboulle> 
and Tom Prince <tom.prince@ualberta.net>
