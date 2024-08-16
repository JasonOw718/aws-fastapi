from unstructured.partition.pdf import partition_pdf

Header=[]
Footer=[]
Title=[]
NarrativeText=[]
Text=[]
ListItem=[]
img=[]
tab=[]

def extract_doc():
        print("Start extracting data from documents....")
        raw_pdf_elements=partition_pdf(
                filename="./data/test.pdf",
                strategy="hi_res",
                extract_images_in_pdf=True,
                extract_image_block_types=["Image", "Table"],
                extract_image_block_to_payload=False,
                extract_image_block_output_dir="extracted_data"
        )

        print("Components Extracted...")

        print("Separating Components...")

        for element in raw_pdf_elements:
                if "unstructured.documents.elements.Header" in str(type(element)):
                        Header.append(str(element))
                elif "unstructured.documents.elements.Footer" in str(type(element)):
                        Footer.append(str(element))
                elif "unstructured.documents.elements.Title" in str(type(element)):
                        Title.append(str(element))
                elif "unstructured.documents.elements.NarrativeText" in str(type(element)):
                        NarrativeText.append(str(element))
                elif "unstructured.documents.elements.Text" in str(type(element)):
                        Text.append(str(element))
                elif "unstructured.documents.elements.ListItem" in str(type(element)):
                        ListItem.append(str(element))
                elif "unstructured.documents.elements.Image" in str(type(element)):
                        img.append(str(element))   
                elif "unstructured.documents.elements.Table" in str(type(element)):
                        tab.append(str(element))
        print("Categorization completed...")
