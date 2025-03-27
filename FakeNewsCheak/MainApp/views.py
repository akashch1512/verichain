# views.py
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import google.generativeai as genai

# Configure Gemini
GEMINI_API_KEY = "AIzaSyDVW4vPFJ7frbYhklDgKoaE9-3CEka5Hpg"
genai.configure(api_key='AIzaSyDVW4vPFJ7frbYhklDgKoaE9-3CEka5Hpg')

def ask_gemini(text, system_name):
    """Ask Gemini to simulate different verification systems"""
    try:
        model_name = "gemini-1.5-flash-latest"  # Pick any available model
        model = genai.GenerativeModel(model_name)  # Corrected the argument
        prompt = f"""
        Act as {system_name} fact verification system. Analyze this text and return ONLY one word:
        - 'TRUE' if the information appears accurate
        - 'FALSE' if the information appears inaccurate
        - 'MIXTURE' if it contains both true and false elements
        
        Text: {text}
        """
        response = model.generate_content(prompt)
        return response.text.strip().upper()
    except Exception as e:
        print(f"Gemini Error ({system_name}): {str(e)}")
        return "ERROR"

@csrf_protect
def home(request):
    context = {
        'verichain_result': None,
        'neuralink_result': None,
        'quantum_result': None,
        'deepscan_result': None,
        'cognix_result': None,
        'summary': None,
        'input_text': None
    }
    
    if request.method == 'POST':
        input_text = request.POST.get('fact_input', '')
        if input_text:
            # Get results from Gemini simulating all 5 systems
            context['verichain_result'] = ask_gemini(input_text, "VeriChain Core")
            context['neuralink_result'] = ask_gemini(input_text, "Neuralink AI") 
            context['quantum_result'] = ask_gemini(input_text, "Quantum Validator")
            context['deepscan_result'] = ask_gemini(input_text, "DeepScan")
            context['cognix_result'] = ask_gemini(input_text, "Cognix Network")
            context['input_text'] = input_text
            
            model_name = "gemini-1.5-flash-latest"  # Pick any available model
            model = genai.GenerativeModel(model_name)  # Corrected the argument
            summary_prompt = f"""
            Based on these verification results from our AI network:
            - VeriChain Core: {context['verichain_result']}
            - Neuralink AI: {context['neuralink_result']}
            - Quantum Validator: {context['quantum_result']}
            - DeepScan: {context['deepscan_result']}
            - Cognix Network: {context['cognix_result']}
            
            For this claim: "{input_text[:200]}..."
            
            Provide a concise 2-3 sentence summary analysis in simple language.
            """
            context['summary'] = model.generate_content(summary_prompt).text
    
    return render(request, 'index.html', context)