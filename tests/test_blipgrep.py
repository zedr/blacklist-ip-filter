from blipgrep import Matrix


def test_matrix_can_add_single_ip():
    matrix = Matrix()
    matrix.add(127, 0, 0, 1)
    assert (127, 0, 0, 1) in matrix
    assert (127, 0, 0, 2) not in matrix
