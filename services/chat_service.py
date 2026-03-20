from rag.retriever import Retriever
from rag.generator import Generator
from rag.cache import QueryCache
from services.memory import UserMemory
from config import TOP_K
from utils.logger import log

retriever = Retriever()
generator = Generator()
cache = QueryCache()
memory = UserMemory()

log("Chat Service INITIALIZED ")


def handle_query(user_id, query):
    # Cache check
    cached = cache.get(query)
    if cached:
        log("Cache hit ")
        return cached

    retrieved = retriever.retrieve(query, TOP_K)

    if not retrieved:
        return ("I don't know", [])

    context = "\n".join([doc for doc, _ in retrieved])
    sources = list(set([name for _, name in retrieved]))

    history = memory.get_history(user_id)
    full_context = history + "\n" + context

    answer = generator.generate(query, full_context)

    memory.add(user_id, query, answer)

    result = (answer, sources)
    cache.set(query, result)

    return result


def summarize(user_id):
    last = memory.get_last_response(user_id)
    if not last:
        return "No previous response to summarize."

    return generator.summarize(last)