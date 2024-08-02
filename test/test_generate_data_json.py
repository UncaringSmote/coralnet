import json
import random
from unittest import TestCase

from dropbox.sharing import PathLinkMetadata

from coralnet_load_model import Data
from generate_json import generate_data_json


class Test(TestCase):
    def old_code(self,tmp_name):
        return {"type": "image",
                     "attributes": {"url": tmp_name.url[:-1] + '1',
                                    "points": [
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(600, 1067)},
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(1067, 1533)},
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(1533, 2000)},
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(2000, 2467)},
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(2467, 2933)},
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(2933, 3400)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(600, 1067)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(1067, 1533)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(1533, 2000)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(2000, 2467)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(2467, 2933)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(2933, 3400)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(600, 1067)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(1067, 1533)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(1533, 2000)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(2000, 2467)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(2467, 2933)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(2933, 3400)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(600, 1067)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(1067, 1533)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(1533, 2000)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(2000, 2467)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(2467, 2933)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(2933, 3400)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(600, 1067)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(1067, 1533)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(1533, 2000)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(2000, 2467)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(2467, 2933)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(2933, 3400)},
                                    ]
                                    }
                     }
    def test_generate_data_json(self):
        random.seed(1)
        result= generate_data_json(PathLinkMetadata(url="testurl"))
        val = json.loads(result.to_json())
        with open(f'statestest.json', 'w') as outfile:
            json.dump(result.to_dict(), outfile)

        with open(f"states.json", "r+") as f:
            self.state_data = StateData.from_dict(json.load(f))


        random.seed(1)
        old = self.old_code(PathLinkMetadata(url="testurl"))
        assert sorted(val.items()) == sorted(old.items())
