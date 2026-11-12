import subprocess
import os

def compress_pdf(input_path, output_path, quality='ebook'):
    """
    Compress a PDF file using Ghostscript.

    Args:
        input_path (str): Path to the input PDF file.
        output_path (str): Path to save the compressed PDF.
        quality (str): Compression quality. Options: 'screen', 'ebook', 'printer', 'prepress', 'default'.
                      'ebook' is good for web, reduces size while maintaining readability.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Ghostscript command for compression
    gs_command = [
        'gswin64c',  # Use 'gswin32c' if 32-bit, or 'gs' on Linux/Mac
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS=/{quality}',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        f'-sOutputFile={output_path}',
        input_path
    ]

    try:
        result = subprocess.run(gs_command, capture_output=True, text=True, check=True)
        print(f"PDF compressed successfully. Output: {output_path}")
        # Check file sizes
        input_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
        output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
        print(".2f")
    except subprocess.CalledProcessError as e:
        print(f"Error compressing PDF: {e}")
        print(f"Ghostscript output: {e.stderr}")
    except FileNotFoundError:
        print("Ghostscript not found. Please install Ghostscript and ensure 'gswin64c' is in your PATH.")

# Example usage
if __name__ == "__main__":
    input_pdf = "your_large_file.pdf"  # Replace with your 206MB PDF path
    output_pdf = "compressed_file.pdf"
    compress_pdf(input_pdf, output_pdf, quality='ebook')