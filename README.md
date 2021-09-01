`cleanup-dungeondraft-asset-packs` is a CLI tool to cleanup Dungeondraft asset packs.

I noticed that some asset packs from [CartographyAssets](https://cartographyassets.com) would register entries in the [Dungeondraft](https://dungeondraft.net) tag list that are associated with an empty asset list. This made the asset discovery process quite painful. 

![Emptry tag entry](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/cleaning-up-dungeondraft-tag-list/empty-assets.webp)

I wrote that CLI tool to automate the process of cleaning up these empty tag entries, in order to keep the tag list as clean as possible.

## Installation

To install the CLI, run

```console
pip3 install cleanup-dungeondraft-asset-packs
```

**Note**: This script is wrapping the `dungeondraft-unpack` and `dungeondraft-pack` commands, installable via [https://github.com/Ryex/Dungeondraft-GoPackager](https://github.com/Ryex/Dungeondraft-GoPackager). You'll need to follow their installation instructions as well. Don't worry if you don't have `go` installed locally, they provide pre-compiled binaries that you have to download and move into your `PATH`.
