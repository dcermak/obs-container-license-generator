#
# spec file for package containers-licenses
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           container-license-generator
Version:        0.1
Release:        0
Summary:        Service for inserting the licenses into a container label
License:        GPL-3.0-or-later
URL:            https://github.com/dcermak/obs-%{name}
Source0:        %{name}
Requires:       /usr/bin/sed
Requires:       /usr/bin/awk
Requires:       /bin/bash
Requires:       findutils
Requires:       jq
Requires:       skopeo
BuildArch:      noarch

%description
This service can be used during buildtime to extract the licenses from OBS
.packages file and inserts them into the org.opencontainers.image.licenses label

%prep
%setup -q -D -T -n .
# cp %%{SOURCE2} .

%build

%install
mkdir -p %{buildroot}%{_prefix}/lib/build/post-build-checks/
install -m 0755 %{SOURCE0} %{buildroot}%{_prefix}/lib/build/post-build-checks/

%files
%dir %{_prefix}/lib/build/post-build-checks/
%{_prefix}/lib/build/post-build-checks/%{name}

%changelog
