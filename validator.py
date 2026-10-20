MAX_TITLE_LENGTH = 100


def validate_title(title):
    """Memastikan judul tugas tidak kosong dan tidak terlalu panjang."""
    if title is None:
        raise ValueError("Judul tugas tidak boleh kosong.")
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("Judul tugas tidak boleh kosong.")
    if len(cleaned) > MAX_TITLE_LENGTH:
        raise ValueError(
            f"Judul tugas maksimal {MAX_TITLE_LENGTH} karakter."
        )
    return cleaned


def validate_id(value):
    """Memastikan ID berupa angka bulat positif."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError("ID harus berupa angka.")
    if number <= 0:
        raise ValueError("ID harus lebih besar dari 0.")
    return number