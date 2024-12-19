import os
import json
import pdfplumber
import fitz
import tabula

# Preprocessing for an individual document
def preprocess_pdf(pdf_path, dir_out):
    results = []
    document_name = os.path.basename(pdf_path)

    # Creating directories for output
    os.makedirs(dir_out, exist_ok=True)
    dir_img = os.path.join(dir_out, "images")
    os.makedirs(dir_img, exist_ok=True)
    dir_csv = os.path.join(dir_out, "tables")
    os.makedirs(dir_csv, exist_ok=True)

    # Extracting text from the PDF
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            text = page.extract_text() or ""
            all_text += text

    # Extracting images
    pdf_document = fitz.open(pdf_path)
    img_paths = []
    for i in range(len(pdf_document)):
        page = pdf_document[i]
        images = page.get_images(full=True)
        for j, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            img_bytes = base_image["image"]
            img_ext = base_image["ext"]
            img_path = os.path.join(dir_img, f"{document_name}_page{i+1}_img{j+1}.{img_ext}")

            with open(img_path, "wb") as img_file:
                img_file.write(img_bytes)

            img_paths.append(img_path)

    # Extracting tables
    dfs = tabula.read_pdf(pdf_path, pages="all")
    csv_paths = []
    for i in range(len(dfs)):
        csv_path = os.path.join(dir_csv, f"{document_name}_table{i+1}.csv")
        dfs[i].to_csv(csv_path)
        csv_paths.append(csv_path)

    results.append({
        "document_name": document_name,
        "text": all_text,
        "img_paths": img_paths,
        "csv_paths": csv_paths,
    })

    return results

# Adding title and link for each paper
def load_metadata(metadata_path):
    with open(metadata_path, 'r') as file:
        metadata = json.load(file)
    return {item['filename']: item for item in metadata}

# Handling all the documents in a directory
def preprocess_documents(input_dir, metadata_path, dir_out):
    all_results = []
    metadata = load_metadata(metadata_path)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            print(f"Processing: {filename}")
            pdf_results = preprocess_pdf(pdf_path, dir_out)

            for result in pdf_results:
                file_metadata = metadata.get(filename)
                if file_metadata:
                    result["title"] = file_metadata.get("title")
                    result["link"] = file_metadata.get("link")
            
            all_results.extend(pdf_results)

    return all_results


preprocessed_data = preprocess_documents("documents", "metadata.json", "preprocessed_data")
output_path = os.path.join("preprocessed_data", "preprocessed_results_with_metadata.json")

with open(output_path, "w") as f:
    json.dump(preprocessed_data, f, indent=4)

print(f"Preprocessing complete, see {output_path}.")
