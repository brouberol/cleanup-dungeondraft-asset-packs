"""
Script in charge of cleaning up the tags in your Dungeondraft asset library,
to make sure to only keep tags actually linked with assets.
"""

import logging
import json
import argparse
import shutil
import os
import subprocess

from pathlib import Path
from contextlib import contextmanager


logging.basicConfig(level=logging.INFO)


@contextmanager
def working_directory(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    Usage:
    > # Do something in original directory
    > with working_directory('/my/new/path'):
    >     # Do something in new directory
    > # Back to old directory
    """

    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def ensure_dependencies_are_present():
    return all(map(shutil.which, ["dungeondraft-pack", "dungeondraft-unpack"]))


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--assets-dir",
        help="The directory containing your Dungeondraft assets",
        required=True,
    )
    return parser.parse_args()


def unpack_dungeondraft_pack(pack_path: Path) -> Path:
    logging.info(f"Unpacking {str(pack_path)}")
    subprocess.run(
        ["dungeondraft-unpack", "-overwrite", str(pack_path), "./tmp"], check=True
    )
    return Path() / "tmp" / pack_path.stem


def repack_dungeondraft_pack(pack_dir_path: Path, output_dir) -> None:
    logging.info(f"Repacking {str(pack_dir_path)}")
    subprocess.run(
        ["dungeondraft-pack", "-overwrite", str(pack_dir_path), str(output_dir)],
        check=True,
    )


def cleanup_dungeondraft_pack(unpacked_dir: Path) -> None:
    with working_directory(unpacked_dir):
        tagfile = Path("./data/default.dungeondraft_tags")
        if not tagfile.exists():
            logging.info("Skipping, as no dungeondraft_tags file is found")
            return
        with open(tagfile) as tags_f:
            empty_tags = set()
            tags = json.load(tags_f)
            cleaned_tags = {"tags": {}, "sets": {}}
            for tag, objects in tags["tags"].items():
                tag = tag.lstrip(".")
                if not objects:
                    logging.info(f"Skipping empty tag {tag}")
                    empty_tags.add(tag)
                else:
                    cleaned_tags["tags"][tag] = objects
            for tagset_name, tagset in tags["sets"].items():
                if tagset_name not in empty_tags:
                    cleaned_tagset = [
                        tag.lstrip(".")
                        for tag in tagset_name
                        if tag.lstrip(".") not in empty_tags
                    ]
                    cleaned_tags["sets"][tagset_name] = cleaned_tagset

        with open(tagfile, "w") as out:
            json.dump(cleaned_tags, out, indent=2)


def main():
    if not ensure_dependencies_are_present():
        logging.error(
            (
                "The required packer and unpacker are not found in your path. "
                "installation instrcutions from https://github.com/Ryex/Dungeondraft-GoPackager"
            )
        )

    args = parse_args()
    with working_directory(args.assets_dir):
        for filename in os.listdir():
            file_obj = Path(args.assets_dir) / filename
            if file_obj.is_file() and file_obj.suffix == ".dungeondraft_pack":
                unpack_dir = unpack_dungeondraft_pack(file_obj)
                cleanup_dungeondraft_pack(unpack_dir)
                output_dir = Path(args.assets_dir) / "cleaned"
                os.makedirs(output_dir, exist_ok=True)
                repack_dungeondraft_pack(unpack_dir, output_dir)
        shutil.rmtree(Path("./tmp"))
