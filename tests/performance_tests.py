from timeit import timeit
from textwrap import dedent as _

def main():
    print(timeit(
        "(127, 0, 0, 1) in matrix",
        setup=_(
            """
            from blipgrep import Matrix
            
            matrix = Matrix()
            matrix.add(127, 0, 0, 1)
            """
        )
    ))

if __name__ == "__main__":
    main()
