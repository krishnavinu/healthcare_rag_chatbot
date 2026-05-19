import os
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_DATA_PATH = Path(__file__).resolve().parent / "college_data.txt"
DEFAULT_MODEL_ID = "google/flan-t5-base"

PROMPT_TEMPLATE = """Answer the college-related question only using the context.
If the answer is not present, say:
"Information not available"

Context:
{context}

Question:
{query}
"""


def load_documents(data_path=None):
    """Load and split the college knowledge base into document chunks."""
    path = Path(data_path) if data_path else DEFAULT_DATA_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {path}\n"
            "Create college_data.txt in the project folder."
        )

    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    return [chunk.strip() for chunk in data.split("\n\n") if chunk.strip()]


def build_prompt(query: str, context: str) -> str:
    return PROMPT_TEMPLATE.format(context=context, query=query).strip()


class Retriever:
    def __init__(self, docs, top_k=2):
        self.docs = docs
        self.top_k = top_k

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.doc_vectors = self.vectorizer.fit_transform(docs)

    def retrieve(self, query):
        query_vector = self.vectorizer.transform([query])

        similarities = cosine_similarity(
            query_vector,
            self.doc_vectors,
        ).flatten()

        top_indices = similarities.argsort()[::-1][: self.top_k]

        return [self.docs[i] for i in top_indices]


class LocalGenerator:
    """Runs FLAN-T5 on your machine (downloads model on first use)."""

    def __init__(self, max_tokens=80, model_id=DEFAULT_MODEL_ID):
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.max_tokens = max_tokens
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    def generate(self, query, context):
        prompt = build_prompt(query, context)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=self.max_tokens)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


class APIGenerator:
    """Calls FLAN-T5 via Hugging Face Inference API (no local model download)."""

    def __init__(self, max_tokens=80, model_id=DEFAULT_MODEL_ID, token=None):
        from huggingface_hub import InferenceClient

        self.max_tokens = max_tokens
        self.model_id = model_id

        api_token = token or os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")
        if not api_token:
            raise ValueError(
                "Hugging Face API token not found. "
                "Set HF_TOKEN in a .env file or as an environment variable."
            )

        self.client = InferenceClient(model=model_id, token=api_token)

    def generate(self, query, context):
        prompt = build_prompt(query, context)

        return self.client.text_generation(
            prompt,
            max_new_tokens=self.max_tokens,
        )


class CollegeChatbot:
    def __init__(self, generator, documents=None, data_path=None, top_k=2):
        self.documents = documents if documents is not None else load_documents(data_path)
        self.retriever = Retriever(self.documents, top_k)
        self.generator = generator

    def chat(self, query, return_context=False):
        retrieved_docs = self.retriever.retrieve(query)
        context = "\n".join(retrieved_docs)
        response = self.generator.generate(query, context)

        if return_context:
            return response, retrieved_docs
        return response


def create_chatbot(mode="local", top_k=2, max_tokens=80, data_path=None, token=None):
    """Create a chatbot using either local or Hugging Face API generation."""
    mode = mode.lower().strip()
    documents = load_documents(data_path)

    if mode == "local":
        generator = LocalGenerator(max_tokens=max_tokens)
    elif mode in ("api", "hf", "huggingface"):
        generator = APIGenerator(max_tokens=max_tokens, token=token)
    else:
        raise ValueError("mode must be 'local' or 'api'")

    return CollegeChatbot(generator, documents=documents, top_k=top_k)
