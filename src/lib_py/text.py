def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    text = text.casefold()
    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')
    text = text.replace('\t', ' ').replace('\r', ' ').replace('\n', ' ')
    text = ' '.join(text.split())
    text = text.strip()
    return text
import re 
def tokenize(text: str) -> list[str]:
    return re.findall(r'\w+(?:-\w+)*', text)
def count_freq(tokens: list[str]) -> dict[str, int]:
    c = {}  
    for w in tokens:
        cu = c.get(w, 0)
        c[w] = cu + 1
    return c
def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    t = []
    for w, count in freq.items():
        t.append((-count, w))
    t.sort()
    result = []
    for neg_count, w in t:
        result.append((w, -neg_count))
    return result[:n]
tok = ["a", "b", "a", "c", "b", "a"]
freq = count_freq(tok)
import sys

sys.path.append(r"C:\Users\eniko\Gitrep\python_labs\src\lib")

from text import (
    normalize,
    tokenize,
    count_freq,
    top_n,
)


def table(
    arr: list[
        tuple[
            str,
            int,
        ]
    ],
    isTable: bool = True,
) -> str:
    if not arr:
        return "(нет данных)"
    s = str()
    if isTable:
        word_col_width = max(
            len("слово"),
            max(len(a[0]) for a in arr),
        )
        freq_col_width = max(
            len("частота"),
            max(len(str(a[1])) for a in arr),
        )
        s += f"{'слово'.ljust(word_col_width)} | {'частота'.rjust(freq_col_width)}"
        s += "\n" + "-" * word_col_width + "-+-" + "-" * freq_col_width
        for (
            word,
            freq,
        ) in arr:
            s += f"\n{word.ljust(word_col_width)} | {str(freq).rjust(freq_col_width)}"
        return s
    else:
        return "\n".join(f"{a[0]}: {a[1]}" for a in arr)


def stats_text(
    text: str,
    n: int = 5,
):
    text = text.strip()
    tokens = normalize(text)
    tokens = tokenize(tokens)
    freqs = count_freq(tokens)
    total_words = len(tokens)
    unique_words = len(freqs)
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    top_n_words = sorted(
        freqs.items(),
        key=lambda x: (
            -x[1],
            x[0],
        ),
    )[:n]
    print(f"Топ-{n}:")
    print(
        table(
            top_n_words,
            True,
        )
    )