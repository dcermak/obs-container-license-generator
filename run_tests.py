#!/usr/bin/env python3

from dataclasses import dataclass, field
from tempfile import TemporaryDirectory
from typing import Dict, Optional, Tuple, Union
import os.path
from pathlib import Path
from shutil import copy
from subprocess import PIPE, check_output
import json
import shlex


CONTAINER_LICENSE_GENERATOR_BINARY = (
    Path(os.path.abspath(os.path.dirname(__file__))) / "container-license-generator"
)

TUMBLEWEED_BUSYBOX_DOT_PACKAGES = """
busybox-adduser|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-attr|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-bc|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-bind-utils|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-bzip2|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-coreutils|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-cpio|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-diffutils|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-dos2unix|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-ed|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-findutils|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-gawk|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-grep|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-gzip|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-hostname|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-iproute2|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-iputils|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-kbd|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-kmod|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-less|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-man|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-misc|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-ncurses-utils|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-net-tools|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-netcat|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-patch|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-policycoreutils|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-procps|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-psmisc|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-sed|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-selinux-tools|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-sendmail|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-sharutils|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-sh|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-syslogd|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-sysvinit-tools|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-tar|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-telnet|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-tftp|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-time|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-traceroute|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-tunctl|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-unzip|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-util-linux|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-vi|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-vlan|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-wget|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-which|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-whois|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox-xz|(none)|1.34.1|19.6|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/6821beec79e980978d3097e149416c90-busybox-links|GPL-2.0-or-later
busybox|(none)|1.34.1|2.1|i586|obs://build.opensuse.org/openSUSE:Factory/standard/c951706ba97fac7f6a7cd70c7233ece9-busybox|GPL-2.0-or-later
compat-usrmerge-tools|(none)|84.87|5.1|i586|obs://build.opensuse.org/openSUSE:Factory/standard/db3ea9074a430717229ef191e990fb4f-compat-usrmerge|MIT
filesystem|(none)|84.87|3.1|i586|obs://build.opensuse.org/openSUSE:Factory/standard/e19f9a2dee97535e8ce230e11e280caf-filesystem|MIT
glibc|(none)|2.34|3.1|i586|obs://build.opensuse.org/openSUSE:Factory/standard/4322ca9caec769677b03c75cf5741007-glibc|GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0
kubernetes-pause|(none)|3.2|1.9|i586|obs://build.opensuse.org/openSUSE:Factory/standard/e1df8d2d38d00f0cf7f64791957f62f2-kubernetes-pause|Apache-2.0
libcrypt1|(none)|4.4.25|1.2|i586|obs://build.opensuse.org/openSUSE:Factory/standard/50e794c54149624b76860d49261c06dd-libxcrypt|BSD-2-Clause AND LGPL-2.1-or-later AND BSD-3-Clause AND SUSE-Public-Domain
libpcre2-8-0|(none)|10.39|1.1|i586|obs://build.opensuse.org/openSUSE:Factory/standard/73b7b1b96bef5f5971492e9cfe3cca65-pcre2|BSD-3-Clause
libselinux1|(none)|3.3|1.1|i586|obs://build.opensuse.org/openSUSE:Factory/standard/4507004e11d82a063e2ad09c6018dc1e-libselinux|SUSE-Public-Domain
libsepol2|(none)|3.3|1.1|i586|obs://build.opensuse.org/openSUSE:Factory/standard/ef4e157bc538eeb0e1630a17d404653f-libsepol|LGPL-2.1-or-later
system-user-nobody|(none)|20170617|24.1|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/87094dcba229da2ac37639b84cbcce97-system-users|MIT
system-user-root|(none)|20190513|1.36|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/338740bedeaffdf9b2e6891ad9924dd1-system-user-root|MIT
sysuser-shadow|(none)|3.1|3.2|noarch|obs://build.opensuse.org/openSUSE:Factory/standard/94e7b7d8b752fdf828ecc22950ed3a61-sysuser-tools|MIT
update-alternatives|(none)|1.20.9|1.2|i586|obs://build.opensuse.org/openSUSE:Factory/standard/2a67fffb1fe5f6d3427658a5ab7f6d50-update-alternatives|GPL-2.0-or-later
gpg-pubkey|(none)|307e3d54|5aaa90a5|(none)|(none)|pubkey
gpg-pubkey|(none)|39db7c82|5f68629b|(none)|(none)|pubkey
"""


def run_cmd(cmd: str, cwd: Optional[Union[str, Path]] = None) -> str:
    return check_output(shlex.split(cmd), cwd=cwd, stderr=PIPE).decode().strip()


@dataclass
class ContainerTest:
    container_archive: Path
    files: Dict[str, Union[str, Path]] = field(default_factory=dict)
    expected_licenses: str = ""

    _tempdir: Optional[TemporaryDirectory] = None

    def __post_init__(self):
        assert self._tempdir is None
        self._tempdir = TemporaryDirectory()

        tmp = Path(self._tempdir.name)
        for path, contents in self.files.items():
            dest = tmp / Path(path)
            (tmp / Path(os.path.dirname(path))).mkdir(parents=True, exist_ok=True)
            if isinstance(contents, str):
                with open(dest, "w") as f:
                    f.write(contents)
            else:
                copy(contents, dest)

    def run_test(self):
        assert self._tempdir is not None
        check_output(CONTAINER_LICENSE_GENERATOR_BINARY, cwd=self._tempdir.name)

        metadata = json.loads(
            run_cmd(
                f"skopeo inspect docker-archive:{str(Path(self._tempdir.name) / self.container_archive)}",
            )
        )

        licenses = metadata["Labels"]["org.opencontainers.image.licenses"]

        assert (
            "pubkey" not in licenses
        ), f"unexpected license 'pubkey' in in '{licenses}'"
        assert (
            licenses == self.expected_licenses
        ), f"""expected the following licenses:
{self.expected_licenses}
but got:
{licenses}
"""

    def cleanup(self):
        assert self._tempdir is not None
        self._tempdir.cleanup()


