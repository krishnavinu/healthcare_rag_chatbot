"""
Optional: pre-download google/flan-t5-base (~1 GB).
app.py downloads automatically on first run if you skip this step.

    python download_model.py
"""

from healthcare_chatbot import DEFAULT_MODEL_ID


def main():
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    print(f"Downloading and caching: {DEFAULT_MODEL_ID}")
    print("This may take several minutes depending on your internet speed.\n")

    AutoTokenizer.from_pretrained(DEFAULT_MODEL_ID)
    AutoModelForSeq2SeqLM.from_pretrained(DEFAULT_MODEL_ID)

    print("\nDone. The model is cached and ready.")
    print("Run:  streamlit run app.py")


if __name__ == "__main__":
    main()
