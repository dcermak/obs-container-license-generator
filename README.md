# obs-containers-licenses

This is a small script that can be inserted as a post build hook into a
container build on the [Open Build Service](https://openbuildservice.org/). It
collects the licenses of every package in the container image and populates the
container label
[`org.opencontainers.image.licenses`](https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys)
from these. This can be used to automatically set this label to the correct
value, provided that:

- all packages in your container declare their licenses correctly
- you have not added any additional content into your container


## Usage

1. Create a new package in the project where you will be building the container
   images called `containers-licenses`.

2. Copy the `containers-licenses` and `containers-licenses.spec` into the
   package and commit the package.

3. Add the following line to your project configuration (you probably want to
   add it only to the repository where you build your containers):
```
Preinstall: containers-licenses
```

4. Build/Rebuild your container images.
