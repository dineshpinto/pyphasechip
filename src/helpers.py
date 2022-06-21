import datetime
import re
from typing import Tuple


def extract_metadata_from_filename(filename: str) -> Tuple[int, datetime.datetime]:
    match = re.search('\d{1-100}', filename)
    if match:
        print(match.group())
        well_number = int(match.group()[0])
        timestamp = datetime.datetime.now()
        return well_number, timestamp
    return 0, datetime.datetime.now()
