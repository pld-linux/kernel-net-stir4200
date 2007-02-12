
%bcond_without	dist_kernel	# Don't use the distribution's kernel
%bcond_without	smp		# Don't build the SMP module

%define _orig_name	stir4200
Summary:	SigmaTel USB-IrDA dongle driver
Summary(es.UTF-8):   Controlador del puente USB-IrDA de SigmaTel
Summary(pl.UTF-8):   Sterownik pomostu USB-IrDA SigmaTel
Name:		kernel-net-%{_orig_name}
# To find out: grep Version: *.h
Version:	0.1b
%define	_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://wetlogic.net/stewart/%{_orig_name}/%{_orig_name}.tgz
# Source0-md5:	422157c08a7dc703fbb6858019ed78d0
URL:		http://sourceforge.net/projects/sigma-irda/
BuildRequires:	%{kgcc_package}
%if %{with dist_kernel}
BuildRequires:	kernel-headers
%requires_releq_kernel_up
%endif
Requires(post,postun):	/sbin/depmod
Provides:	kernel(%{_orig_name})
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SigmaTel has released a chip for USB IrDA adapters that fails to
comply with the "Universal Serial Bus IrDA Bridge Device Definition".
Install this package if, despite of that, you want to make use of
devices based on the chip.

%description -l es.UTF-8
SigmaTel ha creado un chip para adaptadored de IrDA en USB que ignora
el estándar "Universal Serial Bus IrDA Bridge Device Definition".
Instale este paquete si, a pesar de ello, quiere sacar provecho de
dispositivos basados en ese chip.

%description -l pl.UTF-8
SigmaTel wypuścił chip dla adapterów IrDA na USB, który łamie zasady
określone w standardzie "Universal Serial Bus IrDA Bridge Device
Definition". Zainstaluj ten pakiet jeśli mimo wszystko chcesz
korzystać z opartych na nim urządzeń.

%package -n kernel-smp-net-%{_orig_name}
Summary:	SigmaTel USB-IrDA dongle driver
Summary(es.UTF-8):   Controlador del puente USB-IrDA de SigmaTel
Summary(pl.UTF-8):   Sterownik pomostu USB-IrDA SigmaTel
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Provides:	kernel(%{_orig_name})

%description -n kernel-smp-net-%{_orig_name}
SigmaTel has released a chip for USB IrDA adapters that fails to
comply with the "Universal Serial Bus IrDA Bridge Device Definition".
Install this package if, despite of that, you want to make use of
devices based on the chip.

%description -n kernel-smp-net-%{_orig_name} -l es.UTF-8
SigmaTel ha creado un chip para adaptadored de IrDA en USB que ignora
el estándar "Universal Serial Bus IrDA Bridge Device Definition".
Instale este paquete si, a pesar de ello, quiere sacar provecho de
dispositivos basados en ese chip.

%description -n kernel-smp-net-%{_orig_name} -l pl.UTF-8
SigmaTel wypuścił chip dla adapterów IrDA na USB, który łamie zasady
określone w standardzie "Universal Serial Bus IrDA Bridge Device
Definition". Zainstaluj ten pakiet jeśli mimo wszystko chcesz
korzystać z opartych na nim urządzeń.

%prep
%setup -q -c -T -a0

%build
CFLAGS="-D__KERNEL__ -DMODULE %{rpmcflags} -fomit-frame-pointer -pipe"
CFLAGS="$CFLAGS -Wall -I%{_kernelsrcdir}/include"

# SMP build
%if %{with smp}
%{__make} CFLAGS="$CFLAGS -D__SMP__ -D__KERNEL_SMP=1"
mv -f stir4200.o stir4200-smp.o
%endif

# UP build
%{__make} CFLAGS="$CFLAGS"

%install
rm -rf $RPM_BUILD_ROOT

# SMP install
%if %{with smp}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install %{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o
%endif

# UP install
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install %{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-%{_orig_name}
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-%{_orig_name}
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%if %{with smp}
%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
%endif
