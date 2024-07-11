import requests
import csv
from typing import List, Final

URL: Final = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"
HEADERS: Final = {
    'User-Agent': 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}


def from_list_row_to_csv(list_of_rows: List[list]) -> None:
    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Company", "Street", "City", "St", "ZIPCode", "IsValid"])
        writer.writerows(list_of_rows)


def from_csv_to_list_row(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        csv_reader = csv.reader(f)
        return list(csv_reader)[1:]


def main() -> None:
    list_of_rows: List[str] = from_csv_to_list_row("input_data.csv")
    for row in list_of_rows:
        data_dict: dict = {"companyName": row[0], "address1": row[1],
                "city": row[2], "state": row[3], "zip": row[4]}
        r = requests.post(URL, data=data_dict, headers=HEADERS).content.decode("utf-8")
        if "SUCCESS" in r:
            row.append("True")
        else:
            row.append("False")
    from_list_row_to_csv(list_of_rows)


if __name__ == "__main__":
    main()
