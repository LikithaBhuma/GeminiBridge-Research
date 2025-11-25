from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import json
import random
import re
import os
from collections import Counter
import pandas as pd
from googletrans import Translator

from sklearn.metrics import classification_report as sk_report
from seqeval.metrics import classification_report as seq_report
from test_data import test_cases
import warnings

app = Flask(__name__)

# Configure Gemini AI
genai.configure(api_key="AIzaSyD6MXGpHqsJG7qg9gssgvNBGZIQ2tXXfk0")
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

# Language codes and data path
LANG_CODES = ['ES', 'TH', 'FA', 'BN','TE']
DATA_PATH = "data"

# Language mapping
LANGUAGES = {
    'english': {'name': 'English', 'code': 'EN'},
    'spanish': {'name': 'Spanish', 'code': 'ES'},
    'persian': {'name': 'Persian', 'code': 'FA'},
    'thai': {'name': 'Thai', 'code': 'TH'},
    'bengali': {'name': 'Bengali', 'code': 'BN'},
    'telugu': {'name': 'Telugu', 'code': 'TE'}
}

# Example datasets for different languages
example_datasets = {
    "english": {
        "alarm": [
            {
                "utterance": "Set an alarm for 7 AM tomorrow",
                "intent": "alarm/set",
                "slots": {"time": "7 AM", "date": "tomorrow"}
            },
            {
                "utterance": "Wake me up at 6",
                "intent": "alarm/set",
                "slots": {"time": "6"}
            }
        ],
        "reminder": [
            {
                "utterance": "Remind me to call mom at 5 PM",
                "intent": "reminder/set",
                "slots": {"task": "call mom", "time": "5 PM"}
            },
            {
                "utterance": "Schedule a meeting at 3 PM",
                "intent": "reminder/set",
                "slots": {"task": "meeting", "time": "3 PM"}
            }
        ]
    },
    "spanish": {
        "alarm": [
            {
                "utterance": "Configura una alarma para mañana a las 7 AM",
                "intent": "alarm/set",
                "slots": {"time": "7 AM", "date": "mañana"}
            },
            {
                "utterance": "Despiértame a las 6",
                "intent": "alarm/set",
                "slots": {"time": "6"}
            }
        ],
        "reminder": [
            {
                "utterance": "Recuérdame llamar a mamá a las 5 PM",
                "intent": "reminder/set",
                "slots": {"task": "llamar a mamá", "time": "5 PM"}
            },
            {
                "utterance": "Programa una reunión a las 3 PM",
                "intent": "reminder/set",
                "slots": {"task": "reunión", "time": "3 PM"}
            }
        ]
    },
    "persian": {
        "alarm": [
            {
                "utterance": "ساعت را برای ساعت ۷ صبح فردا تنظیم کن",
                "intent": "alarm/set",
                "slots": {"time": "۷ صبح", "date": "فردا"}
            },
            {
                "utterance": "من را ساعت ۶ بیدار کن",
                "intent": "alarm/set",
                "slots": {"time": "۶"}
            }
        ],
        "reminder": [
            {
                "utterance": "یادآوری کن که به مامان زنگ بزنم ساعت ۵ عصر",
                "intent": "reminder/set",
                "slots": {"task": "به مامان زنگ بزنم", "time": "۵ عصر"}
            },
            {
                "utterance": "جلسه‌ای را برای ساعت ۳ برنامه‌ریزی کن",
                "intent": "reminder/set",
                "slots": {"task": "جلسه‌ای", "time": "۳"}
            }
        ]
    },
    "thai": {
        "alarm": [
            {
                "utterance": "ตั้งนาฬิกาปลุกสำหรับพรุ่งนี้ตอน 7 โมงเช้า",
                "intent": "alarm/set",
                "slots": {"time": "7 โมงเช้า", "date": "พรุ่งนี้"}
            },
            {
                "utterance": "ปลุกฉันตอน 6 โมง",
                "intent": "alarm/set",
                "slots": {"time": "6 โมง"}
            }
        ],
        "reminder": [
            {
                "utterance": "เตือนฉันให้โทรหาคุณแม่ตอน 5 โมงเย็น",
                "intent": "reminder/set",
                "slots": {"task": "โทรหาคุณแม่", "time": "5 โมงเย็น"}
            },
            {
                "utterance": "ตั้งเตือนความจำให้ไปประชุมเวลา 3 โมง",
                "intent": "reminder/set",
                "slots": {"task": "ไปประชุม", "time": "3 โมง"}
            }
        ]
    },
    "bengali": {
        "alarm": [
            {
                "utterance": "আগামীকাল সকাল ৭টায় একটি অ্যালার্ম সেট করো",
                "intent": "alarm/set",
                "slots": {"time": "সকাল ৭টা", "date": "আগামীকাল"}
            },
            {
                "utterance": "আমাকে সকাল ৬টায় জাগাও",
                "intent": "alarm/set",
                "slots": {"time": "সকাল ৬টা"}
            }
        ],
        "reminder": [
            {
                "utterance": "আমাকে বিকেল ৫টায় মাকে ফোন করার কথা মনে করিয়ে দাও",
                "intent": "reminder/set",
                "slots": {"task": "মাকে ফোন করার কথা", "time": "বিকেল ৫টা"}
            },
            {
                "utterance": "বিকেল ৩টায় একটি মিটিং নির্ধারণ করো",
                "intent": "reminder/set",
                "slots": {"task": "মিটিং", "time": "বিকেল ৩টা"}
            }
        ]
    },
    "telugu": {
        "alarm": [
            {
                "utterance": "రేపు ఉదయం 7 గంటలకు అలారం సెట్ చేయండి",
                "intent": "alarm/set",
                "slots": {"time": "7 గంటలు", "date": "రేపు"}
            },
            {
                "utterance": "నన్ను 6 గంటలకు మేల్కొలపండి",
                "intent": "alarm/set",
                "slots": {"time": "6 గంటలు"}
            }
        ],
        "reminder": [
            {
                "utterance": "మధ్యాహ్నం 5 గంటలకు అమ్మకు ఫోన్ చేయమని నాకు గుర్తు చేయండి",
                "intent": "reminder/set",
                "slots": {"task": "అమ్మకు ఫోన్ చేయడం", "time": "5 గంటలు"}
            },
            {
                "utterance": "మధ్యాహ్నం 3 గంటలకు సమావేశం ఏర్పాటు చేయండి",
                "intent": "reminder/set",
                "slots": {"task": "సమావేశం", "time": "3 గంటలు"}
            }
        ]
    }
}

