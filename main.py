from core.simple_stag_inserter import SimpleStagInserter
from core.simple_stag_extractor import SimpleStagExtractor


def main():
    simple_stag_inserter = SimpleStagInserter()
    simple_stag_inserter.insert_file_at_the_end("ex01.pdf", "trip.jpg")
    
    simple_stag_extractor = SimpleStagExtractor()
    simple_stag_extractor.extract_file("trip.jpg Copy.jpg")

if __name__ == "__main__":
    main()
