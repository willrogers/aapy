import os
from aa import epics_event_pb2 as ee
from aa.pb_tools import fixes, pb_file

def test_split_files_by_prefix_gives_correct_output():
    test_filenames = [
        "OPS:2017.pb",
        "OPS:2018.pb",
        "OPS:2019.pb",
        "STAT:2017.pb",
        "STAT:2018.pb",
        "STAT:2019.pb",
    ]
    output = fixes.group_filenames_by_prefix(test_filenames)
    expected_output = {
        "OPS":
            ["OPS:2017.pb",
            "OPS:2018.pb",
            "OPS:2019.pb",],
        "STAT":
            ["STAT:2017.pb",
            "STAT:2018.pb",
            "STAT:2019.pb",],
    }
    assert output == expected_output


def test_find_all_files_in_tree_gives_expected_output():
    # Build absolute path to our test directory from the relative path
    test_dir = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "mock_lts"
        )
    )
    output, count_found = fixes.find_all_files_in_tree(test_dir)

    base_path = os.path.join(test_dir, "BL13I", "OP", "MIRR", "01")
    expect = {
        os.path.join(base_path, "X", "RBV"): fixes.PbGroup(
            dir_path=os.path.join(base_path, "X"),
            file_paths=sorted([
                os.path.join(base_path, "X", "RBV:2018.pb"),
                os.path.join(base_path, "X", "RBV:2019.pb"),
            ])),
        os.path.join(base_path, "STAT"): fixes.PbGroup(
            dir_path = base_path,
            file_paths = sorted([
                os.path.join(base_path, "STAT:2018.pb"),
                os.path.join(base_path, "STAT:2019.pb"),
            ])),

    }
    expect_count = 4
    assert output == expect
    assert count_found == expect_count


def test_group_files_by_year_gives_expected_output():

    filenames = []
    pb_files = []
    for year in [2017, 2018, 2018, 2019]:
        test_file = pb_file.PbFile()
        test_file.payload_info = ee.PayloadInfo(
            year=year,
            type=5,
            pvname="BL14J-PS-SHTR-03:OPS",
            elementCount=1,
        )
        pb_files.append(test_file)
        suffix = ""
        while f"{year}.pb{suffix}" in filenames:
            suffix += "1"
        filenames.append(f"{year}.pb{suffix}")

    result = fixes.group_files_by_year(filenames, pb_files)

    expected = {
        2017: ["2017.pb"],
        2018: ["2018.pb",
               "2018.pb1"],
        2019: ["2019.pb"],
    }

    assert result == expected


def test_group_files_by_type_gives_expected_output():

    filenames = []
    pb_files = []
    for type in [1, 2, 3, 3, 4]:
        test_file = pb_file.PbFile()
        year = 2000 + type
        test_file.payload_info = ee.PayloadInfo(
            year=2000 + type,
            type=type,
            pvname="BL14J-PS-SHTR-03:OPS",
            elementCount=1,
        )
        pb_files.append(test_file)
        suffix = ""
        while f"{year}.pb{suffix}" in filenames:
            suffix += "1"
        filenames.append(f"{year}.pb{suffix}")

    result = fixes.group_files_by_type(filenames, pb_files)

    expected = {
        1: ["2001.pb"],
        2: ["2002.pb"],
        3: ["2003.pb",
            "2003.pb1"],
        4: ["2004.pb"],
    }

    assert result == expected