#
%define		_ftpdir	/home/services/ftp
#
%bcond_with	clamav	#ClamAV scanning support

Summary:	vsftpd - Very Secure FTP Daemon
Summary(pl.UTF-8):	Bardzo Bezpieczny Demon FTP
Summary(pt_BR.UTF-8):	vsftpd - Daemon FTP Muito Seguro
Name:		vsftpd
Version:	2.1.1
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	ftp://vsftpd.beasts.org/users/cevans/%{name}-%{version}.tar.gz
# Source0-md5:	b1fab0e6212738f9f3572e067c419778
Source1:	%{name}.inetd
Source2:	%{name}.pamd
Source3:	%{name}-ftpusers
Source4:	ftpusers.tar.bz2
# Source4-md5:	76c80b6ec9f4d079a1e27316edddbe16
Source5:	%{name}.init
Patch0:		%{name}-builddefs.patch
Patch1:		%{name}-amd64-findlibs.patch
Patch2:		%{name}-clamav.patch
Patch3:		%{name}-include.patch
URL:		http://vsftpd.beasts.org/
BuildRequires:	libcap-devel
BuildRequires:	libwrap-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	%{name}-init = %{version}-%{release}
Requires:	filesystem >= 3.0-11
Requires:	pam >= 0.77.3
Provides:	ftpserver
Conflicts:	man-pages < 1.51
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Very Secure FTP Daemon - written from scratch - by Chris "One Man
Security Audit Team" Evans.

%description -l pl.UTF-8
Bardzo Bezpieczny Demon FTP - napisany od zera przez Chrisa "One Man
Security Audit Team" Evansa.

%description -l pt_BR.UTF-8
A Very Secure FTP Daemon (vsftpd) - escrito do zero - por Chris "One
Man Security Audit Team" Evans.

%package inetd
Summary:	vsftpd - Very Secure FTP Daemon
Summary(pl.UTF-8):	Bardzo Bezpieczny Demon FTP
Summary(pt_BR.UTF-8):	vsftpd - Daemon FTP Muito Seguro
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	rc-inetd
Provides:	%{name}-init = %{version}-%{release}
Obsoletes:	vsftpd-standalone
Conflicts:	%{name} <= 2.0.3-1

%description inetd
This package allows to start vsftpd as inetd service.

%description inetd -l pl.UTF-8
Ten pakiet pozwala na wystartowanie vsftpd jako usługi inetd.

%package standalone
Summary:	vsftpd - Very Secure FTP Daemon
Summary(pl.UTF-8):	Bardzo Bezpieczny Demon FTP
Summary(pt_BR.UTF-8):	vsftpd - Daemon FTP Muito Seguro
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts
Provides:	%{name}-init = %{version}-%{release}
Obsoletes:	vsftpd-inetd
Conflicts:	%{name} <= 2.0.3-1

%description standalone
This package allows to start vsftpd as standalone daemon.

%description standalone -l pl.UTF-8
Ten pakiet pozwala na wystartowanie vsftpd jako samodzielnego demona.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1
%if %{with clamav}
#%patch2 -p1 - needs update
%endif

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LINK="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT/etc/{pam.d,sysconfig/rc-inetd,logrotate.d,ftpd,rc.d/init.d} \
	$RPM_BUILD_ROOT{%{_ftpdir}/pub/incoming,/var/log}

install vsftpd $RPM_BUILD_ROOT%{_sbindir}/vsftpd
install vsftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd.conf
install vsftpd.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/vsftpd.conf.5
install vsftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/vsftpd.8
install RedHat/vsftpd.log $RPM_BUILD_ROOT/etc/logrotate.d/vsftpd

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/vsftpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/ftp
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/ftpd/ftpusers
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/vsftpd

> $RPM_BUILD_ROOT/var/log/vsftpd.log

bzip2 -dc %{SOURCE4} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
rm -f $RPM_BUILD_ROOT/usr/share/man/ftpusers-path.diff

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/log/vsftpd.log
chmod 640 /var/log/vsftpd.log

%post inetd
%service -q rc-inetd reload

%postun inetd
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
fi

%post standalone
/sbin/chkconfig --add %{name}
%service vsftpd restart "vsftpd server"

%preun standalone
if [ "$1" = "0" ]; then
	%service vsftpd stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUDIT BENCHMARKS BUGS Changelog FAQ README README.ssl REWARD SIZE SPEED TODO TUNING EXAMPLE SECURITY
%attr(755,root,root) %{_sbindir}/vsftpd
%dir %attr(750,root,ftp) %dir %{_sysconfdir}/ftpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vsftpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/ftpusers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/ftp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/vsftpd
%attr(640,root,root) %ghost /var/log/vsftpd.log
%{_mandir}/man5/vsftpd.conf.5*
%{_mandir}/man8/vsftpd.8*
%{_mandir}/man5/ftpusers.5*
%lang(ja) %{_mandir}/ja/man5/ftpusers*
%lang(pl) %{_mandir}/pl/man5/ftpusers*
%lang(pt_BR) %{_mandir}/pt_BR/man5/ftpusers*
%lang(ru) %{_mandir}/ru/man5/ftpusers*
%dir %{_ftpdir}
%dir %{_ftpdir}/pub
# it's safe - by default anon_upload_enable=NO, anon_world_readable_only=YES
%attr(775,root,ftp) %dir %{_ftpdir}/pub/incoming

%files inetd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/vsftpd

%files standalone
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vsftpd
