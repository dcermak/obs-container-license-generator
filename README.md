# container-license-generator

This is a small script that can be inserted as a post build hook into a
container build in the [Open Build Service](https://openbuildservice.org/). It
collects the licenses of every package in the container image and populates the
container label
[`org.opencontainers.image.licenses`](https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys)
from these. This can be used to automatically set this label to the correct
value, provided that all packages in your container declare their licenses
correctly.

## Usage

1. Create a new package in the project where you will be building the container
   images called `container-license-generator`.

2. Copy the `container-license-generator` and `container-license-generator.spec` into the
   package and commit the package. Alternatively you can also use the following
   `_service` file to automate this process:
```xml
<services>
  <service name="obs_scm">
    <param name="url">https://github.com/dcermak/obs-container-license-generator.git</param>
    <param name="scm">git</param>
    <param name="extract">container-license-generator</param>
    <param name="extract">container-license-generator.spec</param>
    <param name="extract">README.md</param>
    <param name="exclude">root</param>
    <param name="revision">main</param>
  </service>
</services>
```

3. Add the following line to your project configuration (you probably want to
   add it only to the repository where you build your containers):
```
Preinstall: container-license-generator
```

4. Build/Rebuild your container images.


## Configuration

The `container-license-generator` can be configured by creating a file called
`container-license-generator.json` in your package in the Open Build Service. At
the moment it supports a the configuration option `inheritLabel`. When set to
`true` it will append the contents of the `org.opencontainers.image.licenses`
label of the final container image (e.g. set by you or inherited from a base
image) to the license list that was extracted from the `.packages` file.

The default behavior is to not modify an existing
`org.opencontainers.image.licenses` label.

Assuming that you build a container in the Open Build Service from the following
`Dockerfile`:
```Dockerfile
#!BuildTag:test:latest

FROM opensuse/tumbleweed
RUN echo "My MIT licensed quote" > /quote.txt
RUN zypper -n in make
LABEL org.opencontainers.image.licenses MIT
```
then `container-license-generator` would do nothing by default and your final
container would have the `org.opencontainers.image.licenses` label set to
`MIT`. However, when you include the configuration file
`container-license-generator.json` with the following contents:
```json
{"inheritLabel": true}
```
Then the final container will have the `org.opencontainers.image.licenses` label
set to `${LICENSES_FROM_DOT_PACKAGES} AND MIT`.