def run_gemini_prompt(prompt):
    """Run a prompt through Gemini AI"""
    try:
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        return f"[ERROR] Gemini response failed: {e}"

def format_few_shot_prompt(examples, new_utterance, task="intent"):
    """Format few-shot prompt for intent detection or slot filling"""
    prompt = ""

    if task == "intent":
        prompt += "You are an intent detection model. Identify the user's intent from their utterance.\n\n"
        for ex in examples:
            prompt += f"Utterance: {ex['utterance']}\nIntent: {ex['intent']}\n\n"
        prompt += f"Utterance: {new_utterance}\nIntent:"

    elif task == "slot":
        prompt += "You are a slot filling model. For each word in the utterance, assign a slot label.\n"
        prompt += "Use JSON format like: [{\"word\": \"Wake\", \"slot\": \"O\"}, ...]\n\n"
        for ex in examples:
            prompt += f"Utterance: {ex['utterance']}\nSlots: [\n"
            for word in ex["utterance"].split():
                matched = False
                for slot, value in ex["slots"].items():
                    if value in word:
                        prompt += f"  {{\"word\": \"{word}\", \"slot\": \"{slot}\"}},\n"
                        matched = True
                        break
                if not matched:
                    prompt += f"  {{\"word\": \"{word}\", \"slot\": \"O\"}},\n"
            prompt = prompt.rstrip(",\n") + "\n]\n\n"
        prompt += f"Utterance: {new_utterance}\nSlots:"

    return prompt.strip()

def detect_intent(utterance, language, domain="reminder"):
    """Detect intent using few-shot prompting"""
    examples = example_datasets.get(language, {}).get(domain, [])[:3]
    if not examples:
        examples = example_datasets["english"].get(domain, [])[:3]
    
    prompt = format_few_shot_prompt(examples, utterance, task="intent")
    return run_gemini_prompt(prompt)

