%global __os_install_post %{_rpmconfigdir}/brp-compress

%global debug_package %{nil}
%global provider github
%global provider_tld com
%global project coreos
%global repo rocket

%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit 9d66f8c679599afec6cec543cb1f2455d3c2fb8e
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name: %{repo}
Version: 0.5.1
Release: 2.git%{shortcommit}%{?dist}
Summary: CLI for running app containers
License: ASL 2.0
URL: https://%{import_path}
ExclusiveArch: x86_64
Source0: https://github.com/lsm5/rocket/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1: README.adoc
Source2: %{repo}-metadata.service
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
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


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
# create install dirs
install -dp %{buildroot}{%{_bindir},%{_libexecdir}/rocket/stage1,%{_unitdir}}

# install rkt binary
install -p -m 755 bin/rkt %{buildroot}%{_bindir}

# Install metadata unitfile
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}

%pre
getent group %{name} > /dev/null || %{_sbindir}/groupadd -r %{name}
exit 0

%post
%systemd_post %{repo}-metadata

%preun
%systemd_preun %{repo}-metadata

%postun
%systemd_postun_with_restart %{repo}-metadata


%files
%doc CONTRIBUTING.md DCO LICENSE NOTICE README.md
%doc Documentation/getting-started-guide.md Documentation/hacking.md
%{_bindir}/rkt
%{_unitdir}/%{repo}-metadata.service

%changelog
* Sat Mar 28 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.1-2.git9d66f8c
- use github.com/lsm5/rocket branch systemd-vendored which includes a checked
out systemd v215 tree instead of git cloning it
- should allow building the rpm in a mock/koji environment

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
