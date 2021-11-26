#!/bin/bash

set -e pipefail

function prepare() {
    pushd tests
    mkdir -p /tmp/test/KIWI{,-docker}/
    mkdir -p /tmp/test_with_label/DOCKER/
    buildah bud --layers -t busybox_label_test .

    podman pull registry.opensuse.org/opensuse/busybox:latest

    skopeo copy containers-storage:localhost/busybox_label_test docker-archive:/tmp/test_with_label/DOCKER/busybox_with_label.tar
    skopeo copy containers-storage:registry.opensuse.org/opensuse/busybox:latest docker-archive:/tmp/test/KIWI/busybox.tar

    cp tumbleweed-busybox.packages /tmp/test_with_label/DOCKER
    cp tumbleweed-busybox.packages /tmp/test/KIWI-docker/
    cp tumbleweed-busybox.packages /tmp/test/KIWI/

    touch /tmp/test_with_label/DOCKER/{busybox.tar.sha256,busybox.basepackages} /tmp/test/KIWI{,-docker}/busybox.tar.sha256
    popd
}

function cleanup {
    rm -rf /tmp/test{,_with_label}
}

function run_test_without_label() {
    pushd /tmp/test

    $1/containers-licenses

    LABELS=$(skopeo inspect docker-archive:/tmp/test/KIWI/busybox.tar | jq ' .Labels["org.opencontainers.image.licenses"]')
    [[ "${LABELS}"  = "\"Apache-2.0 AND (BSD-2-Clause AND LGPL-2.1-or-later AND BSD-3-Clause AND SUSE-Public-Domain) AND BSD-3-Clause AND GPL-2.0-or-later AND (GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0) AND LGPL-2.1-or-later AND MIT AND SUSE-Public-Domain\"" ]] || (echo "got unexpected label ${LABELS}"; exit 1)

    popd
}


function run_test_with_label() {
    pushd /tmp/test_with_label

    $1/containers-licenses

    LABELS=$(skopeo inspect docker-archive:/tmp/test_with_label/DOCKER/busybox_with_label.tar | jq ' .Labels["org.opencontainers.image.licenses"]')
    [[ "${LABELS}"  = "\"there's an entry already\"" ]] || (echo "got unexpected label ${LABELS}"; exit 1)

    popd
}

trap cleanup EXIT

prepare

run_test_with_label $(pwd)
run_test_without_label $(pwd)
