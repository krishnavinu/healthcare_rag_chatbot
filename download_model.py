"""
Download and cache google/flan-t5-base locally (~1 GB).

Optional — app_local.py downloads automatically on first run.

    python download_model.py
"""

from college_chatbot import DEFAULT_MODEL_ID


def main():
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    print(f"Downloading and caching: {DEFAULT_MODEL_ID}")
    print("This may take several minutes depending on your internet speed.\n")

    AutoTokenizer.from_pretrained(DEFAULT_MODEL_ID)
    AutoModelForSeq2SeqLM.from_pretrained(DEFAULT_MODEL_ID)

    print("\nDone. The model is cached and ready.")
    print("Run:  streamlit run app_local.py")


if __name__ == "__main__":
    main()