def prepare_container_archives(tempdir: str) -> Tuple[Path, Path, Path]:
    dockerfile_path = Path(tempdir) / "Dockerfile"
    busybox_tar = Path(tempdir) / "busybox.tar"
    busybox_with_single_label_tar = Path(tempdir) / "busybox_with_single_label.tar"
    busybox_with_multiple_labels_tar = (
        Path(tempdir) / "busybox_with_multiple_labels.tar"
    )

    run_cmd("podman pull registry.opensuse.org/opensuse/busybox:latest", tempdir)
    run_cmd(
        f"skopeo copy containers-storage:registry.opensuse.org/opensuse/busybox:latest docker-archive:/{busybox_tar}",
        tempdir,
    )

    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(
            """FROM registry.opensuse.org/opensuse/busybox:latest

LABEL org.opencontainers.image.licenses "CC-BY-NC-4.0"
"""
        )
    run_cmd(
        f"buildah bud --layers -t busybox_label_test -f {dockerfile_path}",
        tempdir,
    )
    run_cmd(
        f"skopeo copy containers-storage:localhost/busybox_label_test docker-archive:/{busybox_with_single_label_tar}",
        tempdir,
    )
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(
            """FROM registry.opensuse.org/opensuse/busybox:latest

LABEL org.opencontainers.image.licenses "CC-BY-NC-4.0 AND GPL-2.0-or-later"
"""
        )
    run_cmd(
        f"buildah bud --layers -t busybox_multiple_labels_test -f {dockerfile_path}",
        tempdir,
    )
    run_cmd(
        f"skopeo copy containers-storage:localhost/busybox_multiple_labels_test docker-archive:/{busybox_with_multiple_labels_tar}",
        tempdir,
    )

    return busybox_tar, busybox_with_single_label_tar, busybox_with_multiple_labels_tar


if __name__ == "__main__":

    with TemporaryDirectory() as tmp:
        (
            busybox_tar,
            busybox_with_single_labels_tar,
            busybox_with_multiple_labels_tar,
        ) = prepare_container_archives(tmp)

        without_labels = ContainerTest(
            files={
                "KIWI/tumbleweed.packages": TUMBLEWEED_BUSYBOX_DOT_PACKAGES,
                "KIWI/busybox.tar": busybox_tar,
                "KIWI-docker/busybox.tar.sha256": "",
                "KIWI/busybox.tar.sha256": "",
            },
            container_archive=Path("KIWI/busybox.tar"),
            expected_licenses="Apache-2.0 AND (BSD-2-Clause AND LGPL-2.1-or-later AND BSD-3-Clause AND SUSE-Public-Domain) AND BSD-3-Clause AND GPL-2.0-or-later AND (GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0) AND LGPL-2.1-or-later AND MIT AND SUSE-Public-Domain",
        )
        with_labels = ContainerTest(
            files={
                "DOCKER/tumbleweed.packages": TUMBLEWEED_BUSYBOX_DOT_PACKAGES,
                "DOCKER/busybox.tar": busybox_with_single_labels_tar,
                "DOCKER/busybox.tar.sha256": "",
                "DOCKER/busybox.basepackages": "",
            },
            container_archive=Path("DOCKER/busybox.tar"),
            expected_licenses="CC-BY-NC-4.0",
        )
        take_labels_from_base = ContainerTest(
            files={
                "DOCKER/tumbleweed.packages": TUMBLEWEED_BUSYBOX_DOT_PACKAGES,
                "DOCKER/busybox.tar": busybox_with_single_labels_tar,
                "SOURCES/container-license-generator.json": """
{"inheritLabel": true}
""",
            },
            expected_licenses="Apache-2.0 AND (BSD-2-Clause AND LGPL-2.1-or-later AND BSD-3-Clause AND SUSE-Public-Domain) AND BSD-3-Clause AND GPL-2.0-or-later AND (GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0) AND LGPL-2.1-or-later AND MIT AND SUSE-Public-Domain AND CC-BY-NC-4.0",
            container_archive=Path("DOCKER/busybox.tar"),
        )
        take_labels_from_base_multiple = ContainerTest(
            files={
                "DOCKER/tumbleweed.packages": TUMBLEWEED_BUSYBOX_DOT_PACKAGES,
                "DOCKER/busybox.tar": busybox_with_multiple_labels_tar,
                "SOURCES/container-license-generator.json": """
{"inheritLabel": true}
""",
            },
            expected_licenses="Apache-2.0 AND (BSD-2-Clause AND LGPL-2.1-or-later AND BSD-3-Clause AND SUSE-Public-Domain) AND BSD-3-Clause AND GPL-2.0-or-later AND (GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0) AND LGPL-2.1-or-later AND MIT AND SUSE-Public-Domain AND (CC-BY-NC-4.0 AND GPL-2.0-or-later)",
            container_archive=Path("DOCKER/busybox.tar"),
        )

        all_tests = [
            with_labels,
            without_labels,
            take_labels_from_base,
            take_labels_from_base_multiple,
        ]

        try:
            for test in all_tests:
                test.run_test()
        finally:
            for test in all_tests:
                test.cleanup()
