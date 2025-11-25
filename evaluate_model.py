from test_data import test_cases
from app import detect_intent, fill_slots
from sklearn.metrics import classification_report as sk_report
from seqeval.metrics import classification_report as seq_report
import warnings

warnings.filterwarnings("ignore")

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

def evaluate_metrics(language="english"):
    y_true_intents = []
    y_pred_intents = []
    y_true_slots = []
    y_pred_slots = []

    for case in test_cases:
        utterance = case["utterance"]
        expected_intent = case["expected_intent"]
        expected_slots_seq = case["expected_slots_seq"]

        # INTENT EVALUATION
        predicted_intent = detect_intent(utterance, language, "reminder")
        predicted_intent = predicted_intent.replace("Intent:", "").strip()
        y_true_intents.append(expected_intent)
        y_pred_intents.append(predicted_intent)

        # SLOT EVALUATION
        predicted_slots_raw = fill_slots(utterance, language, "reminder")

        if isinstance(predicted_slots_raw, list):
            predicted_bio = convert_to_bio(predicted_slots_raw, utterance)
        else:
            predicted_bio = ["O"] * len(expected_slots_seq)

        # Adjust lengths
        while len(predicted_bio) < len(expected_slots_seq):
            predicted_bio.append("O")
        while len(predicted_bio) > len(expected_slots_seq):
            predicted_bio = predicted_bio[:len(expected_slots_seq)]

        y_true_slots.append(expected_slots_seq)
        y_pred_slots.append(predicted_bio)

        print("\nUtterance:", utterance)
        print("Expected Intent:", expected_intent, "| Predicted Intent:", predicted_intent)
        print("Expected Slots:", expected_slots_seq)
        print("Predicted Slots:", predicted_bio)

    print("\n\n🔍 Intent Classification Report:")
    print(sk_report(y_true_intents, y_pred_intents, digits=3, zero_division=0))

    print("\n🧩 Slot Filling Report:")
    print(seq_report(y_true_slots, y_pred_slots, digits=3))

# Optional CLI
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate Gemini AI intent/slot model")
    parser.add_argument("--language", type=str, default="english", help="Language to evaluate")
    args = parser.parse_args()
    evaluate_metrics(args.language.lower())
