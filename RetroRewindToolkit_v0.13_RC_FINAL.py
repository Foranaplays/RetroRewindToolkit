import os
import shutil
import base64
import tempfile
import re
import struct
import json
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

PATCH = base64.b64decode("""BgAAAFF1ZXN0AA4AAABBcnJheVByb3BlcnR5AAEAAAAPAAAAU3RydWN0UHJvcGVydHkAAgAAAA0AAABRdWVzdF9TdHJ1Y3QAAQAAADMAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1F1ZXN0X1N0cnVjdAAAAAAAJQAAADE3MTY2MTRlLTRjNzItZmI5Ni0xYzJlLWZkYWNlNTdhMGQ3MQAAAAAArgEAAAABAAAAJgAAAElEXzhfNDcyNjkzQkM0NDg2QTczNzM0REE0MEEwMzFBRTkzNTkADwAAAFN0cnVjdFByb3BlcnR5AAEAAAAFAAAAR3VpZAABAAAAFAAAAC9TY3JpcHQvQ29yZVVPYmplY3QAAAAAABAAAAAIFH7ZBfcy/UKTaGQz7nsNgi8AAABRdWVzdENsYXNzXzExX0NFNUNFNjY1NEFBMjY3RTY2MTQwNzdBMTAxODcxRDMxAA8AAABPYmplY3RQcm9wZXJ0eQAAAAAAgwAAAAB/AAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9SZXR1cm5Cb3gtU2NhblJldHVybk1vdmllX0Jyb2tlbi5RdWVzdF9SZXR1cm5Cb3gtU2NhblJldHVybk1vdmllX0Jyb2tlbl9DAC8AAABQcm9ncmVzc2lvbl82XzIxRTg2MUU0NEM1RERCQ0VBQ0YzRjQ5NTYwOTdFRUUxAAwAAABJbnRQcm9wZXJ0eQAAAAAABAAAAAAAAAAABQAAAE5vbmUADQAAAFF1ZXN0TWFuYWdlcgAPAAAAU3RydWN0UHJvcGVydHkAAgAAABMAAABRdWVzdF9NYW5hZ2VyX1NhdmUAAQAAADkAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1F1ZXN0X01hbmFnZXJfU2F2ZQAAAAAAJQAAAGMzZDRjNzFjLTRhZDUtNGMyMS0yMTYyLTA2OGJiZjFlNjg2MgAAAAAARwoAAAAtAAAAUXVlc3REb25lXzRfNTIyNEY5MjI0MjhDQTVERkE3RTg2QjlFRDhFODhEOTAADAAAAE1hcFByb3BlcnR5AAIAAAAPAAAAT2JqZWN0UHJvcGVydHkAAAAAAA0AAABCb29sUHJvcGVydHkAAAAAAMgJAAAAAAAAABkAAABTAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9Nb3ZlUGxheWVyLlF1ZXN0X01vdmVQbGF5ZXJfQwABXQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfQWNjZXNzQ2F0YWxvZ3VlLlF1ZXN0X0FjY2Vzc0NhdGFsb2d1ZV9DAAFTAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9CdXlTaGVsdmVzLlF1ZXN0X0J1eVNoZWx2ZXNfQwABWQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfUGlja1VwU2hlbHZlcy5RdWVzdF9QaWNrVXBTaGVsdmVzX0MAAVcAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1BsYWNlU2hlbHZlcy5RdWVzdF9QbGFjZVNoZWx2ZXNfQwABWwAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfQWNjZXNzQ29tcHV0ZXIuUXVlc3RfQWNjZXNzQ29tcHV0ZXJfQwABUQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfQnV5TW92aWVzLlF1ZXN0X0J1eU1vdmllc19DAAFXAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9QaWNrVXBNb3ZpZXMuUXVlc3RfUGlja1VwTW92aWVzX0MAAWcAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1N0b2NrTW92aWVzSW5TaGVsdmVzLlF1ZXN0X1N0b2NrTW92aWVzSW5TaGVsdmVzX0MAAU8AAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1NhdmVHYW1lLlF1ZXN0X1NhdmVHYW1lX0MAAV0AAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X0FjY2Vzc05hbWVTdG9yZS5RdWVzdF9BY2Nlc3NOYW1lU3RvcmVfQwABTwAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfT3BlblNpZ24uUXVlc3RfT3BlblNpZ25fQwABVwAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfQWNjZXNzRmx5ZXJzLlF1ZXN0X0FjY2Vzc0ZseWVyc19DAAFtAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9DaGVja091dC1TZXJ2ZUN1c3RvbWVycy5RdWVzdF9DaGVja091dC1TZXJ2ZUN1c3RvbWVyc19DAAFbAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9BY2Nlc3NDYWxlbmRhci5RdWVzdF9BY2Nlc3NDYWxlbmRhcl9DAAFXAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9BY2Nlc3NSZXR1cm4uUXVlc3RfQWNjZXNzUmV0dXJuX0MAAXMAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1JldHVybkJveC1TY2FuUmV0dXJuTW92aWVzLlF1ZXN0X1JldHVybkJveC1TY2FuUmV0dXJuTW92aWVzX0MAAWcAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1N0b2NrLVJlc2VydmVkTW92aWVzLlF1ZXN0X1N0b2NrLVJlc2VydmVkTW92aWVzX0MAAVkAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X09wZW5TaWduLURheTIuUXVlc3RfT3BlblNpZ24tRGF5Ml9DAAFfAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9BY2Nlc3MtVGVsZXBob25lLlF1ZXN0X0FjY2Vzcy1UZWxlcGhvbmVfQwABhQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3QtUmVwZWF0YWJsZV9QaG9uZV9QaWNrVXAtUmVzZXJ2YXRpb24uUXVlc3QtUmVwZWF0YWJsZV9QaG9uZV9QaWNrVXAtUmVzZXJ2YXRpb25fQwABZQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfTmV3UmVsZWFzZV9CdXlNb3ZpZS5RdWVzdF9OZXdSZWxlYXNlX0J1eU1vdmllX0MAAXsAAAAvR2FtZS9WaWRlb1N0b3JlL2NvcmUvYmx1ZXByaW50L3F1ZXN0L1R1dG9yaWFsL1F1ZXN0X1JldHVybkJveC1TY2FuUmV0dXJuTW92aWVfTGF0ZS5RdWVzdF9SZXR1cm5Cb3gtU2NhblJldHVybk1vdmllX0xhdGVfQwABXQAAAC9HYW1lL1ZpZGVvU3RvcmUvY29yZS9ibHVlcHJpbnQvcXVlc3QvVHV0b3JpYWwvUXVlc3RfR29Ub0JsYWNrTWFya2V0LlF1ZXN0X0dvVG9CbGFja01hcmtldF9DAAFhAAAAL0dhbWUvVmlkZW9TdG9yZS9jb3JlL2JsdWVwcmludC9xdWVzdC9UdXRvcmlhbC9RdWVzdF9FbmRUdXRvcmlhbC1CYXNpYy5RdWVzdF9FbmRUdXRvcmlhbC1CYXNpY19DAAEFAAAATm9uZQA=""")

