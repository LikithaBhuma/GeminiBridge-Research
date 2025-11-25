# test_data.py

# Format updated for classification metrics support
test_cases = [
    # English - Reminder
    {
        "utterance": "Remind me to call mom at 5 PM",
        "expected_intent": "reminder/set",
        "expected_slots_seq": ["O", "O", "O", "B-task", "I-task", "O", "B-time", "I-time"]
    },
    {
        "utterance": "Schedule a meeting at 3 PM",
        "expected_intent": "reminder/set",
        "expected_slots_seq": ["O", "O", "B-task", "O", "B-time", "I-time"]
    },

    # Spanish - Alarm
    {
        "utterance": "Despiértame a las 6",
        "expected_intent": "alarm/set",
        "expected_slots_seq": ["O", "O", "O", "B-time"]
    },

    # Persian - Reminder
    {
        "utterance": "یادآوری کن که به مامان زنگ بزنم ساعت ۵ عصر",
        "expected_intent": "reminder/set",
        "expected_slots_seq": ["O", "O", "O", "O", "B-task", "I-task", "O", "B-time", "I-time"]
    },

    # Thai - Alarm
    {
        "utterance": "ปลุกฉันตอน 6 โมง",
        "expected_intent": "alarm/set",
        "expected_slots_seq": ["O", "B-time", "I-time"]
    },

    # Bengali - Reminder
    {
        "utterance": "আমাকে বিকেল ৫টায় মাকে ফোন করার কথা মনে করিয়ে দাও",
        "expected_intent": "reminder/set",
        "expected_slots_seq": ["O", "B-time", "I-time", "B-task", "I-task", "I-task", "I-task", "O", "O", "O"]
    },

    # Telugu - Alarm
    {
        "utterance": "నన్ను 6 గంటలకు మేల్కొలపండి",
        "expected_intent": "alarm/set",
        "expected_slots_seq": ["O", "B-time", "I-time", "O"]
    }
]
