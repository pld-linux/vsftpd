Summary:	vsftpd - Very Secure FTP Daemon
Summary(pl):	Bardzo Bezpieczny Demon FTP
Name:		vsftpd
Version:	1.0.1
Release:	2
License:	GPL v2
Group:		Daemons
Source0:	ftp://ferret.lmh.ox.ac.uk/pub/linux/vsftpd/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.pamd
Source3:	%{name}-ftpusers
URL:		http://vsftpd.beasts.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
PreReq:		rc-inetd
Provides:	ftpserver
Obsoletes:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	muddleftpd
Obsoletes:	proftpd
Obsoletes:	proftpd-common
Obsoletes:	proftpd-inetd
Obsoletes:	proftpd-standalone
Obsoletes:	pure-ftpd
Obsoletes:	troll-ftpd
Obsoletes:	wu-ftpd

%description
A Very Secure FTP Daemon - written from scratch - by Chris "One Man
Security Audit Team" Evans.

%description -l pl
Bardzo Bezpieczny Demon FTP - napisany od zera przez Chrisa "One Man
Security Audit Team" Evansa.

%prep
%setup -q -n %{name}-%{version}

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LINK="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_datadir}/empty,%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT/etc/{pam.d,sysconfig/rc-inetd,logrotate.d,ftpd} \
	$RPM_BUILD_ROOT{/home/ftp/pub/Incoming,/var/log}

install vsftpd $RPM_BUILD_ROOT%{_sbindir}/vsftpd
install vsftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd.conf
install vsftpd.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5/vsftpd.conf.5
install vsftpd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/vsftpd.8
install RedHat/vsftpd.log $RPM_BUILD_ROOT/etc/logrotate.d/vsftpd

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/vsftpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/ftp
install %{SOURCE3} $RPM_BUILD_ROOT/etc/ftpd/ftpusers

> $RPM_BUILD_ROOT/var/log/vsftpd.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/log/vsftpd.log
chmod 640 /var/log/vsftpd.log
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%files
%defattr(644,root,root,755)
%doc AUDIT BENCHMARKS BUGS Changelog FAQ README REWARD SIZE SPEED TODO TUNING
%doc SECURITY
%attr(755,root,root) %{_sbindir}/vsftpd
%dir %{_datadir}/empty
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/vsftpd.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/ftpd/ftpusers
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/vsftpd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/ftp
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/vsftpd
%attr(640,root,root) %ghost /var/log/vsftpd.log
%{_mandir}/man5/vsftpd.conf.5*
%{_mandir}/man8/vsftpd.8*
%dir /home/ftp
%dir /home/ftp/pub
# it's safe - by default anon_upload_enable=NO, anon_world_readable_only=YES
%attr(775,root,ftp) %dir /home/ftp/pub/Incoming
