from pathlib import Path
from timeit import timeit
from textwrap import dedent as _

_fixtures_folder = Path(__file__).parent / "fixtures"


def test_1():
    return timeit(
        "(127, 0, 0, 1) in matrix",
        setup=_(
            """
            from blipgrep import Matrix
            matrix = Matrix()
            matrix.add(127, 0, 0, 1)
            """
        ),
        number=5000000
    )


def test_2():
    blacklist_file_path = _fixtures_folder / "test_blacklist.txt"
    return timeit(
        "matrix.populate_from(fd)",
        setup=_(
            f"""
            from blipgrep import Matrix
            matrix = Matrix()
            fd = open("{blacklist_file_path}")
            """
        ),
    )


def test_3():
    access_file_path = _fixtures_folder / "test_access.log"
    blacklist_file_path = _fixtures_folder / "test_blacklist_lite.txt"
    return timeit(
        "for _ in grep(fd, matrix): pass",
        setup=_(
            f"""
            from blipgrep import Matrix, grep
            matrix = Matrix()
            with open("{blacklist_file_path}") as fd:
                matrix.populate_from(fd)
            fd = open("{access_file_path}")
            """
        )
    )


def main():
    print(f"matrix.add() - {test_1()}")
    print(f"matrix.populate_from() - {test_2()}")
    print(f"grep() - {test_3()}")


if __name__ == "__main__":
    main()
