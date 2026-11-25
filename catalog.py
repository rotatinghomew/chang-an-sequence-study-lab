"""盘点导入前收到的 JSON 资料。"""

from argparse import ArgumentParser
import json
from pathlib import Path


def read_packet(directory):
    """读取同一交换目录中的记录表，并核对首列标识。"""
    directory = Path(directory)
    content = {}
    for path in sorted(directory.glob("*.json")):
        records = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError(f"{path.name} 需要 JSON 对象数组")
        identifiers = set()
        for entry in records:
            if not isinstance(entry, dict) or not isinstance(entry.get("id"), str) or not entry["id"].strip():
                raise ValueError(f"{path.name} 存在没有标识的记录")
            if entry["id"] in identifiers:
                raise ValueError(f"{path.name} 重复记录标识 {entry['id']}")
            identifiers.add(entry["id"])
        content[path.stem] = records
    if not content:
        raise FileNotFoundError(f"{directory} 没有 JSON 资料表")
    return content


def main():
    parser = ArgumentParser(description="核对交换资料并盘点各表记录数")
    parser.add_argument("directory", type=Path, help="交换资料目录")
    args = parser.parse_args()
    packet = read_packet(args.directory)
    for name, rows in packet.items():
        print(f"{name}  {len(rows)} 条")


if __name__ == "__main__":
    main()
