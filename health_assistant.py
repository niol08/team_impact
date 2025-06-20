# Create a new file health_assistant.py with the core functionality
import os
import requests
import json
from datetime import datetime
import PyPDF2
import pytesseract
from PIL import Image
import PyPDF2
import fitz  # PyMuPDF for PDF text extraction
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT_NAME")
CURACEL_API_KEY = os.getenv("CURACEL_API_KEY")
CURACEL_BASE_URL = os.getenv("CURACEL_BASE_URL")

SUPPORTED_TEXT_EXTENSIONS = ['.txt', '.md']
SUPPORTED_PDF_EXTENSIONS = ['.pdf']
SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']



# Load environment variables
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT_NAME")
CURACEL_API_KEY = os.getenv("CURACEL_API_KEY")
CURACEL_BASE_URL = os.getenv("CURACEL_BASE_URL")

SUPPORTED_TEXT_EXTENSIONS = ['.txt', '.md']
SUPPORTED_PDF_EXTENSIONS = ['.pdf']
SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']

def check_environment_variables():
    required_vars = {
        "OPENAI_ENDPOINT": AZURE_OPENAI_ENDPOINT,
        "OPENAI_API_KEY": AZURE_OPENAI_KEY,
        "OPENAI_DEPLOYMENT_NAME": AZURE_OPENAI_DEPLOYMENT,
        "CURACEL_API_KEY": CURACEL_API_KEY,
        "CURACEL_BASE_URL": CURACEL_BASE_URL
    }
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        print("Error: Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease check your .env file and ensure all variables are set correctly.")
        return False
    print("Environment variables loaded successfully!")
    return True

def extract_text_from_pdf_pypdf2(file_path):
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF with PyPDF2: {str(e)}")
        return None

