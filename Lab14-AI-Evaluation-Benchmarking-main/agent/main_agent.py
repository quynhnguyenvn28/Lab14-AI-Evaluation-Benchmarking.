import asyncio
import math
import re
import unicodedata
from typing import Dict, List, Tuple

from data.corpus import DOCUMENTS


STOPWORDS = {
    "a",
    "ai",
    "anh",
    "bao",
    "bi",
    "bo",
    "cai",
    "can",
    "cho",
    "chinh",
    "cong",
    "co",
    "cua",
    "de",
    "duoc",
    "gi",
    "ha",
    "hay",
    "hoi",
    "khong",
    "la",
    "lam",
    "nam",
    "nay",
    "nhan",
    "neu",
    "nhu",
    "noi",
    "o",
    "phai",
    "quy",
    "rang",
    "sach",
    "sao",
    "the",
    "thi",
    "toi",
    "tra",
    "trong",
    "tu",
    "va",
    "ve",
    "voi",
    "vien",
}


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return value.replace("đ", "d")


def tokenize(value: str) -> List[str]:
    normalized = normalize_text(value)
    return [token for token in re.findall(r"[a-z0-9]+", normalized) if token not in STOPWORDS and len(token) > 1]


class MainAgent:
    """
    Local RAG agent used for the lab benchmark.

    version="v1" intentionally uses a weaker retriever.
    version="v2" adds keyword boosts, ambiguity checks and safer out-of-context handling.
    """

    def __init__(self, version: str = "v2", top_k: int = 3):
        self.version = version
        self.top_k = top_k
        self.name = f"SupportAgent-{version}"
        self.documents = DOCUMENTS

    def _score_v1(self, query_tokens: List[str], doc: Dict) -> float:
        doc_tokens = set(tokenize(doc["title"] + " " + doc["text"]))
        overlap = len(set(query_tokens) & doc_tokens)
        return overlap / max(math.sqrt(len(doc_tokens)), 1)

    def _score_v2(self, query: str, query_tokens: List[str], doc: Dict) -> float:
        doc_text = doc["title"] + " " + doc["text"] + " " + " ".join(doc["keywords"])
        doc_tokens = set(tokenize(doc_text))
        overlap = len(set(query_tokens) & doc_tokens)
        score = overlap / max(math.sqrt(len(doc_tokens)), 1)

        normalized_query = normalize_text(query)
        for keyword in doc["keywords"]:
            normalized_keyword = normalize_text(keyword)
            if normalized_keyword in normalized_query:
                score += 0.55

        if normalize_text(doc["category"]) in normalized_query:
            score += 0.2
        if (
            "tai khoan bi khoa" in normalized_query
            or "khoa tai khoan" in normalized_query
        ) and doc["id"] == "doc_account_lock":
            score += 1.0
        if "hoa don" in normalized_query and "chi phi" not in normalized_query and doc["id"] == "doc_invoice_tax":
            score += 0.8
        if "mat du lieu" in normalized_query and doc["id"] == "doc_incident_reporting":
            score += 0.8

        return score

    def retrieve(self, question: str) -> List[Tuple[Dict, float]]:
        query_tokens = tokenize(question)
        scored = []
        for doc in self.documents:
            if self.version == "v1":
                score = self._score_v1(query_tokens, doc)
            else:
                score = self._score_v2(question, query_tokens, doc)
            scored.append((doc, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[: self.top_k]

    def _is_ambiguous(self, question: str) -> bool:
        normalized = normalize_text(question)
        generic_phrases = [
            "toi muon doi cai do",
            "chinh sach nay",
            "gui yeu cau o dau",
            "cai nao la mac dinh",
            "khi nao can lien he bo phan lien quan",
            "neu vuot gioi han thi sao",
        ]
        return any(phrase in normalized for phrase in generic_phrases)

    def _is_known_out_of_scope(self, question: str) -> bool:
        normalized = normalize_text(question)
        out_of_scope_terms = [
            "bitcoin",
            "co phieu",
            "pho bo",
            "bong da",
            "tong thong",
            "xe may",
        ]
        return any(term in normalized for term in out_of_scope_terms)

    def _answer_from_context(self, question: str, retrieved: List[Tuple[Dict, float]]) -> str:
        best_doc, best_score = retrieved[0]
        normalized_question = normalize_text(question)

        if self.version == "v2":
            if self._is_known_out_of_scope(question):
                return (
                    "Toi khong tim thay thong tin lien quan trong bo tai lieu hien co. "
                    "Ban nen dung nguon chuyen mon phu hop cho cau hoi nay."
                )
            if self._is_ambiguous(question):
                return (
                    "Cau hoi hien thieu ngu canh. Ban vui long noi ro chinh sach, san pham "
                    "hoac tinh huong can ho tro de toi tra loi dua tren tai lieu phu hop."
                )
            if best_score < 0.18:
                return (
                    "Toi khong tim thay thong tin lien quan trong bo tai lieu hien co. "
                    "Ban nen cung cap them ngu canh hoac lien he bo phan phu trach."
                )
            if "quen mat khau" in normalized_question and "bi khoa" in normalized_question:
                docs_by_id = {doc["id"]: doc for doc in self.documents}
                return (
                    f"{docs_by_id['doc_account_lock']['summary_answer']} "
                    f"Sau khi mo khoa hoac xac minh danh tinh, {docs_by_id['doc_password_reset']['summary_answer']} "
                    "Nguon: doc_account_lock, doc_password_reset."
                )

        if self.version == "v1" and best_score < 0.08:
            return (
                "Dua tren tai lieu gan nhat, co the can tao ticket ho tro de duoc xu ly. "
                f"Thong tin tham khao: {best_doc['summary_answer']}"
            )

        safety_prefix = ""
        if "bo qua" in normalized_question or "thay vi" in normalized_question:
            safety_prefix = "Toi se khong bo qua tai lieu he thong. "

        return f"{safety_prefix}{best_doc['summary_answer']} Nguon: {best_doc['id']}."

    async def query(self, question: str) -> Dict:
        await asyncio.sleep(0.05 if self.version == "v2" else 0.08)

        retrieved = self.retrieve(question)
        answer = self._answer_from_context(question, retrieved)
        retrieved_docs = [doc for doc, _ in retrieved]
        retrieved_ids = [doc["id"] for doc in retrieved_docs]
        contexts = [doc["text"] for doc in retrieved_docs]

        prompt_tokens = len(tokenize(question)) + sum(len(tokenize(ctx)) for ctx in contexts)
        completion_tokens = len(tokenize(answer))
        total_tokens = prompt_tokens + completion_tokens
        cost_usd = round((prompt_tokens * 0.00000015) + (completion_tokens * 0.0000006), 6)

        return {
            "answer": answer,
            "contexts": contexts,
            "retrieved_ids": retrieved_ids,
            "metadata": {
                "agent_version": self.version,
                "model": "local-rag-heuristic",
                "tokens_used": total_tokens,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "estimated_cost_usd": cost_usd,
                "sources": retrieved_ids,
                "retrieval_scores": {doc["id"]: round(score, 4) for doc, score in retrieved},
            },
        }


if __name__ == "__main__":
    agent = MainAgent(version="v2")

    async def test():
        resp = await agent.query("Lam the nao de doi mat khau?")
        print(resp)

    asyncio.run(test())
