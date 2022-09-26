from pathlib import Path

from blipgrep import Matrix, get_ipv4_seq, generate_matrix

_fixture_folder = Path(__file__).parent / "fixtures"


def test_matrix_can_add_single_ip():
    matrix = Matrix()
    matrix.add(127, 0, 0, 1)

    assert (127, 0, 0, 1) in matrix
    assert (127, 0, 0, 2) not in matrix


def test_matrix_can_add_ip_range():
    matrix = Matrix()
    for ipv4_address in get_ipv4_seq("192.168.0.0/30"):
        matrix.add(*ipv4_address)

    assert (192, 168, 0, 1) in matrix
    assert (192, 168, 0, 2) in matrix
    assert (192, 168, 0, 3) not in matrix


def test_matrix_can_parse_blacklist_file():
    with open(_fixture_folder / "fixture_bl.txt") as fd:
        matrix = generate_matrix(fd)

    assert (127, 0, 0, 1) in matrix
    assert (192, 168, 1, 1) in matrix
    assert (192, 168, 1, 2) in matrix
    assert (192, 168, 1, 3) not in matrix