def fill_slots(utterance, language, domain="reminder"):
    """Fill slots using few-shot prompting"""
    examples = example_datasets.get(language, {}).get(domain, [])[:3]
    if not examples:
        examples = example_datasets["english"].get(domain, [])[:3]
    
    prompt = format_few_shot_prompt(examples, utterance, task="slot")
    output = run_gemini_prompt(prompt)

    # Try to extract JSON output
    try:
        match = re.search(r'\[\s*{.*?}\s*\]', output, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass
    return {"raw_output": output}

def translate_to_english(text, language, task="intent or slot labels"):
    """Translate results to English"""
    if language == "english":
        return text
    
    instruction = f"Translate the following {task} from {language} to English:\n{text}"
    return run_gemini_prompt(instruction)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', languages=LANGUAGES)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze text for intent and slots"""
    try:
        data = request.get_json()
        utterance = data.get('utterance', '').strip()
        language = data.get('language', 'english')
        domain = data.get('domain', 'reminder')

        if not utterance:
            return jsonify({'success': False, 'error': 'No utterance provided'})

        # Translate utterance to selected language (if not English)
        lang_code = LANGUAGES.get(language, {}).get('code', 'EN').lower()
        translated_utterance = utterance
        if lang_code != 'en':
            translator = Translator()
            try:
                translated = translator.translate(utterance, dest=lang_code)
                translated_utterance = translated.text
            except Exception as e:
                translated_utterance = f"[Translation error: {str(e)}]"

        # Always translate utterance to the selected language for the translation field, even if selected language is English
        translator = Translator()
        try:
            translated_utterance_selected_lang = translator.translate(utterance, dest=lang_code).text
        except Exception as e:
            translated_utterance_selected_lang = f"[Translation error: {str(e)}]"

        # Detect intent
        intent_result = detect_intent(utterance, language, domain)
        intent_translation = translate_to_english(intent_result, language, "intent")

        # Fill slots
        slots_result = fill_slots(utterance, language, domain)
        slots_text = slots_result if isinstance(slots_result, str) else json.dumps(slots_result, ensure_ascii=False)
        # For translation, join the words into a sentence if possible
        if isinstance(slots_result, list):
            slot_words = [item['word'] for item in slots_result if 'word' in item]
            slot_sentence = ' '.join(slot_words)
        else:
            slot_sentence = str(slots_result)
        slots_translation = translate_to_english(slot_sentence, language, "slot labels")

        return jsonify({
            'success': True,
            'results': {
                'intent': {
                    'original': intent_result,
                    'translation': intent_translation
                },
                'slots': {
                    'original': slots_result,
                    'translation': slots_translation
                }
            },
            'translated_utterance': translated_utterance,
            'translated_utterance_selected_lang': translated_utterance_selected_lang
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/examples/<language>')
def get_examples(language):
    """Get example utterances for a language"""
    try:
        examples = example_datasets.get(language, {})
        return jsonify(examples)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Multilingual Language Understanding API is running'})

@app.route('/evaluate-metrics-ui', methods=['GET'])
def evaluate_metrics_ui():
    language = request.args.get('language', 'english').lower()
    warnings.filterwarnings("ignore")

    y_true_intents = []
    y_pred_intents = []
    y_true_slots = []
    y_pred_slots = []

    def convert_to_bio(predicted_slots, utterance):
        words = utterance.split()
        bio_tags = []
        for word in words:
            tag = "O"
            for slot in predicted_slots:
                if slot.get("word") == word:
                    label = slot.get("slot", "O")
                    if label == "O":
                        tag = "O"
                    elif not bio_tags or bio_tags[-1][2:] != label:
                        tag = f"B-{label}"
                    else:
                        tag = f"I-{label}"
                    break
            bio_tags.append(tag)
        return bio_tags

    for case in test_cases:
        utterance = case["utterance"]
        expected_intent = case["expected_intent"]
        expected_slots_seq = case["expected_slots_seq"]

        predicted_intent = detect_intent(utterance, language, "reminder")
        predicted_intent = predicted_intent.replace("Intent:", "").strip()
        y_true_intents.append(expected_intent)
        y_pred_intents.append(predicted_intent)

        predicted_slots_raw = fill_slots(utterance, language, "reminder")

        if isinstance(predicted_slots_raw, list):
            predicted_bio = convert_to_bio(predicted_slots_raw, utterance)
        else:
            predicted_bio = ["O"] * len(expected_slots_seq)

        while len(predicted_bio) < len(expected_slots_seq):
            predicted_bio.append("O")
        while len(predicted_bio) > len(expected_slots_seq):
            predicted_bio = predicted_bio[:len(expected_slots_seq)]

        y_true_slots.append(expected_slots_seq)
        y_pred_slots.append(predicted_bio)

    intent_report = sk_report(y_true_intents, y_pred_intents, digits=3, zero_division=0, output_dict=True)
    slot_report = seq_report(y_true_slots, y_pred_slots, digits=3, output_dict=True)

    return jsonify({
        "success": True,
        "language": language,
        "intent_report": intent_report,
        "slot_report": slot_report
    })

if __name__ == '__main__':
    print("🚀 Starting Multilingual Language Understanding Interface...")
    print("📝 Supported Languages: English, Spanish, Persian, Thai, Bengali, Telugu")
    print("🎯 Supported Domains: Reminder, Alarm")
    print("🌐 Interface will be available at: http://localhost:5000")
    print("🔗 Health check: http://localhost:5000/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 