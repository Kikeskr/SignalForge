"""Evidence capture, structured field extraction, and stable source deduplication."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import UTC, datetime

from signalforge.fetch import canonicalize_url
from signalforge.search import SearchResult

PRIMARY_DOMAINS = (
    "arxiv.org",
    "openreview.net",
    "biorxiv.org",
    "medrxiv.org",
    "nature.com",
    "science.org",
    "acm.org",
    "ieee.org",
    "doi.org",
    "semanticscholar.org",
    "python.org",
    "peps.python.org",
    "docs.python.org",
    "github.com",
    "w3.org",
    "ietf.org",
    "iso.org",
)

QUANTITATIVE_PATTERNS = (
    r"\b(?:\+|\-)?\d+(?:\.\d+)?%\s*(?:faster|slower|speedup|improvement|reduction|increase|decrease|overhead|latency reduction|accuracy|throughput|gain|drop|boost)?\b",
    r"\b\d+(?:\.\d+)?x\s*(?:faster|speedup|improvement|throughput|more|gain)\b",
    r"\b(?:speedup of|improvement of|reduced by|increased by|latency of|overhead of)\s*[\w\s.%-]{1,40}\b",
    r"\b\d+(?:\.\d+)?\s*(?:ms|milliseconds|seconds|µs|microseconds|ns|nanoseconds)\b",
    r"\bp\s*[<=]\s*0\.\d+\b",
)

SAMPLE_SIZE_PATTERNS = (
    r"\b(?:n\s*=\s*|sample size of\s*|sample of\s*|cohort of\s*|evaluated on\s*|tested on\s*|across\s*|benchmark suite of\s*)([\d,]+(?:\s*(?:distinct\s+|different\s+)?(?:pyperformance\s+|standard\s+)?(?:benchmarks|workloads|samples|participants|subjects|cases|runs|iterations|examples|models|prompts|queries|tasks|trials))?)\b",
    r"\b([\d,]+)\s+(?:distinct\s+|different\s+)?(?:pyperformance\s+|standard\s+)?(?:benchmarks|workloads|participants|subjects|iterations|trials|runs|evaluated prompts|test cases|microbenchmarks)\b",
)

DATE_PATTERNS = (
    r"\b(20\d{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))\b",
    r"\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+20\d{2})\b",
    r"\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+20\d{2})\b",
    r"\barXiv:\d{2}(\d{2})\.\d+",
)

UNCERTAINTY_PATTERNS = (
    r"\b(?:uncertain|unclear|inconclusive|preliminary|conflicting reports|debated|unproven|speculative|yet to be determined|remains to be seen)\b",
)

LIMITATION_PATTERNS = (
    r"\b(?:limitations?:?|caveats?:?|threats to validity:?)\s*([^.!?\n]+[.!?]?)",
    r"\b(?:restricted to|does not account for|preliminary results?|potential bias|small sample|synthetic benchmark|only tested on|requires further verification)\b[^.!?\n]*",
)


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    title: str
    url: str
    retrieved_at: str
    excerpt: str
    publication_date: str | None = None
    source_type: str = "secondary"
    sample_size: str | None = None
    methodology: str | None = None
    measured_outcome: str | None = None
    limitations: tuple[str, ...] = ()
    evidence_strength: str = "moderate"

    def __post_init__(self) -> None:
        if isinstance(self.limitations, list):
            object.__setattr__(self, "limitations", tuple(self.limitations))


def detect_source_type(url: str, text: str) -> str:
    domain_match = re.findall(r"https?://([^/:]+)", url.lower())
    if domain_match:
        host = domain_match[0]
        if any(host == d or host.endswith("." + d) for d in PRIMARY_DOMAINS):
            return "primary"
    lower = text.lower()
    if re.search(r"\bdoi:\s*10\.\d{4,9}/", lower) or re.search(r"\barxiv:\s*\d{4}\.\d{4,5}", lower):
        return "primary"
    if re.search(r"\bpep\s+\d{3,4}\b", lower) and ("abstract" in lower or "specification" in lower):
        return "primary"
    if "abstract" in lower and any(sec in lower for sec in ["methodology", "experimental setup", "benchmark results", "evaluation"]):
        return "primary"
    return "secondary"


def extract_publication_date(text: str) -> str | None:
    for pat in DATE_PATTERNS:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def extract_sample_size(text: str) -> str | None:
    for pat in SAMPLE_SIZE_PATTERNS:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return None


def extract_methodology(text: str) -> str | None:
    lower = text.lower()
    if any(k in lower for k in ["pyperformance", "benchmark suite", "benchmarking", "microbenchmark", "latency test", "throughput test", "execution time measured"]):
        return "Empirical benchmark evaluation"
    if any(k in lower for k in ["randomized controlled", "control group", "a/b test", "double-blind"]):
        return "Randomized controlled trial"
    if any(k in lower for k in ["pep ", "specification", "rfc ", "standard library documentation", "official release notes", "language reference"]):
        return "Official specification & documentation"
    if any(k in lower for k in ["survey", "questionnaire", "interviews", "observational cohort", "qualitative study"]):
        return "Observational study / survey"
    if any(k in lower for k in ["formal proof", "theorem", "algorithmic complexity", "theoretical analysis"]):
        return "Theoretical / formal analysis"
    return None


def extract_measured_outcome(text: str) -> str | None:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]
    for sentence in sentences:
        for pat in QUANTITATIVE_PATTERNS:
            match = re.search(pat, sentence, re.IGNORECASE)
            if match:
                return sentence[:200].strip()
    return None


def detect_uncertainty(text: str) -> bool:
    return any(re.search(pat, text, re.IGNORECASE) for pat in UNCERTAINTY_PATTERNS)


def extract_limitations(text: str, has_quantitative: bool = True) -> tuple[str, ...]:
    limits: list[str] = []
    if not has_quantitative:
        limits.append("Missing quantitative details or sample size")
    for pat in LIMITATION_PATTERNS:
        matches = re.finditer(pat, text, re.IGNORECASE)
        for m in matches:
            phrase = m.group(0).strip()[:150]
            if phrase and phrase not in limits:
                limits.append(phrase)
    return tuple(limits[:3])


def evaluate_evidence_strength(
    source_type: str,
    has_outcome: bool,
    has_sample: bool,
    has_methodology: bool,
    is_uncertain: bool = False,
    is_weak_signal: bool = False,
) -> str:
    if is_weak_signal:
        return "unsupported"
    if is_uncertain:
        return "weak"
    if source_type == "primary" and has_outcome and (has_sample or has_methodology):
        return "strong"
    if has_outcome or (source_type == "primary" and has_methodology):
        return "moderate"
    if not has_outcome and not has_sample:
        return "weak"
    return "moderate"


def select_excerpt(text: str, query: str, is_primary: bool = False) -> str:
    """Pick a bounded paragraph with query-term overlap and quantitative details for primary papers."""
    chunks = [re.sub(r"\s+", " ", part).strip() for part in re.split(r"\n+|(?<=[.!?])\s+", text)]
    chunks = [part for part in chunks if len(part) >= 60]
    terms = {word.lower() for word in re.findall(r"\d+(?:\.\d+)+|[a-zA-Z][\w'-]{2,}", query)}
    if not chunks:
        return text.strip()[:1200]

    def score_chunk(part: str) -> int:
        part_lower = part.lower()
        score = sum(word in part_lower for word in terms)
        if is_primary:
            has_quant = any(re.search(p, part, re.IGNORECASE) for p in QUANTITATIVE_PATTERNS)
            if has_quant:
                score += 5
            if any(k in part_lower for k in ["benchmark", "results", "evaluation", "measured", "pyperformance", "speedup"]):
                score += 3
            if part_lower.startswith(("abstract:", "in this paper")):
                score -= 2
        return score

    return max(chunks, key=score_chunk)[:1200]


def make_evidence(result: SearchResult, text: str, retrieved_at: str | None = None,
                  query: str = "") -> Evidence:
    url = canonicalize_url(result.url)
    evidence_id = "E-" + hashlib.sha256(url.encode()).hexdigest()[:10].upper()
    source_type = detect_source_type(url, text)
    excerpt = (select_excerpt(text, query, is_primary=(source_type == "primary")) or result.snippet).strip()[:1200]
    pub_date = extract_publication_date(excerpt) or extract_publication_date(text)
    sample_size = extract_sample_size(excerpt) or extract_sample_size(text)
    methodology = extract_methodology(excerpt) or extract_methodology(text)
    measured_outcome = extract_measured_outcome(excerpt) or extract_measured_outcome(text)
    has_outcome = measured_outcome is not None
    has_sample = sample_size is not None
    has_method = methodology is not None
    is_uncertain = detect_uncertainty(excerpt)
    limitations = extract_limitations(excerpt, has_quantitative=has_outcome)
    strength = evaluate_evidence_strength(source_type, has_outcome, has_sample, has_method, is_uncertain=is_uncertain)
    return Evidence(
        evidence_id=evidence_id,
        title=result.title.strip() or url,
        url=url,
        retrieved_at=retrieved_at or datetime.now(UTC).isoformat(),
        excerpt=excerpt,
        publication_date=pub_date,
        source_type=source_type,
        sample_size=sample_size,
        methodology=methodology,
        measured_outcome=measured_outcome,
        limitations=limitations,
        evidence_strength=strength,
    )


def deduplicate(results: list[SearchResult]) -> list[SearchResult]:
    seen: set[str] = set()
    unique: list[SearchResult] = []
    for result in results:
        try:
            url = canonicalize_url(result.url)
        except ValueError:
            continue
        if url not in seen:
            seen.add(url)
            unique.append(SearchResult(result.title, url, result.snippet))
    return unique
