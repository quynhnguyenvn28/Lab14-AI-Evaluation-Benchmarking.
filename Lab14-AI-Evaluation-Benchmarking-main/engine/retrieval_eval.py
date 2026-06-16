import re
import unicodedata
from typing import Dict, List


def _normalize(value: str) -> str:
    value = unicodedata.normalize("NFD", value.lower())
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return value.replace("đ", "d")


def _tokens(value: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", _normalize(value))


class RetrievalEvaluator:
    def calculate_hit_rate(self, expected_ids: List[str], retrieved_ids: List[str], top_k: int = 3) -> float:
        if not expected_ids:
            return 1.0
        top_retrieved = retrieved_ids[:top_k]
        hit = any(doc_id in top_retrieved for doc_id in expected_ids)
        return 1.0 if hit else 0.0

    def calculate_mrr(self, expected_ids: List[str], retrieved_ids: List[str]) -> float:
        if not expected_ids:
            return 1.0
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in expected_ids:
                return 1.0 / (i + 1)
        return 0.0

    def _lexical_overlap(self, expected_answer: str, answer: str) -> float:
        expected = set(_tokens(expected_answer))
        actual = set(_tokens(answer))
        if not expected:
            return 1.0
        return len(expected & actual) / len(expected)

    async def score(self, case: Dict, response: Dict) -> Dict:
        expected_ids = case.get("expected_retrieval_ids", [])
        retrieved_ids = response.get("retrieved_ids", [])
        contexts = response.get("contexts", [])
        answer = response.get("answer", "")

        hit_rate = self.calculate_hit_rate(expected_ids, retrieved_ids, top_k=3)
        mrr = self.calculate_mrr(expected_ids, retrieved_ids)
        answer_overlap = self._lexical_overlap(case.get("expected_answer", ""), answer)

        if expected_ids:
            faithfulness = 1.0 if any(doc_id in retrieved_ids for doc_id in expected_ids) else 0.35
            faithfulness = min(1.0, faithfulness * (0.65 + 0.35 * answer_overlap))
        else:
            safe_unknown = any(
                phrase in _normalize(answer)
                for phrase in ["khong tim thay", "thieu ngu canh", "khong cung cap", "noi ro"]
            )
            faithfulness = 1.0 if safe_unknown else 0.4

        question_tokens = set(_tokens(case.get("question", "")))
        context_tokens = set(_tokens(" ".join(contexts)))
        relevancy = len(question_tokens & context_tokens) / max(len(question_tokens), 1)
        if not expected_ids and faithfulness == 1.0:
            relevancy = 1.0

        return {
            "faithfulness": round(faithfulness, 4),
            "relevancy": round(min(1.0, relevancy), 4),
            "answer_overlap": round(answer_overlap, 4),
            "retrieval": {
                "hit_rate": hit_rate,
                "mrr": round(mrr, 4),
                "expected_ids": expected_ids,
                "retrieved_ids": retrieved_ids,
                "not_applicable": not bool(expected_ids),
            },
        }

    async def evaluate_batch(self, results: List[Dict]) -> Dict:
        if not results:
            return {"avg_hit_rate": 0.0, "avg_mrr": 0.0}

        retrieval_cases = [
            result for result in results if not result["ragas"]["retrieval"].get("not_applicable", False)
        ]
        denominator = len(retrieval_cases) or 1
        return {
            "avg_hit_rate": sum(r["ragas"]["retrieval"]["hit_rate"] for r in retrieval_cases) / denominator,
            "avg_mrr": sum(r["ragas"]["retrieval"]["mrr"] for r in retrieval_cases) / denominator,
            "retrieval_case_count": len(retrieval_cases),
        }
