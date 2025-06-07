import os
import subprocess

# Folder that holds all sub-folders of .cube LUTs
BASE_PATH = "luts"

# Reference image you want every LUT applied to
TEST_IMAGE = "test_image.jpg"

# One, flat destination for every thumbnail
THUMBNAIL_DIR = "filtered"


def generate_thumbnails(base_path: str, test_image: str, output_dir: str) -> None:
    """
    Apply every .cube LUT found under `base_path` to `test_image`
    and save the resulting JPEGs in `output_dir` (flat, no sub-folders).
    """
    # Make sure the single output folder exists
    os.makedirs(output_dir, exist_ok=True)

    for category in os.listdir(base_path):
        category_path = os.path.join(base_path, category)
        if not os.path.isdir(category_path):
            continue  # Skip stray files in BASE_PATH

        for lut in os.listdir(category_path):
            lut_path = os.path.join(category_path, lut)
            lut_name, _ = os.path.splitext(lut)

            #  e.g.  "Cinematic_Warm.cube" in category "Film" → "Film-Cinematic_Warm.jpg"
            thumbnail_name = f"{category}-{lut_name}.jpg"
            thumbnail_path = os.path.join(output_dir, thumbnail_name)

            ffmpeg_cmd = [
                "ffmpeg",
                "-y",  # overwrite existing files
                "-i", test_image,
                "-vf", f"lut3d={lut_path}",
                thumbnail_path,
            ]
            subprocess.run(ffmpeg_cmd, check=True)


if __name__ == "__main__":
    generate_thumbnails(BASE_PATH, TEST_IMAGE, THUMBNAIL_DIR)
