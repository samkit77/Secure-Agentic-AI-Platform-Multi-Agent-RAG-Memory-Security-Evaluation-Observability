from pypdf import PdfReader


def parse_pdf(file_path: str):
    """
    Parses a PDF file and extracts readable text.
    """

    try:
        reader = PdfReader(file_path)

        full_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                full_text += text + "\n"

        return full_text

    except Exception as e:
        raise e