QUEST_MARKER = b"Quest\x00"
STAT_MARKER = b"Statistic\x00"
END_TUTORIAL = b"Quest_EndTutorial-Basic"

def default_save_dir():
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        return None
    candidates = [
        Path(local) / "RetroRewind" / "Saved" / "SaveGames",
        Path(local) / "Retro Rewind" / "Saved" / "SaveGames",
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]

def read_store_name(path):
    """Lee el nombre de la tienda guardado en el .sav sin modificar nada."""
    try:
        data = Path(path).read_bytes()

        # Retro Rewind stores the shop name in a TextProperty whose generated
        # property name begins with Name_18_. We only read it for display.
        m = re.search(br"Name_18_[0-9A-F]+\x00", data)
        if not m:
            return None

        start = m.end()
        end = min(len(data), start + 260)
        chunk = data[start:end]

        tp = chunk.find(b"TextProperty\x00")
        if tp == -1:
            return None

        region_start = tp + len(b"TextProperty\x00")
        region = chunk[region_start:]

        candidates = []
        for i in range(0, max(0, len(region) - 5)):
            n = int.from_bytes(region[i:i+4], "little", signed=True)
            if not (2 <= n <= 80):
                continue
            j = i + 4
            k = j + n
            if k > len(region):
                continue
            raw = region[j:k]
            if not raw.endswith(b"\x00"):
                continue
            raw = raw[:-1]
            try:
                s = raw.decode("utf-8")
            except UnicodeDecodeError:
                continue
            if not s or any(ord(c) < 32 for c in s):
                continue
            if s == "TextProperty":
                continue
            if re.fullmatch(r"[0-9A-F]{20,}", s):
                continue
            candidates.append(s)

        return candidates[0] if candidates else None
    except Exception:
        return None

def list_saves(folder):
    p = Path(folder)
    if not p.exists():
        return []

    saves = []
    for f in p.glob("Player_Save*.sav"):
        low = f.name.lower()
        if "backup" in low or "rr_skip_backup" in low or "skip_tutorial_test" in low:
            continue
        try:
            if f.read_bytes()[:4] != b"GVAS":
                continue
        except Exception:
            continue
        saves.append(f)

    return sorted(saves, key=lambda x: x.stat().st_mtime, reverse=True)

def patch_save(path):
    path = Path(path)
    data = path.read_bytes()

    if not data.startswith(b"GVAS"):
        raise ValueError("El archivo no parece ser un guardado GVAS de Unreal Engine.")

    q = data.find(QUEST_MARKER)
    st = data.find(STAT_MARKER)

    if q < 4 or st < 4 or st <= q:
        raise ValueError("No se ha encontrado la estructura de quests esperada.")

    # Include the 4-byte FString length prefix.
    q0 = q - 4
    st0 = st - 4
    current_block = data[q0:st0]

    if b"QuestManager\x00" not in current_block or b"QuestDone_" not in current_block:
        raise ValueError("La estructura de QuestManager no coincide con la versión compatible.")

    if END_TUTORIAL in current_block:
        return "already", None

    backup_dir = path.parent / "RetroRewindTool_Backups"
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = backup_dir / f"{path.stem}_before_skip_tutorial_{stamp}{path.suffix}"
    shutil.copy2(path, backup)

    new_data = data[:q0] + PATCH + data[st0:]

    # Extra sanity checks before writing.
    if not new_data.startswith(b"GVAS"):
        raise ValueError("Comprobación de seguridad fallida.")
    if END_TUTORIAL not in new_data:
        raise ValueError("No se pudo insertar el estado de tutorial completado.")

    fd, tmp_name = tempfile.mkstemp(prefix=path.stem + "_", suffix=".tmp", dir=path.parent)
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        tmp.write_bytes(new_data)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)

    return "patched", backup


MONEY64_NAME = b"Money64_14_4E3C8A914A3F4058F90C30BD533FEF7E\x00"
MONEY64_PROP = b"Int64Property\x00"
MONEY32_NAME = b"Money_2_334F50394D552F37FAADAB9A3C50D7D7\x00"


LEVEL_NAME = b"Level_4_D665A6394BEDE281DFD626929A94188A\x00"
INT_PROP = b"IntProperty\x00"



def read_money(path):
    """Devuelve el dinero actual como float. Si Money64 no existe, usa el valor inicial por defecto ($550)."""
    try:
        data = Path(path).read_bytes()
        if not data.startswith(b"GVAS"):
            return None

        # Normal case after the value has been serialized.
        idx = data.find(MONEY64_NAME)
        if idx != -1:
            pidx = data.find(MONEY64_PROP, idx, idx + 180)
            if pidx == -1:
                return None
            marker = b"\x08\x00\x00\x00\x00"
            sm = data.find(marker, pidx + len(MONEY64_PROP), pidx + len(MONEY64_PROP) + 40)
            if sm == -1:
                return None
            vpos = sm + len(marker)
            if vpos + 8 > len(data):
                return None
            cents = struct.unpack("<q", data[vpos:vpos+8])[0]
            return cents / 100.0

        # In fresh saves Retro Rewind may omit Money64 while the game is still
        # using the default starting balance.
        return 550.0
    except Exception:
        return None

def read_store_level(path):
    """Devuelve el nivel de tienda serializado o None si aún no existe."""
    try:
        data = Path(path).read_bytes()
        if not data.startswith(b"GVAS"):
            return None
        idx = data.find(LEVEL_NAME)
        if idx == -1:
            return None
        pidx = data.find(INT_PROP, idx, idx + 180)
        if pidx == -1:
            return None
        marker = b"\x04\x00\x00\x00\x00"
        sm = data.find(marker, pidx + len(INT_PROP), pidx + len(INT_PROP) + 40)
        if sm == -1:
            return None
        vpos = sm + len(marker)
        if vpos + 4 > len(data):
            return None
        return struct.unpack("<i", data[vpos:vpos+4])[0]
    except Exception:
        return None



def _save_edited_bytes(path, data, edit_name):
    """Guarda una edición del save conservando una copia de seguridad."""
    path = Path(path)
    backup_dir = path.parent / "RetroRewindTool_Backups"
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = backup_dir / f"{path.stem}_before_{edit_name}_edit_{stamp}{path.suffix}"
    shutil.copy2(path, backup)

    fd, tmp_name = tempfile.mkstemp(prefix=path.stem + "_", suffix=".tmp", dir=path.parent)
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        tmp.write_bytes(data)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
    return backup


