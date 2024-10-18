from core.simple_stag_inserter import SimpleStagInserter


def main():
    simple_stag_inserter = SimpleStagInserter()
    simple_stag_inserter.insert_file_at_the_end("ex01.pdf", "trip.jpg")

if __name__ == "__main__":
    main()
