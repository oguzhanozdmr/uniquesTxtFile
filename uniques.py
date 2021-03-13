#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ademoguzhanozdemir
"""

import sys
import os
import re


__params = {"-infile": None,
            "-outfile": None,
            "-sort": False,
            "-deleteblank": False,
            "-casesensitive": True}

__required_params = {"-infile": True,
                     "-outfile": False,
                     "-sort": False,
                     "-deleteblank": False,
                     "-casesensitive": False}

__params_description = {"-infile": "infile path",
                        "-outfile": "outfile path, default name_out.txt",
                        "-sort": "Default False",
                        "-deleteblank": "Default False",
                        "-casesensitive": "Default True"}

__params_have = {"-infile": True,
                 "-outfile": True,
                 "-sort": False,
                 "-deleteblank": False,
                 "-casesensitive": True}

__params_type = {"-infile": "(.*?)[.]txt$",
                 "-outfile": "(.*?)[.]txt$",
                 "-casesensitive": "(^False$|^True$)"}


def __read_txt(filepath: str = None) -> list:
    """
    read txt

    """
    if filepath is None:
        filepath = __params["-infile"]
    try:
        assert os.path.isfile(filepath), f"Not found {filepath}"
        file = open(filepath, "r", encoding="utf-8")
        txt_list = file.readlines()
        file.close()
    except IOError:
        assert False, "Error: File does not appear to exist."
        txt_list = None
    finally:
        assert filepath is not None, "Error"
        assert filepath.strip(), "Error"

    return txt_list


def __build_output_file_name(infile: str = None) -> str:
    """
    import os
    data1.txt
    data1.txt.out.txt
    0: data1
    1: .txt
    data1.out.txt
    """
    if infile is None:
        infile = __params["-infile"]

    parts = os.path.splitext(infile)
    # ('file1', '.txt')
    only_file_name = parts[0]
    only_file_ext = parts[1]
    new_file_name = only_file_name + "_out" + only_file_ext
    #                 file1           .out      .txt
    return new_file_name


def __write_txt(txt_list: list, out_path: str = None) -> None:
    """
    listeki değerleri txt dosyasına yazıyor

    Parameters
    ----------
    txt_list : list
        DESCRIPTION.
    out_path : str, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None
        DESCRIPTION.

    """
    if out_path is None:
        out_path = __params["-outfile"]
        if __params["-outfile"] is None:
            out_path = __build_output_file_name()

    assert isinstance(txt_list, list), "liste boş olamaz"

    txt = "".join(txt_list)
    file = open(out_path, "w", encoding="utf-8")
    file.write(txt)
    file.close()


def __process():
    """
    parameterlere göre işlemleri gerçekleştiriyor

    Returns
    -------
    None.

    """
    read_txt_line = __read_txt()
    if read_txt_line[-1]:
        read_txt_line[-1] = read_txt_line[-1] + "\n"
    new_txt_line = []
    unique_txt = []

    for row in read_txt_line:
        if __params["-deleteblank"]:
            if not row.strip():
                row = row.strip()

        if __params["-casesensitive"]:
            if row not in new_txt_line:
                new_txt_line.append(row)
        else:
            if row.lower() not in unique_txt:
                new_txt_line.append(row)
                unique_txt.append(row.lower())

    if __params["-sort"]:
        new_txt_line = __sort(new_txt_line)

    __write_txt(new_txt_line)
    print("successful")


def __partition(c_list: list, low_index: int, high_index: int):
    pivot = c_list[high_index]
    s_j = low_index - 1
    for s_i in range(low_index, high_index):
        if c_list[s_i] < pivot:
            s_j += 1
            c_list[s_i], c_list[s_j] = c_list[s_j], c_list[s_i]
    c_list[s_j + 1], c_list[high_index] = pivot, c_list[s_j + 1]
    return s_j + 1, c_list


def __quicksort(c_list: list, low_index: int, high_index: int):
    if low_index < high_index:
        pivot, c_list = __partition(c_list, low_index, high_index)
        __quicksort(c_list, low_index, pivot - 1)
        __quicksort(c_list, pivot + 1, high_index)
    return c_list


def __sort(txt_lst: list) -> list:
    """
    sıralama yapıyor

    Parameters
    ----------
    txt_lst : list
        DESCRIPTION.

    Returns
    -------
    list
        sıralanmış liste.

    """
    if len(txt_lst) < 100:
        # TODO: 10 listeyi parcalayip gonder
        txt_lst = __quicksort(txt_lst, 0, len(txt_lst)-1)
    else:
        # pyhton 3.8.1
        txt_lst = sorted(txt_lst)
    return txt_lst


def __error_params(parameter_name: str) -> None:
    """
    Exit system and message

    Parameters
    ----------
    parameter_name : str
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    print(f"{parameter_name} error value")
    sys.exit(0)


def __type_change() -> None:
    """
    gelen degerlerin tiplerini degistiriyor

    """
    __params["-casesensitive"] = __bool_type(__params["-casesensitive"])


def __bool_type(input_value: str) -> bool:
    """
     True False degerini bool olarak donduruyor

    Parameters
    ----------
    input_value : str

    Returns
    -------
    bool
        donen bool deger.

    """
    if isinstance(input_value, bool):
        return input_value
    result = False
    if input_value.strip().lower() == "true":
        result = True
    return result


def main():
    """
    main define
    Returns
    -------
    None.

    """
    if len(sys.argv) == 1:
        print("\n uniques params \n")
        for txt in __params_description:
            print(f"{txt} ->{__params_description[txt]}")
        sys.exit()

    for parameter in sys.argv:
        if parameter[0] != "-":
            continue

        if parameter in __params:
            if __params_have[parameter]:
                index_parameter = sys.argv.index(parameter) + 1
                if index_parameter < len(sys.argv):
                    parameter_value = sys.argv[index_parameter]
                    if re.search(__params_type[parameter], parameter_value):
                        __params[parameter] = parameter_value
                    else:
                        __error_params(parameter)
                else:
                    __error_params(parameter)
            else:
                __params[parameter] = not __params[parameter]
        else:
            print(f"Error: {parameter} unknow")
            sys.exit()

    for parameter in __required_params:
        if __required_params[parameter]:
            if __params[parameter] is None:
                print(f"{parameter} is required")
                sys.exit(0)

    __type_change()

    __process()


if __name__ == "__main__":
    main()
