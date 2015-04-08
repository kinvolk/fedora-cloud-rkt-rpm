%global __os_install_post %{_rpmconfigdir}/brp-compress

%global debug_package %{nil}
%global provider github
%global provider_tld com
%global project coreos
%global repo rkt

%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit 96d0cc03f28c63440ea2f1d7b3e145e0b7333d0b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name: %{repo}
Version: 0.5.3
Release: 12.git%{shortcommit}%{?dist}
Summary: CLI for running app containers
License: ASL 2.0
URL: https://%{import_path}
ExclusiveArch: x86_64
Source0: https://%{import_path}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1: README.adoc
BuildRequires: glibc-static
BuildRequires: golang >= 1.3.3
BuildRequires: go-bindata >= 3.0.7-1
BuildRequires: squashfs-tools
BuildRequires: golang(github.com/appc/spec/schema/types)
BuildRequires: systemd
BuildRequires: git
BuildRequires: libgcrypt-devel
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: gperf
BuildRequires: libcap-devel
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
%{summary}

%prep
%setup -qn %{repo}-%{commit}

%build
# some issues in here prevent fedora approval
# using COPR until then
GOPATH=$GOPATH:%{gopath}:$(pwd)/Godeps/_workspace:$(pwd)/_build \
       RKT_STAGE1_USR_FROM=src ./build

%install
# create install dirs
install -dp %{buildroot}{%{_bindir},%{_libexecdir}/%{repo},%{_unitdir}}

# install rkt binary
install -p -m 755 bin/%{repo} %{buildroot}%{_bindir}

# install stage1.aci
install -p -m 644 bin/stage1.aci %{buildroot}%{_libexecdir}/%{repo}

# install metadata unitfiles
install -p -m 644 dist/init/systemd/%{repo}-metadata.service %{buildroot}%{_unitdir}
install -p -m 644 dist/init/systemd/%{repo}-metadata.socket %{buildroot}%{_unitdir}

%pre
getent group %{repo} > /dev/null || %{_sbindir}/groupadd -r %{repo}
exit 0

%post
%systemd_post %{repo}-metadata

%preun
%systemd_preun %{repo}-metadata

%postun
%systemd_postun_with_restart %{repo}-metadata

%files
%doc CONTRIBUTING.md DCO LICENSE MAINTAINERS NOTICE README.md Documentation/*
%{_bindir}/%{repo}
%{_libexecdir}/%{repo}/*
%{_unitdir}/%{repo}-metadata.s*

%changelog
* Wed Apr 08 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-12.git96d0cc0
- built rkt commit#96d0cc0

* Tue Apr 07 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-11.gitfd44be4
- built rkt commit#fd44be4

* Sun Apr 05 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-10.gitb9bfa72
- built rkt commit#b9bfa72

* Sat Apr 04 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-9.gitb9bfa72
- built rkt commit#b9bfa72

* Fri Apr 03 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-8.gitae78000
- built rkt commit#ae78000

* Fri Apr 03 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-7.gitae78000
- built rkt commit#ae78000

* Fri Apr 03 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-6.gitae78000
- built rkt commit#ae78000

* Fri Apr 03 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-5.gitae78000
- built rkt commit#ae78000

* Fri Apr 03 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-4.gitae78000
- built rkt commit#ae78000

* Fri Apr 03 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-3.gitae78000
- built rkt commit#ae78000

* Thu Apr 02 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-2.gita72ad99
- install stage1.aci and metadata socket file

* Thu Apr 02 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-1.gita72ad99
- update to 0.5.3+git

* Sat Mar 28 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.1-2.git9d66f8c
- use github.com/lsm5/rkt branch systemd-vendored which includes a checked
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
- install init in libexec/rkt/stage1
https://github.com/coreos/rkt/issues/173
thanks Jonathan Boulle <jonathan.boulle@coreos.com>
and Tom Prince <tom.prince@ualberta.net>