def _find_property_value(data, field_name, property_type, marker, value_size):
    """Localiza el valor serializado de una propiedad conocida del guardado."""
    idx = data.find(field_name)
    if idx == -1:
        return None
    pidx = data.find(property_type, idx, idx + 180)
    if pidx == -1:
        raise ValueError("La estructura encontrada no coincide con la versión compatible.")
    sm = data.find(marker, pidx + len(property_type), pidx + len(property_type) + 40)
    if sm == -1:
        raise ValueError("No se pudo localizar el valor de la propiedad.")
    vpos = sm + len(marker)
    if vpos + value_size > len(data):
        raise ValueError("El valor de la propiedad está incompleto.")
    return vpos


def set_store_level(path, new_level):
    """Cambia únicamente el Level existente. No toca Experience."""
    path = Path(path)
    if new_level < 1:
        raise ValueError("El editor de nivel solo está disponible desde nivel 1.")
    if new_level > 9999:
        raise ValueError("El nivel indicado es demasiado alto.")

    data = bytearray(path.read_bytes())
    if not data.startswith(b"GVAS"):
        raise ValueError("El archivo no parece ser un guardado válido de Retro Rewind.")

    vpos = _find_property_value(data, LEVEL_NAME, INT_PROP, b"\x04\x00\x00\x00\x00", 4)
    if vpos is None:
        raise ValueError(
            "Esta partida todavía no tiene creado el campo Level. "
            "Juega normalmente hasta alcanzar el nivel 1, guarda y vuelve a intentarlo."
        )

    old_level = struct.unpack_from("<i", data, vpos)[0]
    struct.pack_into("<i", data, vpos, int(new_level))
    backup = _save_edited_bytes(path, data, "level")
    return backup, old_level




def set_money(path, dollars):
    """Cambia el dinero. Retro Rewind guarda Money64 en centavos."""
    path = Path(path)
    if dollars < 0:
        raise ValueError("El dinero no puede ser negativo.")
    if dollars > 9_000_000_000:
        raise ValueError("La cantidad es demasiado alta.")

    cents = int(round(dollars * 100))
    data = bytearray(path.read_bytes())
    if not data.startswith(b"GVAS"):
        raise ValueError("El archivo no parece ser un guardado válido de Retro Rewind.")

    vpos = _find_property_value(data, MONEY64_NAME, MONEY64_PROP, b"\x08\x00\x00\x00\x00", 8)

    if vpos is not None:
        struct.pack_into("<q", data, vpos, cents)
    else:
        m32 = data.find(MONEY32_NAME)
        if m32 == -1:
            raise ValueError("No se encontró la estructura de dinero compatible.")

        ip = data.find(INT_PROP, m32, m32 + 160)
        if ip == -1:
            raise ValueError("No se encontró IntProperty asociado a Money.")

        none_marker = b"\x05\x00\x00\x00None\x00"
        none_pos = data.find(none_marker, ip, ip + 120)
        if none_pos == -1:
            raise ValueError("No se encontró el final de la estructura de dinero.")

        prop = bytearray()
        prop.extend(struct.pack("<i", len("Money64_14_4E3C8A914A3F4058F90C30BD533FEF7E") + 1))
        prop.extend(MONEY64_NAME)
        prop.extend(struct.pack("<i", len("Int64Property") + 1))
        prop.extend(MONEY64_PROP)
        prop.extend(b"\x00\x00\x00\x00")
        prop.extend(struct.pack("<I", 8))
        prop.extend(b"\x00")
        prop.extend(struct.pack("<q", cents))

        money_len_prefix = m32 - 4
        size_pos = money_len_prefix - 9
        if size_pos < 0:
            raise ValueError("No se pudo localizar el tamaño del Core_Game_Struct.")

        old_size = struct.unpack_from("<I", data, size_pos)[0]
        if old_size < 50 or old_size > 10000:
            raise ValueError("El tamaño de Core_Game_Struct no parece compatible.")

        struct.pack_into("<I", data, size_pos, old_size + len(prop))
        data[none_pos:none_pos] = prop

    return _save_edited_bytes(path, data, "money")




APP_VERSION = "0.13 RC"

def toolkit_config_path():
    base = os.environ.get("LOCALAPPDATA") or str(Path.home())
    p = Path(base) / "RetroRewindToolkit"
    p.mkdir(parents=True, exist_ok=True)
    return p / "settings.json"

def load_toolkit_settings():
    try:
        p = toolkit_config_path()
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    except Exception:
        pass
    return {}

def save_toolkit_settings(data):
    try:
        toolkit_config_path().write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except Exception:
        pass

