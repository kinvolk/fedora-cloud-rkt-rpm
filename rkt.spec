%global debug_package %{nil}
%global provider github
%global provider_tld com
%global project coreos
%global repo rkt

%global git0 https://%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit0 7575500011a56584755be5e9978c8cfef4aff433
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global version 0.15.0

# valid values: coreos usr-from-src usr-from-host
%global stage1_flavors host

Name:       %{repo}
Version:    %{version}
Release:    2.git%{shortcommit0}%{?dist}
Summary:    CLI for running app containers
License:    ASL 2.0
URL:        https://%{import_path}
ExclusiveArch:  x86_64
Source0:    %{git0}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bc
BuildRequires: git
BuildRequires: glibc-static
BuildRequires: golang >= 1.3.3
BuildRequires: go-bindata >= 3.0.7-1
BuildRequires: golang(github.com/appc/spec/schema/types)
BuildRequires: gperf
BuildRequires: gnupg
BuildRequires: intltool
BuildRequires: libacl-devel
BuildRequires: libcap-devel
BuildRequires: libgcrypt-devel
BuildRequires: libtool
BuildRequires: libmount-devel
BuildRequires: libxkbcommon-devel
BuildRequires: perl-Config-Tiny
BuildRequires: squashfs-tools
BuildRequires: systemd >= 222

Requires(pre): shadow-utils
Requires(post): systemd >= 222
Requires(preun): systemd >= 222
Requires(postun): systemd >= 222

%description
%{summary}

%prep
%setup -qn %{name}-%{commit0}

%build
./autogen.sh
# ./configure flags: https://github.com/coreos/rkt/blob/master/Documentation/build-configure.md
./configure --with-stage1-flavors=%{stage1_flavors} \
            --with-stage1-flavors-version-override=%{version}-%{release} \
            --with-stage1-default-location=%{_libexecdir}/%{name}/stage1-host.aci
make all

%install
# install binaries
install -dp %{buildroot}{%{_bindir},%{_libexecdir}/%{name},%{_unitdir}}

install -p -m 755 build-%{name}-%{version}+git/bin/%{name} %{buildroot}%{_bindir}
install -p -m 644 build-%{name}-%{version}+git/bin/stage1-host.aci %{buildroot}%{_libexecdir}/%{name}

# install metadata unitfiles
install -p -m 644 dist/init/systemd/%{name}-gc.timer %{buildroot}%{_unitdir}
install -p -m 644 dist/init/systemd/%{name}-gc.service %{buildroot}%{_unitdir}
install -p -m 644 dist/init/systemd/%{name}-metadata.socket %{buildroot}%{_unitdir}
install -p -m 644 dist/init/systemd/%{name}-metadata.service %{buildroot}%{_unitdir}

# Install runtime directories
# https://github.com/coreos/rkt/blob/master/Documentation/packaging.md#ownership-and-permissions-of-rkt-directories
install -dp -m 770 %{buildroot}%{_sharedstatedir}/%{name}
install -dp -m 770 %{buildroot}%{_sharedstatedir}/%{name}/cas
install -dp -m 770 %{buildroot}%{_sharedstatedir}/%{name}/cas/db
install -dp -m 770 %{buildroot}%{_sharedstatedir}/%{name}/cas/imagelocks
install -dp -m 770 %{buildroot}%{_sharedstatedir}/%{name}/cas/imageManifest
install -dp -m 770 %{buildroot}%{_sharedstatedir}/%{name}/cas/blob
install -dp -m 770 %{buildroot}%{_sharedstatedir}/%{name}/cas/tmp
install -dp -m 750 %{buildroot}%{_sharedstatedir}/%{name}/cas/tree
install -dp -m 750 %{buildroot}%{_sharedstatedir}/%{name}/cas/treestorelocks
install -dp -m 770 %{buildroot}%{_sharedstatedir}/%{name}/locks

install -dp -m 750 %{buildroot}%{_sharedstatedir}/%{name}/pods
install -dp -m 750 %{buildroot}%{_sharedstatedir}/%{name}/pods/embryo
install -dp -m 750 %{buildroot}%{_sharedstatedir}/%{name}/pods/prepare
install -dp -m 750 %{buildroot}%{_sharedstatedir}/%{name}/pods/prepared
install -dp -m 750 %{buildroot}%{_sharedstatedir}/%{name}/pods/run
install -dp -m 750 %{buildroot}%{_sharedstatedir}/%{name}/pods/exited-garbage
install -dp -m 750 %{buildroot}%{_sharedstatedir}/%{name}/pods/garbage