def extract_text_from_pdf_pymupdf(file_path):
    try:
        text = ""
        pdf_document = fitz.open(file_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text() + "\n"
        pdf_document.close()
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF with PyMuPDF: {str(e)}")
        return None

def extract_text_from_pdf(file_path):
    print("Extracting text from PDF...")
    text = extract_text_from_pdf_pypdf2(file_path)
    if not text or len(text.strip()) < 50:
        print("Trying alternative PDF extraction method...")
        text = extract_text_from_pdf_pymupdf(file_path)
    if text and len(text.strip()) > 0:
        print(f"Successfully extracted {len(text)} characters from PDF")
        return text
    else:
        print("Failed to extract text from PDF")
        return None

def extract_text_from_image(file_path):
    try:
        print("Performing OCR on image...")
        try:
            pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            print("Error: Tesseract OCR is not installed or not found in PATH")
            print("Please install Tesseract OCR:")
            print("- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
            print("- macOS: brew install tesseract")
            print("- Linux: sudo apt install tesseract-ocr")
            return None
        image = Image.open(file_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        text = pytesseract.image_to_string(image, lang='eng')
        if text and len(text.strip()) > 0:
            print(f"Successfully extracted {len(text)} characters from image")
            return text.strip()
        else:
            print("No text found in the image")
            return None
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        return None

def process_document_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    file_extension = Path(file_path).suffix.lower()
    try:
        if file_extension in SUPPORTED_TEXT_EXTENSIONS:
            print("Processing text file...")
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif file_extension in SUPPORTED_PDF_EXTENSIONS:
            return extract_text_from_pdf(file_path)
        elif file_extension in SUPPORTED_IMAGE_EXTENSIONS:
            return extract_text_from_image(file_path)
        else:
            print(f"Unsupported file type: {file_extension}")
            print(f"Supported formats:")
            print(f"  Text files: {', '.join(SUPPORTED_TEXT_EXTENSIONS)}")
            print(f"  PDF files: {', '.join(SUPPORTED_PDF_EXTENSIONS)}")
            print(f"  Image files: {', '.join(SUPPORTED_IMAGE_EXTENSIONS)}")
            return None
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

def analyze_document_with_gpt(doc_text):
    # Very solid prompt for medical document analysis
    prompt = f"""
You are a highly knowledgeable, ethical, and helpful medical assistant. 
A user has uploaded the following medical document (could be a doctor’s note, lab result, discharge summary, scan report, referral, or insurance form): 

--- DOCUMENT START ---
{doc_text[:3500]}
--- DOCUMENT END ---

1. Summarize the main findings and information in this document.
2. List any key diagnoses, symptoms, medications, or procedures mentioned.
3. Highlight any abnormal results or values (if present).
4. Suggest follow-up questions or next steps that the user should consider.
5. Remind the user to consult a healthcare professional for medical advice.

Return your answers as concise bullet points under each numbered instruction above.
"""
    try:
        messages = [
            {"role": "system", "content": "You are a careful medical document summarizer and explainer."},
            {"role": "user", "content": prompt}
        ]
        endpoint = AZURE_OPENAI_ENDPOINT.rstrip('/')
        url = f"{endpoint}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-12-01-preview"
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_KEY
        }
        data = {
            "messages": messages,
            "max_tokens": 800,
            "temperature": 0.5,
            "top_p": 0.85
        }
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error during document analysis: {e}")
        return None

def chat_with_bot(message, conversation=[], doc_summary=None, curacel_context=None):
    try:
        system_message = """You are an intelligent health assistant with access to medical document analysis and health insurance claims processing through Curacel. 
        
        You can help users with:
        - General health questions and advice
        - Medical document analysis (from text, PDF, and image files)
        - Health insurance claim processing
        - Treatment cost estimation
        - Insurance coverage verification
        
        Always provide helpful, accurate medical information while reminding users to consult healthcare professionals for serious concerns."""
        
        messages = [{"role": "system", "content": system_message}]
        
        if doc_summary:
            messages.append({"role": "system", "content": f"Medical document analysis: {doc_summary}"})
        
        if curacel_context:
            messages.append({"role": "system", "content": f"Insurance/Claims context: {curacel_context}"})
        
        recent_conversation = conversation[-10:] if len(conversation) > 10 else conversation
        messages += recent_conversation
        messages.append({"role": "user", "content": message})

        endpoint = AZURE_OPENAI_ENDPOINT.rstrip('/')
        url = f"{endpoint}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-12-01-preview"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_KEY
        }
        
        data = {
            "messages": messages, 
            "max_tokens": 800,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        finish_reason = result["choices"][0]["finish_reason"]
        if finish_reason == "length":
            content += "\n\n[Response truncated due to length limit. Please ask me to continue if you need more information.]"
        return content
    
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again with a shorter message."
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Azure OpenAI: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def create_curacel_claim(claim_data):
    try:
        url = f"{CURACEL_BASE_URL}/api/v1/claims"
        headers = {
            "Authorization": f"Bearer {CURACEL_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.post(url, headers=headers, json=claim_data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating Curacel claim: {str(e)}")
        return None

def get_treatment_cost_estimate(procedure_code, location="Nigeria"):
    try:
        url = f"{CURACEL_BASE_URL}/api/v1/estimates"
        headers = {
            "Authorization": f"Bearer {CURACEL_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "procedure_code": procedure_code,
            "location": location,
            "currency": "NGN"
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting cost estimate: {str(e)}")
        return None

def verify_insurance_coverage(policy_number, procedure_code):
    try:
        url = f"{CURACEL_BASE_URL}/api/v1/coverage/verify"
        headers = {
            "Authorization": f"Bearer {CURACEL_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "policy_number": policy_number,
            "procedure_code": procedure_code
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error verifying coverage: {str(e)}")
        return None

def process_user_request(user_input, conversation, doc_summary=None):
    insurance_keywords = [
        "insurance", "claim", "coverage", "policy", "premium", "deductible",
        "cost", "price", "estimate", "reimburse", "copay", "benefits"
    ]
    curacel_context = None
    if any(keyword in user_input.lower() for keyword in insurance_keywords):
        if "cost" in user_input.lower() or "price" in user_input.lower():
            cost_info = get_treatment_cost_estimate("general_consultation")
            if cost_info:
                curacel_context = f"Treatment cost information: {json.dumps(cost_info, indent=2)}"
        elif "coverage" in user_input.lower() or "policy" in user_input.lower():
            curacel_context = "Insurance coverage verification available. Please provide your policy number for specific coverage details."
    return chat_with_bot(user_input, conversation, doc_summary, curacel_context)

def show_curacel_menu():
    print("\n=== Curacel Health Insurance Services ===")
    print("1. Create Insurance Claim")
    print("2. Get Treatment Cost Estimate")
    print("3. Verify Insurance Coverage")
    print("4. Back to Main Chat")
    print("==========================================")

def handle_curacel_services():
    while True:
        show_curacel_menu()
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            print("\n--- Create Insurance Claim ---")
            patient_name = input("Patient Name: ")
            procedure = input("Treatment/Procedure: ")
            amount = input("Claim Amount (NGN): ")
            hospital = input("Hospital/Clinic: ")
            claim_data = {
                "patient_name": patient_name,
                "procedure": procedure,
                "amount": float(amount) if amount.replace('.', '').isdigit() else 0,
                "provider": hospital,
                "date": datetime.now().isoformat(),
                "currency": "NGN"
            }
            result = create_curacel_claim(claim_data)
            if result:
                print(f"\nClaim created successfully!")
                print(f"Claim ID: {result.get('claim_id', 'N/A')}")
                print(f"Status: {result.get('status', 'N/A')}")
            else:
                print("Failed to create claim. Please try again.")
        elif choice == "2":
            print("\n--- Treatment Cost Estimate ---")
            procedure = input("Enter procedure/treatment name: ")
            location = input("Location (default: Nigeria): ") or "Nigeria"
            estimate = get_treatment_cost_estimate(procedure, location)
            if estimate:
                print(f"\nCost Estimate for {procedure}:")
                print(f"Estimated Cost: ₦{estimate.get('estimated_cost', 'N/A')}")
                print(f"Location: {estimate.get('location', location)}")
            else:
                print("Could not retrieve cost estimate. Please try again.")
        elif choice == "3":
            print("\n--- Verify Insurance Coverage ---")
            policy_number = input("Policy Number: ")
            procedure = input("Procedure/Treatment: ")
            coverage = verify_insurance_coverage(policy_number, procedure)
            if coverage:
                print(f"\nCoverage Information:")
                print(f"Covered: {'Yes' if coverage.get('covered') else 'No'}")
                print(f"Coverage Amount: ₦{coverage.get('coverage_amount', 'N/A')}")
                print(f"Deductible: ₦{coverage.get('deductible', 'N/A')}")
            else:
                print("Could not verify coverage. Please check your policy number.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def show_supported_formats():
    print("\nSupported File Formats:")
    print(f"Text files: {', '.join(SUPPORTED_TEXT_EXTENSIONS)}")
    print(f"PDF files: {', '.join(SUPPORTED_PDF_EXTENSIONS)}")
    print(f"Image files: {', '.join(SUPPORTED_IMAGE_EXTENSIONS)}")
    print()

def main():
    if not check_environment_variables():
        return
    print("\nEnhanced Health Assistant with Multi-Format Document Support")
    print("=" * 65)
    print("Features:")
    print("Chat with AI Health Assistant")
    print("Process Text, PDF, and Image files")
    print("OCR for medical images and scanned documents")
    print("Curacel Insurance Services")
    print("=" * 65)
    show_supported_formats()
    print("Choose an option:")
    print("1. Chat with Health Assistant")
    print("2. Upload and Analyze Medical Document")
    print("3. Chat with Document Analysis")
    print("4. Access Curacel Insurance Services")
    print("5. Exit")
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        if choice in ["1", "2", "3", "4", "5"]:
            break
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
    conversation = []
    doc_summary = None

    if choice == "2" or choice == "3":
        show_supported_formats()
        doc_path = input("Enter the path to your medical document: ").strip()
        doc_path = doc_path.strip('"\'')
        try:
            print(f"\nProcessing file: {doc_path}")
            doc_text = process_document_file(doc_path)
            if not doc_text:
                print("Failed to extract text from the document.")
                return
            if len(doc_text.strip()) < 10:
                print("Warning: Very little text was extracted from the document.")
                print("This might indicate:")
                print("- The document is mostly images (for PDFs)")
                print("- Poor image quality (for image files)")
                print("- The document is in a different language")
            print(f"\nExtracted text preview ({len(doc_text)} characters):")
            print("-" * 50)
            print(doc_text[:300] + "..." if len(doc_text) > 300 else doc_text)
            print("-" * 50)
            print("\nAnalyzing document with GPT...")
            analysis = analyze_document_with_gpt(doc_text)
            if analysis:
                doc_summary = analysis
                print("\nDocument analysis completed!")
                print("\nSummary (first 350 chars):")
                print(doc_summary[:350] + "..." if len(doc_summary) > 350 else doc_summary)
                if choice == "2":
                    print("\nAnalysis complete! You can now chat with the assistant about this document.")
                    return
            else:
                print("Document analysis failed, but you can still chat about the extracted text.")
                doc_summary = f"Document text (analysis failed): {doc_text[:1000]}"
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return

    elif choice == "4":
        handle_curacel_services()
        return
    elif choice == "5":
        print("Goodbye! Stay healthy!")
        return

    if choice == "1" or choice == "3":
        print(f"\nStart chatting with the health assistant.")
        print("Try asking about: symptoms, treatments, insurance costs, or coverage")
        if doc_summary:
            print("Your document has been analyzed and is available for discussion")
        print("Type 'curacel' for insurance services or 'exit' to quit.\n")
        while True:
            try:
                user_input = input("> ").strip()
                if user_input.lower() == "exit":
                    print("Goodbye! Take care of your health!")
                    break
                if user_input.lower() == "curacel":
                    handle_curacel_services()
                    continue
                if not user_input:
                    print("Please enter a message.")
                    continue
                print("Thinking...")
                reply = process_user_request(user_input, conversation, doc_summary)
                print(f"\nAssistant: {reply}\n")
                conversation.append({"role": "user", "content": user_input})
                conversation.append({"role": "assistant", "content": reply})
            except KeyboardInterrupt:
                print("\nGoodbye! Stay healthy!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()