class App(tk.Tk):
    TXT = {
        "es": {
            "lang":"Idioma:", "warning":"⚠ Retro Rewind debe estar CERRADO antes de modificar una partida.",
            "folder":"Carpeta de guardados:", "browse":"Buscar...", "save":"Partida:", "refresh":"Actualizar",
            "tutorial":"Tutorial", "skip":"SALTAR TUTORIAL", "money":"Dinero", "amount":"Cantidad ($):",
            "change_money":"CAMBIAR DINERO", "level":"Nivel de tienda", "new_level":"Nuevo nivel:",
            "change_level":"CAMBIAR NIVEL",
            "vhs_label":"CINTA VHS", "cash_label":"CAJA / EFECTIVO", "progress_label":"PROGRESO DE TIENDA",
            "money_note":"* Disponible después de realizar al menos una compra en el juego y guardar la partida.",
            "level_note":"* Solo disponible si la partida ha alcanzado el nivel 1 de forma natural.",
            "found":"✓ {n} guardado(s) de Retro Rewind detectado(s).",
            "none":"⚠ No se han detectado guardados válidos.",
            "select":"Selecciona primero una partida válida.", "confirm":"Confirmar", "done":"Listo",
            "error":"Error", "nochanges":"Sin cambios",
            "skip_confirm":"Se modificará:\n\n{label}\n\nSe creará automáticamente una copia de seguridad antes de tocar el save.\n\n¿Continuar?",
            "skip_already":"Ese save ya contiene el estado de tutorial completado.",
            "skip_done":"Se ha aplicado Skip Tutorial correctamente.",
            "backup":"Copia de seguridad:",
            "money_invalid":"Escribe una cantidad válida, por ejemplo: 2500 o 2500,50",
            "money_negative":"El dinero no puede ser negativo.",
            "money_confirm":"Partida:\n\n{label}\n\nNuevo dinero: {shown}\n\nSe creará automáticamente una copia de seguridad.\n\n¿Continuar?",
            "money_done":"Dinero actualizado correctamente a {shown}.",
            "level_invalid":"Escribe un nivel entero, por ejemplo: 5",
            "level_min":"El editor de nivel funciona desde nivel 1. Alcanza primero el nivel 1 de forma natural.",
            "level_confirm":"Partida:\n\n{label}\n\nNuevo nivel de tienda: {level}\n\nSolo se modificará Level. Experience y LifetimeExperience no se tocarán.\nRetro Rewind gestionará los desbloqueos correspondientes.\n\nSe creará automáticamente una copia de seguridad.\n\n¿Continuar?",
            "level_done":"Nivel de tienda actualizado correctamente:\n{old} → {new}",
            "status_ready":"Selecciona una partida.",
            "current_money":"Dinero actual:", "current_level":"Nivel actual:", "level_zero":"0 (aún no editable)",
        },
        "en": {
            "lang":"Language:", "warning":"⚠ Retro Rewind must be CLOSED before editing a save.",
            "folder":"Save folder:", "browse":"Browse...", "save":"Save:", "refresh":"Refresh",
            "tutorial":"Tutorial", "skip":"SKIP TUTORIAL", "money":"Money", "amount":"Amount ($):",
            "change_money":"CHANGE MONEY", "level":"Store level", "new_level":"New level:",
            "change_level":"CHANGE LEVEL",
            "vhs_label":"VHS TAPE", "cash_label":"CHECKOUT / CASH", "progress_label":"STORE PROGRESS",
            "money_note":"* Available after making at least one purchase in-game and saving the game.",
            "level_note":"* Only available if the save has reached level 1 naturally.",
            "found":"✓ {n} Retro Rewind save(s) detected.",
            "none":"⚠ No valid saves detected.",
            "select":"Select a valid save first.", "confirm":"Confirm", "done":"Done",
            "error":"Error", "nochanges":"No changes",
            "skip_confirm":"This save will be modified:\n\n{label}\n\nA backup will be created automatically before editing the save.\n\nContinue?",
            "skip_already":"This save already contains the completed tutorial state.",
            "skip_done":"Skip Tutorial was applied successfully.",
            "backup":"Backup:",
            "money_invalid":"Enter a valid amount, for example: 2500 or 2500.50",
            "money_negative":"Money cannot be negative.",
            "money_confirm":"Save:\n\n{label}\n\nNew money: {shown}\n\nA backup will be created automatically.\n\nContinue?",
            "money_done":"Money updated successfully to {shown}.",
            "level_invalid":"Enter a whole-number level, for example: 5",
            "level_min":"Level editing works from level 1 onward. Reach level 1 naturally first.",
            "level_confirm":"Save:\n\n{label}\n\nNew store level: {level}\n\nOnly Level will be changed. Experience and LifetimeExperience will remain untouched.\nRetro Rewind will handle the corresponding unlocks.\n\nA backup will be created automatically.\n\nContinue?",
            "level_done":"Store level updated successfully:\n{old} → {new}",
            "status_ready":"Select a save.",
            "current_money":"Current money:", "current_level":"Current level:", "level_zero":"0 (not editable yet)",
        },
        "fr": {
            "lang":"Langue :", "warning":"⚠ Retro Rewind doit être FERMÉ avant de modifier une sauvegarde.",
            "folder":"Dossier des sauvegardes :", "browse":"Parcourir...", "save":"Sauvegarde :", "refresh":"Actualiser",
            "tutorial":"Tutoriel", "skip":"PASSER LE TUTORIEL", "money":"Argent", "amount":"Montant ($) :",
            "change_money":"MODIFIER L’ARGENT", "level":"Niveau du magasin", "new_level":"Nouveau niveau :",
            "change_level":"MODIFIER LE NIVEAU",
            "vhs_label":"CASSETTE VHS", "cash_label":"CAISSE / ARGENT", "progress_label":"PROGRESSION DU MAGASIN",
            "money_note":"* Disponible après avoir effectué au moins un achat dans le jeu et sauvegardé la partie.",
            "level_note":"* Disponible uniquement si la sauvegarde a atteint naturellement le niveau 1.",
            "found":"✓ {n} sauvegarde(s) Retro Rewind détectée(s).",
            "none":"⚠ Aucune sauvegarde valide détectée.",
            "select":"Sélectionnez d’abord une sauvegarde valide.", "confirm":"Confirmer", "done":"Terminé",
            "error":"Erreur", "nochanges":"Aucune modification",
            "skip_confirm":"Cette sauvegarde sera modifiée :\n\n{label}\n\nUne copie de sauvegarde sera créée automatiquement avant toute modification.\n\nContinuer ?",
            "skip_already":"Cette sauvegarde contient déjà l’état de tutoriel terminé.",
            "skip_done":"Le tutoriel a été ignoré avec succès.",
            "backup":"Copie de sauvegarde :",
            "money_invalid":"Saisissez un montant valide, par exemple : 2500 ou 2500,50",
            "money_negative":"L’argent ne peut pas être négatif.",
            "money_confirm":"Sauvegarde :\n\n{label}\n\nNouvel argent : {shown}\n\nUne copie de sauvegarde sera créée automatiquement.\n\nContinuer ?",
            "money_done":"Argent mis à jour avec succès : {shown}.",
            "level_invalid":"Saisissez un niveau entier, par exemple : 5",
            "level_min":"L’éditeur de niveau fonctionne à partir du niveau 1. Atteignez d’abord naturellement le niveau 1.",
            "level_confirm":"Sauvegarde :\n\n{label}\n\nNouveau niveau du magasin : {level}\n\nSeul Level sera modifié. Experience et LifetimeExperience resteront inchangés.\nRetro Rewind gérera les déblocages correspondants.\n\nUne copie de sauvegarde sera créée automatiquement.\n\nContinuer ?",
            "level_done":"Niveau du magasin mis à jour avec succès :\n{old} → {new}",
            "status_ready":"Sélectionnez une sauvegarde.",
            "current_money":"Argent actuel :", "current_level":"Niveau actuel :", "level_zero":"0 (pas encore modifiable)",
        },
        "de": {
            "lang":"Sprache:", "warning":"⚠ Retro Rewind muss GESCHLOSSEN sein, bevor ein Spielstand bearbeitet wird.",
            "folder":"Spielstand-Ordner:", "browse":"Durchsuchen...", "save":"Spielstand:", "refresh":"Aktualisieren",
            "tutorial":"Tutorial", "skip":"TUTORIAL ÜBERSPRINGEN", "money":"Geld", "amount":"Betrag ($):",
            "change_money":"GELD ÄNDERN", "level":"Ladenstufe", "new_level":"Neue Stufe:",
            "change_level":"STUFE ÄNDERN",
            "vhs_label":"VHS-KASSETTE", "cash_label":"KASSE / GELD", "progress_label":"LADENFORTSCHRITT",
            "money_note":"* Verfügbar, nachdem mindestens ein Kauf im Spiel getätigt und gespeichert wurde.",
            "level_note":"* Nur verfügbar, wenn der Spielstand Stufe 1 auf normalem Weg erreicht hat.",
            "found":"✓ {n} Retro-Rewind-Spielstand/Spielstände erkannt.",
            "none":"⚠ Keine gültigen Spielstände erkannt.",
            "select":"Wähle zuerst einen gültigen Spielstand aus.", "confirm":"Bestätigen", "done":"Fertig",
            "error":"Fehler", "nochanges":"Keine Änderungen",
            "skip_confirm":"Dieser Spielstand wird geändert:\n\n{label}\n\nVor der Änderung wird automatisch eine Sicherung erstellt.\n\nFortfahren?",
            "skip_already":"Dieser Spielstand enthält bereits den abgeschlossenen Tutorial-Status.",
            "skip_done":"Das Tutorial wurde erfolgreich übersprungen.",
            "backup":"Sicherung:",
            "money_invalid":"Gib einen gültigen Betrag ein, z. B. 2500 oder 2500,50",
            "money_negative":"Der Geldbetrag darf nicht negativ sein.",
            "money_confirm":"Spielstand:\n\n{label}\n\nNeuer Geldbetrag: {shown}\n\nVor der Änderung wird automatisch eine Sicherung erstellt.\n\nFortfahren?",
            "money_done":"Geld erfolgreich auf {shown} gesetzt.",
            "level_invalid":"Gib eine ganze Zahl als Stufe ein, z. B. 5",
            "level_min":"Die Stufenbearbeitung funktioniert ab Stufe 1. Erreiche zuerst Stufe 1 auf normalem Weg.",
            "level_confirm":"Spielstand:\n\n{label}\n\nNeue Ladenstufe: {level}\n\nEs wird nur Level geändert. Experience und LifetimeExperience bleiben unverändert.\nRetro Rewind übernimmt die entsprechenden Freischaltungen.\n\nVor der Änderung wird automatisch eine Sicherung erstellt.\n\nFortfahren?",
            "level_done":"Ladenstufe erfolgreich aktualisiert:\n{old} → {new}",
            "status_ready":"Wähle einen Spielstand aus.",
            "current_money":"Aktuelles Geld:", "current_level":"Aktuelle Stufe:", "level_zero":"0 (noch nicht bearbeitbar)",
        },
        "it": {
            "lang":"Lingua:", "warning":"⚠ Retro Rewind deve essere CHIUSO prima di modificare un salvataggio.",
            "folder":"Cartella dei salvataggi:", "browse":"Sfoglia...", "save":"Salvataggio:", "refresh":"Aggiorna",
            "tutorial":"Tutorial", "skip":"SALTA TUTORIAL", "money":"Denaro", "amount":"Importo ($):",
            "change_money":"CAMBIA DENARO", "level":"Livello negozio", "new_level":"Nuovo livello:",
            "change_level":"CAMBIA LIVELLO",
            "vhs_label":"CASSETTA VHS", "cash_label":"CASSA / DENARO", "progress_label":"PROGRESSO NEGOZIO",
            "money_note":"* Disponibile dopo aver effettuato almeno un acquisto nel gioco e aver salvato la partita.",
            "level_note":"* Disponibile solo se il salvataggio ha raggiunto naturalmente il livello 1.",
            "found":"✓ Rilevati {n} salvataggi di Retro Rewind.",
            "none":"⚠ Nessun salvataggio valido rilevato.",
            "select":"Seleziona prima un salvataggio valido.", "confirm":"Conferma", "done":"Fatto",
            "error":"Errore", "nochanges":"Nessuna modifica",
            "skip_confirm":"Questo salvataggio verrà modificato:\n\n{label}\n\nVerrà creata automaticamente una copia di sicurezza prima della modifica.\n\nContinuare?",
            "skip_already":"Questo salvataggio contiene già lo stato di tutorial completato.",
            "skip_done":"Tutorial saltato con successo.",
            "backup":"Copia di sicurezza:",
            "money_invalid":"Inserisci un importo valido, ad esempio: 2500 o 2500,50",
            "money_negative":"Il denaro non può essere negativo.",
            "money_confirm":"Salvataggio:\n\n{label}\n\nNuovo denaro: {shown}\n\nVerrà creata automaticamente una copia di sicurezza.\n\nContinuare?",
            "money_done":"Denaro aggiornato correttamente a {shown}.",
            "level_invalid":"Inserisci un livello intero, ad esempio: 5",
            "level_min":"L’editor del livello funziona dal livello 1 in poi. Raggiungi prima naturalmente il livello 1.",
            "level_confirm":"Salvataggio:\n\n{label}\n\nNuovo livello negozio: {level}\n\nVerrà modificato solo Level. Experience e LifetimeExperience resteranno invariati.\nRetro Rewind gestirà gli sblocchi corrispondenti.\n\nVerrà creata automaticamente una copia di sicurezza.\n\nContinuare?",
            "level_done":"Livello negozio aggiornato correttamente:\n{old} → {new}",
            "status_ready":"Seleziona un salvataggio.",
            "current_money":"Denaro attuale:", "current_level":"Livello attuale:", "level_zero":"0 (non ancora modificabile)",
        },
        "pt": {
            "lang":"Idioma:", "warning":"⚠ Retro Rewind deve estar FECHADO antes de editar um save.",
            "folder":"Pasta de saves:", "browse":"Procurar...", "save":"Save:", "refresh":"Atualizar",
            "tutorial":"Tutorial", "skip":"PULAR TUTORIAL", "money":"Dinheiro", "amount":"Valor ($):",
            "change_money":"ALTERAR DINHEIRO", "level":"Nível da loja", "new_level":"Novo nível:",
            "change_level":"ALTERAR NÍVEL",
            "vhs_label":"FITA VHS", "cash_label":"CAIXA / DINHEIRO", "progress_label":"PROGRESSO DA LOJA",
            "money_note":"* Disponível após fazer pelo menos uma compra no jogo e salvar a partida.",
            "level_note":"* Disponível apenas se o save tiver alcançado naturalmente o nível 1.",
            "found":"✓ {n} save(s) do Retro Rewind detectado(s).",
            "none":"⚠ Nenhum save válido detectado.",
            "select":"Selecione primeiro um save válido.", "confirm":"Confirmar", "done":"Concluído",
            "error":"Erro", "nochanges":"Sem alterações",
            "skip_confirm":"Este save será modificado:\n\n{label}\n\nUma cópia de segurança será criada automaticamente antes da edição.\n\nContinuar?",
            "skip_already":"Este save já contém o estado de tutorial concluído.",
            "skip_done":"Tutorial pulado com sucesso.",
            "backup":"Cópia de segurança:",
            "money_invalid":"Digite um valor válido, por exemplo: 2500 ou 2500,50",
            "money_negative":"O dinheiro não pode ser negativo.",
            "money_confirm":"Save:\n\n{label}\n\nNovo dinheiro: {shown}\n\nUma cópia de segurança será criada automaticamente.\n\nContinuar?",
            "money_done":"Dinheiro atualizado com sucesso para {shown}.",
            "level_invalid":"Digite um nível inteiro, por exemplo: 5",
            "level_min":"A edição de nível funciona a partir do nível 1. Alcance primeiro o nível 1 naturalmente.",
            "level_confirm":"Save:\n\n{label}\n\nNovo nível da loja: {level}\n\nApenas Level será alterado. Experience e LifetimeExperience permanecerão intactos.\nRetro Rewind cuidará dos desbloqueios correspondentes.\n\nUma cópia de segurança será criada automaticamente.\n\nContinuar?",
            "level_done":"Nível da loja atualizado com sucesso:\n{old} → {new}",
            "status_ready":"Selecione um save.",
            "current_money":"Dinheiro atual:", "current_level":"Nível atual:", "level_zero":"0 (ainda não editável)",
        }
    }

    # Video-store inspired palette. No external assets are required.
    BG = "#17191d"
    HEADER = "#101216"
    PANEL = "#24272d"
    PANEL_ALT = "#2c3037"
    BORDER = "#474c55"
    CREAM = "#f2e5c4"
    MUTED = "#aaa79f"
    RED = "#d9534f"
    RED_HOVER = "#ea625d"
    TEAL = "#43a6a1"
    TEAL_HOVER = "#55bbb6"
    GOLD = "#d7aa52"
    ENTRY = "#121419"
    WHITE = "#f7f4eb"

    def __init__(self):
        super().__init__()
        self.title("Retro Rewind Toolkit")
        self.geometry("900x900")
        self.minsize(840, 900)
        self.configure(bg=self.BG)

        settings = load_toolkit_settings()
        self.lang = settings.get("language", "es")
        saved_folder = settings.get("save_folder")
        initial_folder = saved_folder if saved_folder and Path(saved_folder).exists() else str(default_save_dir() or "")
        self.folder_var = tk.StringVar(value=initial_folder)
        self.save_var = tk.StringVar()
        self.money_var = tk.StringVar()
        self.level_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.save_lookup = {}

        self._styles()
        self._build()
        self._translate()
        self.after(150, self.refresh)

    def t(self, key):
        return self.TXT[self.lang][key]

    def _styles(self):
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass

        s.configure("VHS.TCombobox",
                    fieldbackground=self.ENTRY, background=self.PANEL_ALT,
                    foreground=self.WHITE, arrowcolor=self.CREAM,
                    bordercolor=self.BORDER, lightcolor=self.BORDER,
                    darkcolor=self.BORDER, padding=7)
        s.map("VHS.TCombobox",
              fieldbackground=[("readonly", self.ENTRY)],
              foreground=[("readonly", self.WHITE)],
              selectbackground=[("readonly", self.ENTRY)],
              selectforeground=[("readonly", self.WHITE)])

    def _button(self, parent, text="", command=None, accent="teal", width=None):
        base = self.TEAL if accent == "teal" else self.RED
        hover = self.TEAL_HOVER if accent == "teal" else self.RED_HOVER
        b = tk.Button(parent, text=text, command=command, width=width,
                      bg=base, fg=self.WHITE, activebackground=hover,
                      activeforeground=self.WHITE, relief="flat",
                      bd=0, padx=16, pady=9, cursor="hand2",
                      font=("Segoe UI", 9, "bold"))
        return b

    def _entry(self, parent, variable, width=20):
        return tk.Entry(parent, textvariable=variable, width=width,
                        bg=self.ENTRY, fg=self.WHITE, insertbackground=self.WHITE,
                        relief="flat", bd=0, highlightthickness=1,
                        highlightbackground=self.BORDER,
                        highlightcolor=self.TEAL,
                        font=("Segoe UI", 10))

    def _card(self, parent):
        outer = tk.Frame(parent, bg=self.BORDER)
        inner = tk.Frame(outer, bg=self.PANEL)
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        return outer, inner

    def _build(self):
        # Header / video-store marquee
        header = tk.Frame(self, bg=self.HEADER, height=132)
        header.pack(fill="x")
        header.pack_propagate(False)

        brand = tk.Frame(header, bg=self.HEADER)
        brand.pack(side="left", padx=28, pady=(14,10))

        tk.Label(brand, text="RETRO REWIND",
                 bg=self.HEADER, fg=self.CREAM,
                 font=("Segoe UI", 23, "bold")).pack(anchor="w", pady=(0,1))
        tk.Label(brand, text="TOOLKIT",
                 bg=self.HEADER, fg=self.RED,
                 font=("Consolas", 13, "bold")).pack(anchor="w", pady=(0,2))

        lang_area = tk.Frame(header, bg=self.HEADER)
        lang_area.pack(side="right", padx=28)
        self.lang_lbl = tk.Label(lang_area, bg=self.HEADER, fg=self.MUTED,
                                 font=("Segoe UI", 9))
        self.lang_lbl.pack(anchor="e", pady=(0,5))
        self.lang_box = ttk.Combobox(
            lang_area,
            values=["Español","English","Français","Deutsch","Italiano","Português"],
            state="readonly", width=15, style="VHS.TCombobox"
        )
        lang_index = {"es":0, "en":1, "fr":2, "de":3, "it":4, "pt":5}.get(self.lang, 0)
        self.lang_box.current(lang_index)
        self.lang_box.pack()
        self.lang_box.bind("<<ComboboxSelected>>", self._lang_change)

        body = tk.Frame(self, bg=self.BG)
        body.pack(fill="both", expand=True, padx=26, pady=12)

        # Warning tape
        warning_box = tk.Frame(body, bg=self.GOLD)
        warning_box.pack(fill="x", pady=(0,14))
        self.warn = tk.Label(warning_box, bg=self.GOLD, fg="#181818",
                             font=("Segoe UI", 10, "bold"),
                             padx=12, pady=8)
        self.warn.pack(fill="x")

        # Save selection card
        outer, savecard = self._card(body)
        outer.pack(fill="x", pady=(0,10))

        top_line = tk.Frame(savecard, bg=self.PANEL)
        top_line.pack(fill="x", padx=16, pady=(13,7))
        tk.Label(top_line, text="▰", bg=self.PANEL, fg=self.TEAL,
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        self.save_title = tk.Label(top_line, bg=self.PANEL, fg=self.CREAM,
                                   font=("Segoe UI", 11, "bold"))
        self.save_title.pack(side="left", padx=(8,0))
        self.detect_lbl = tk.Label(top_line, bg=self.PANEL, fg=self.TEAL,
                                   font=("Segoe UI", 9))
        self.detect_lbl.pack(side="right")

        folder_row = tk.Frame(savecard, bg=self.PANEL)
        folder_row.pack(fill="x", padx=16, pady=5)
        self.folder_lbl = tk.Label(folder_row, bg=self.PANEL, fg=self.MUTED,
                                   width=20, anchor="w", font=("Segoe UI", 9))
        self.folder_lbl.pack(side="left")
        self.folder_entry = self._entry(folder_row, self.folder_var, 56)
        self.folder_entry.pack(side="left", fill="x", expand=True, ipady=7)
        self.browse_btn = self._button(folder_row, command=self.pick_folder, accent="teal")
        self.browse_btn.pack(side="left", padx=(8,0))

        save_row = tk.Frame(savecard, bg=self.PANEL)
        save_row.pack(fill="x", padx=16, pady=(5,14))
        self.save_lbl = tk.Label(save_row, bg=self.PANEL, fg=self.MUTED,
                                 width=20, anchor="w", font=("Segoe UI", 9))
        self.save_lbl.pack(side="left")
        self.combo = ttk.Combobox(save_row, textvariable=self.save_var,
                                  state="readonly", style="VHS.TCombobox")
        self.combo.pack(side="left", fill="x", expand=True)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self._update_selected_info())
        self.refresh_btn = self._button(save_row, command=self.refresh, accent="teal")
        self.refresh_btn.pack(side="left", padx=(8,0))

        current_row = tk.Frame(savecard, bg=self.PANEL)
        current_row.pack(fill="x", padx=16, pady=(0,14))

        self.current_money_caption = tk.Label(current_row, bg=self.PANEL, fg=self.MUTED,
                                              font=("Segoe UI", 9, "bold"))
        self.current_money_caption.pack(side="left")

        self.current_money_lbl = tk.Label(current_row, bg=self.PANEL, fg=self.TEAL,
                                          font=("Consolas", 10, "bold"))
        self.current_money_lbl.pack(side="left", padx=(6,18))

        self.current_level_caption = tk.Label(current_row, bg=self.PANEL, fg=self.MUTED,
                                              font=("Segoe UI", 9, "bold"))
        self.current_level_caption.pack(side="left")

        self.current_level_lbl = tk.Label(current_row, bg=self.PANEL, fg=self.GOLD,
                                          font=("Consolas", 10, "bold"))
        self.current_level_lbl.pack(side="left", padx=(6,0))

        # Three VHS-style tool cards
        tools = tk.Frame(body, bg=self.BG)
        tools.pack(fill="both", expand=True)

        # Tutorial
        o1, c1 = self._card(tools)
        o1.pack(fill="x", pady=(0,8))
        stripe = tk.Frame(c1, bg=self.RED, width=7)
        stripe.pack(side="left", fill="y")
        content = tk.Frame(c1, bg=self.PANEL)
        content.pack(side="left", fill="both", expand=True, padx=16, pady=13)
        self.tut_micro = tk.Label(content, bg=self.PANEL, fg=self.RED,
                                  font=("Consolas", 9, "bold"))
        self.tut_micro.pack(anchor="w")
        self.tut_title = tk.Label(content, bg=self.PANEL, fg=self.CREAM,
                                  font=("Segoe UI", 12, "bold"))
        self.tut_title.pack(anchor="w", pady=(2,8))
        self.skip_btn = self._button(content, command=self.apply_patch, accent="red")
        self.skip_btn.pack(anchor="w")

        # Money
        o2, c2 = self._card(tools)
        o2.pack(fill="x", pady=(0,8))
        stripe2 = tk.Frame(c2, bg=self.TEAL, width=7)
        stripe2.pack(side="left", fill="y")
        content2 = tk.Frame(c2, bg=self.PANEL)
        content2.pack(side="left", fill="both", expand=True, padx=16, pady=13)
        self.money_micro = tk.Label(content2, bg=self.PANEL, fg=self.TEAL,
                                    font=("Consolas", 9, "bold"))
        self.money_micro.pack(anchor="w")
        self.money_title = tk.Label(content2, bg=self.PANEL, fg=self.CREAM,
                                    font=("Segoe UI", 12, "bold"))
        self.money_title.pack(anchor="w", pady=(2,4))
        self.money_note = tk.Label(content2, bg=self.PANEL, fg=self.TEAL,
                                   wraplength=720, justify="left",
                                   font=("Segoe UI", 8, "bold"))
        self.money_note.pack(anchor="w", pady=(0,8))
        mr = tk.Frame(content2, bg=self.PANEL); mr.pack(fill="x")
        self.amount_lbl = tk.Label(mr, bg=self.PANEL, fg=self.MUTED,
                                   font=("Segoe UI", 9))
        self.amount_lbl.pack(side="left")
        self.money_entry = self._entry(mr, self.money_var, 18)
        self.money_entry.pack(side="left", padx=10, ipady=7)
        self.money_btn = self._button(mr, command=self.apply_money, accent="teal")
        self.money_btn.pack(side="left")

        # Level
        o3, c3 = self._card(tools)
        o3.pack(fill="x", pady=(0,8))
        stripe3 = tk.Frame(c3, bg=self.GOLD, width=7)
        stripe3.pack(side="left", fill="y")
        content3 = tk.Frame(c3, bg=self.PANEL)
        content3.pack(side="left", fill="both", expand=True, padx=16, pady=13)
        self.level_micro = tk.Label(content3, bg=self.PANEL, fg=self.GOLD,
                                    font=("Consolas", 9, "bold"))
        self.level_micro.pack(anchor="w")
        self.level_title = tk.Label(content3, bg=self.PANEL, fg=self.CREAM,
                                    font=("Segoe UI", 12, "bold"))
        self.level_title.pack(anchor="w", pady=(2,4))
        self.level_note = tk.Label(content3, bg=self.PANEL, fg=self.GOLD,
                                   wraplength=720, justify="left",
                                   font=("Segoe UI", 8, "bold"))
        self.level_note.pack(anchor="w", pady=(0,8))
        lr = tk.Frame(content3, bg=self.PANEL); lr.pack(fill="x")
        self.newlevel_lbl = tk.Label(lr, bg=self.PANEL, fg=self.MUTED,
                                     font=("Segoe UI", 9))
        self.newlevel_lbl.pack(side="left")
        self.level_entry = self._entry(lr, self.level_var, 18)
        self.level_entry.pack(side="left", padx=10, ipady=7)
        self.level_btn = self._button(lr, command=self.apply_level, accent="teal")
        self.level_btn.pack(side="left")

        info = tk.Frame(body, bg=self.BG)
        info.pack(fill="x", pady=(6,0))
        tk.Label(info, text="● Offline", bg=self.BG, fg=self.TEAL,
                 font=("Consolas", 8, "bold")).pack(side="left")
        tk.Label(info, text="  •  Automatic backups  •  No administrator rights required",
                 bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 8)).pack(side="left")

    def _lang_change(self,event=None):
        mapping = {
            "Español":"es", "English":"en", "Français":"fr",
            "Deutsch":"de", "Italiano":"it", "Português":"pt"
        }
        self.lang = mapping.get(self.lang_box.get(), "es")
        save_toolkit_settings({"language": self.lang, "save_folder": self.folder_var.get()})
        self._translate()
        self.refresh()
        self._update_selected_info()

    def _translate(self):
        self.lang_lbl.config(text=self.t("lang"))
        self.warn.config(text=self.t("warning"))
        self.save_title.config(text=self.t("save"))
        self.folder_lbl.config(text=self.t("folder"))
        self.browse_btn.config(text=self.t("browse"))
        self.save_lbl.config(text=self.t("save"))
        self.refresh_btn.config(text=self.t("refresh"))
        self.current_money_caption.config(text=self.t("current_money"))
        self.current_level_caption.config(text=self.t("current_level"))
        self.tut_title.config(text=self.t("tutorial"))
        self.skip_btn.config(text=self.t("skip"))
        self.money_title.config(text=self.t("money"))
        self.amount_lbl.config(text=self.t("amount"))
        self.money_btn.config(text=self.t("change_money"))
        self.money_note.config(text=self.t("money_note"))
        self.tut_micro.config(text=f"▣  {self.t("vhs_label")}")
        self.money_micro.config(text=f"$  {self.t("cash_label")}")
        self.level_micro.config(text=f"★  {self.t("progress_label")}")
        self.level_title.config(text=self.t("level") + " *")
        self.newlevel_lbl.config(text=self.t("new_level"))
        self.level_btn.config(text=self.t("change_level"))
        self.level_note.config(text=self.t("level_note"))
        if not self.status_var.get():
            self.status_var.set(self.t("status_ready"))

    def pick_folder(self):
        initial=self.folder_var.get()
        chosen=filedialog.askdirectory(initialdir=initial if Path(initial).exists() else None)
        if chosen:
            self.folder_var.set(chosen)
            save_toolkit_settings({"language": self.lang, "save_folder": chosen})
            self.refresh()

    def refresh(self):
        folder_now = self.folder_var.get().strip()
        if folder_now:
            save_toolkit_settings({"language": self.lang, "save_folder": folder_now})
        saves=list_saves(folder_now)
        self.save_lookup={}
        labels=[]
        for p in saves:
            store=read_store_name(p)
            label=f"{store} — {p.name}" if store else p.name
            labels.append(label)
            self.save_lookup[label]=p
        self.combo["values"]=labels
        if labels:
            current=self.save_var.get()
            self.save_var.set(current if current in labels else labels[0])
            msg=self.t("found").format(n=len(labels))
            self.detect_lbl.config(text=msg, fg=self.TEAL)
            self.status_var.set(msg)
            self._update_selected_info()
        else:
            self.save_var.set("")
            self.detect_lbl.config(text=self.t("none"), fg=self.RED)
            self.status_var.set(self.t("none"))
            self._update_selected_info()

    def _update_selected_info(self):
        path = self._selected()
        if path is None:
            self.current_money_lbl.config(text="—")
            self.current_level_lbl.config(text="—")
            self._update_level_state()
            return

        money = read_money(path)
        level = read_store_level(path)

        if money is None:
            self.current_money_lbl.config(text="—")
        else:
            self.current_money_lbl.config(text=f"${money:,.2f}")

        if level is None:
            self.current_level_lbl.config(text=self.t("level_zero"))
        else:
            self.current_level_lbl.config(text=str(level))

        self._update_level_state()

    def _update_level_state(self):
        """Bloquea el editor de nivel si el save aún no tiene Level serializado."""
        path = self._selected()
        current = read_store_level(path) if path else None

        if current is None:
            self.level_entry.config(state="disabled", disabledbackground="#1a1c21",
                                    disabledforeground="#777777")
            self.level_btn.config(state="disabled", bg="#55585d",
                                  activebackground="#55585d", cursor="arrow")
        else:
            self.level_entry.config(state="normal")
            self.level_btn.config(state="normal", bg=self.TEAL,
                                  activebackground=self.TEAL_HOVER, cursor="hand2")

    def _selected(self):
        path = self.save_lookup.get(self.save_var.get())
        if path is None or not Path(path).exists():
            return None
        try:
            if Path(path).read_bytes()[:4] != b"GVAS":
                return None
        except Exception:
            return None
        return path

    def apply_patch(self):
        label=self.save_var.get(); path=self._selected()
        if path is None:
            messagebox.showerror(self.t("error"),self.t("select")); return
        if not messagebox.askyesno(self.t("confirm"),self.t("skip_confirm").format(label=label)): return
        try:
            result,backup=patch_save(path)
            if result=="already":
                messagebox.showinfo(self.t("nochanges"),self.t("skip_already"))
            else:
                self.status_var.set(self.t("skip_done"))
                messagebox.showinfo(self.t("done"),f'{self.t("skip_done")}\n\n{self.t("backup")}\n{backup}')
        except Exception as e:
            messagebox.showerror(self.t("error"),str(e))

    def apply_money(self):
        label=self.save_var.get(); path=self._selected()
        if path is None:
            messagebox.showerror(self.t("error"),self.t("select")); return
        raw=self.money_var.get().strip().replace("$","").replace(" ","").replace(",",".")
        try:
            dollars=float(raw)
        except ValueError:
            messagebox.showwarning(self.t("error"),self.t("money_invalid")); return
        if dollars<0:
            messagebox.showwarning(self.t("error"),self.t("money_negative")); return
        shown=f"${dollars:,.2f}"
        if not messagebox.askyesno(self.t("confirm"),self.t("money_confirm").format(label=label,shown=shown)): return
        try:
            backup=set_money(path,dollars)
            self._update_selected_info()
            self.status_var.set(self.t("money_done").format(shown=shown))
            messagebox.showinfo(self.t("done"),f'{self.t("money_done").format(shown=shown)}\n\n{self.t("backup")}\n{backup}')
        except Exception as e:
            messagebox.showerror(self.t("error"),str(e))

    def apply_level(self):
        label=self.save_var.get(); path=self._selected()
        if path is None:
            messagebox.showerror(self.t("error"),self.t("select")); return
        try:
            level=int(self.level_var.get().strip())
        except ValueError:
            messagebox.showwarning(self.t("error"),self.t("level_invalid")); return
        if level<1:
            messagebox.showwarning(self.t("error"),self.t("level_min")); return
        if not messagebox.askyesno(self.t("confirm"),self.t("level_confirm").format(label=label,level=level)): return
        try:
            backup,old=set_store_level(path,level)
            self._update_selected_info()
            self.status_var.set(self.t("level_done").format(old=old,new=level))
            messagebox.showinfo(self.t("done"),f'{self.t("level_done").format(old=old,new=level)}\n\n{self.t("backup")}\n{backup}')
        except Exception as e:
            messagebox.showerror(self.t("error"),str(e))

if __name__ == "__main__":
    App().mainloop()
