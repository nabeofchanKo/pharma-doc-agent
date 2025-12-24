from pypdf import PdfReader
import io

class PDFLoader:
    """
    Service class to handle PDF file loading and text extraction.
    """

    @staticmethod
    def extract_text_from_stream(file_stream: bytes) -> str:
            """
            Extracts full text from a PDF file stream (memory).
            
            Args:
                file_stream (bytes): The raw bytes of the PDF file.
            Returns:
                str: Extracted text content.
            """
            try:
                # Create a PDF reader object from bytes
                reader = PdfReader(io.BytesIO(file_stream))
                text = ""

                # Iterate over each page and extract text
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"

                return text

            except Exception as e:
                print(f"Error reading PDF:{e}")
                raise e