%pre

getent group rkt >/dev/null || groupadd -r rkt
exit 0

%post
%systemd_post %{name}-metadata

%preun
%systemd_preun %{name}-metadata

%postun
%systemd_postun_with_restart %{name}-metadata

%files
%doc CONTRIBUTING.md DCO LICENSE README.md Documentation/*

%{_bindir}/%{name}
%{_libexecdir}/%{name}/stage1-host.aci

%{_unitdir}/%{name}-gc.timer
%{_unitdir}/%{name}-gc.service
%{_unitdir}/%{name}-metadata.socket
%{_unitdir}/%{name}-metadata.service

%attr(2770, root, rkt) %{_sharedstatedir}/%{name}
%attr(2770, root, rkt) %{_sharedstatedir}/%{name}/cas
%attr(2770, root, rkt) %{_sharedstatedir}/%{name}/cas/db
%attr(2770, root, rkt) %{_sharedstatedir}/%{name}/cas/imagelocks
%attr(2770, root, rkt) %{_sharedstatedir}/%{name}/cas/imageManifest
%attr(2770, root, rkt) %{_sharedstatedir}/%{name}/cas/blob
%attr(2770, root, rkt) %{_sharedstatedir}/%{name}/cas/tmp
%attr(2750, root, rkt) %{_sharedstatedir}/%{name}/cas/tree
%attr(2750, root, rkt) %{_sharedstatedir}/%{name}/cas/treestorelocks
%attr(2770, root, rkt) %{_sharedstatedir}/%{name}/locks

%attr(2750, root, rkt) %{_sharedstatedir}/%{name}/pods
%attr(2750, root, rkt) %{_sharedstatedir}/%{name}/pods/embryo
%attr(2750, root, rkt) %{_sharedstatedir}/%{name}/pods/prepare
%attr(2750, root, rkt) %{_sharedstatedir}/%{name}/pods/prepared
%attr(2750, root, rkt) %{_sharedstatedir}/%{name}/pods/run
%attr(2750, root, rkt) %{_sharedstatedir}/%{name}/pods/exited-garbage
%attr(2750, root, rkt) %{_sharedstatedir}/%{name}/pods/garbage

%changelog
* Sun Jan 10 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.15.0-2.git7575500
- built commit#7575500

* Mon Aug 03 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.0-3.git6dae5d5
- built rkt commit#6dae5d5

* Mon Aug 03 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.0-2.git6dae5d5
- built rkt commit#6dae5d5

* Sun Jul 19 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.0-1
- New version: 0.7.0, built rkt         commit#c5e8cd5

* Wed Jun 17 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.6.1-1
- New version: 0.6.1, built rkt         commit#30cb88c

* Wed Jun 10 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.6-5.git06bf23b
- built rkt commit#06bf23b

* Sun Jun 07 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.6-4.git7bf926e
- built rkt commit#7bf926e

* Tue Jun 02 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.6-3.git25b862d
- built rkt commit#25b862d

* Fri May 29 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.6-2.gited97885
- built rkt commit#ed97885

* Thu May 28 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.6-1
- New version: 0.5.6, built rkt         commit#139af2b

* Wed May 27 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.5-7.git5e95eac
- built rkt commit#5e95eac

* Sun May 24 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.5-6.gite5be761
- built rkt commit#e5be761

* Mon May 11 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.5-5.git724e49e
- built rkt commit#724e49e

* Mon May 11 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.5-4.git724e49e
- built rkt commit#724e49e

* Fri May 08 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.5-3.gitd61a4c5
- built rkt commit#d61a4c5

* Mon May 04 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.5-2.gitb1190d9
- built rkt commit#b1190d9

* Mon May 04 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.5-1
- New version: 0.5.5, built rkt         commit#b1190d9

* Wed Apr 29 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.4-3.git40ecb47
- built rkt commit#40ecb47

* Wed Apr 29 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.4-2.git%{d_shortcommit}
- built rkt commit#40ecb47

* Thu Apr 23 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-16.gita506a39
- built rkt commit#a506a39

* Tue Apr 21 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-15.git73e6e1e
- built rkt commit#73e6e1e

* Mon Apr 13 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-14.git7bcbe3f
- built rkt commit#7bcbe3f

* Sun Apr 12 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-13.git7bcbe3f
- built rkt commit#7bcbe3f

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
