from pathlib import Path
from lib.main import parseString

if __name__ == "__main__":
    path = Path(__file__).parent / "spec" / "2_multiple.txt"
    with open(path) as f:
        contents = f.read()

    print(*parseString(contents), sep="\n")
