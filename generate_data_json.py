from dropbox.sharing import PathLinkMetadata

from generate_points import get_points_array


def generate_data_json(shared_link: PathLinkMetadata) -> dict:
    points = get_points_array()
    return {"type": "image",
            "attributes": {"url": shared_link.url[:-1] + '1',
                           "points": points
                           }
            }
