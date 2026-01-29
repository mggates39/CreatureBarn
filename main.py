"""
CreatureStatBlockParser – version 0.02
Robust Pathfinder stat-block parser.
"""

import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import re
import database
from database import Database

OUTPUT_FIELDS = [
    "Name",
    "CR",
    "XP",
    "Alignment",
    "Size",
    "Type/(sub-type)",
    "Class",
    "Align Type Init",
    "Senses",
    "Aura",
    "AC",
    "HP",
    "Fort",
    "Ref",
    "Will",
    "DR",
    "SR",
    "Immunities",
    "Resistances",
    "Weaknesses",
    "Defensive Abilities",
    "Speed",
    "Space",
    "Reach",
    "Melee",
    "Ranged",
    "Special Attacks",
    "Spell-Like Abilities",
    "Spells Known",
    "Spells Prepared",
    "STR",
    "DEX",
    "CON",
    "INT",
    "WIS",
    "CHA",
    "BAB",
    "CMB",
    "CMD",
    "Feats",
    "Skills",
    "Racial Modifiers",
    "Languages",
    "Special Qualities",
    "Environment",
    "Organization",
    "Treasure",
    "Special Abilities and Content",
]

ALIGNMENTS = ["LG", "NG", "CG", "LN", "N", "CN", "LE", "NE", "CE"]
SIZES = [
    "Fine",
    "Diminutive",
    "Tiny",
    "Small",
    "Medium",
    "Large",
    "Huge",
    "Gargantuan",
    "Colossal",
]


def render(parsed: dict) -> str:
    output = ""
    for field in OUTPUT_FIELDS:
        output += f"{field}: {parsed.get(field,'')}\n"
    return output


def _normalize_case(text: str) -> str:
    parts = [p.strip() for p in text.split(",")]
    return ", ".join(p[:1].upper() + p[1:] for p in parts)


def _normalize_aura(text: str) -> str:
    parts = [p.strip() for p in text.split(",")]
    return ", ".join(p[:1].upper() + p[1:] for p in parts)


def _capture_multiline(section_text: str, field_name: str) -> str:
    pattern = re.compile(rf"{field_name}\s*(.*)", re.I)
    match = pattern.search(section_text)
    if not match:
        return ""
    start_index = match.start(1)
    rest_text = section_text[start_index:]
    lines = rest_text.split("\n")
    captured = []
    for line in lines:
        if re.match(r"^\w+[\s]*:", line) or re.match(
            r"^(AC|HP|Speed|Melee|Spell-Like Abilities|Spells Known|Spells Prepared|STR|Dex|Con|Int|Wis|Cha|Feats|Skills|Languages)\s",
            line,
        ):
            break
        captured.append(line.strip())
    return " ".join(captured).strip()


class CreatureBarn:
    def __init__(self, root):
        self.root = root
        self.root.title("Creature Stat Block Parser")
        self.text = tk.Text(root, wrap="word", width=120, height=45)
        self.text.pack(expand=True, fill="both")

        menu = tk.Menu(root)
        fm = tk.Menu(menu, tearoff=0)
        fm.add_command(label="Open and Parse", command=self.load)
        fm.add_command(label="Exit", command=root.quit)
        menu.add_cascade(label="File", menu=fm)
        dbm = tk.Menu(menu, tearoff=0)
        dbm.add_command(label="Manage Spells")
        dbm.add_command(label="Manage Creatures")
        dbm.add_command(label="Manage NPCs")
        dbm.add_separator()
        dbm.add_command(label="Init Database", command=self.db_init)
        menu.add_cascade(label="Database", menu=dbm)
        root.config(menu=menu)

        self.database = Database('creature_barn.db')

    def load(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        raw = Path(path).read_text(encoding="utf-8")
        parsed = self.parse(raw)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, render(parsed))

    def db_init(self):
        # Connect to SQLite Database and test the connection
        self.database.open_database()
        self.database.test_database()
        self.database.close_database()
    def parse(self, text: str) -> dict:
        r = {field: "" for field in OUTPUT_FIELDS}
        text = re.sub(r"\r\n", "\n", text)
        text = re.sub(r"\n+", "\n", t000000000000000000000000000000000000000000000000000000000000000000000000000000000000ext)

        # --- NAME ---
        name_match = re.match(r"^(.+)", text)
        if name_match:
            r["Name"] = name_match.group(1).strip()

        # --- CR / XP ---
        cr_match = re.search(r"CR\s+([\d/]+)", text, re.IGNORECASE)
        xp_match = re.search(r"XP\s+([\d,]+)", text, re.IGNORECASE)
        if cr_match:
            r["CR"] = f"CR {cr_match.group(1)}"
        if xp_match:
            r["XP"] = xp_match.group(1)

        # --- Alignment / Size / Type / Init / Senses / Aura ---
        align_line = None
        for m in re.finditer(
            r"\b(" + "|".join(ALIGNMENTS) + r")\b.*", text, re.IGNORECASE
        ):
            align_line = m.group(0)
            break
        if align_line:
            type_match = re.match(
                r"(?P<alignment>[LNCEG]{1,2})\s+(?P<size>\w+)?\s+(?P<type>[^\n]+)",
                align_line,
                re.IGNORECASE,
            )
            if type_match:
                r["Alignment"] = type_match.group("alignment").upper()
                r["Size"] = type_match.group("size") or ""
                r["Type/(sub-type)"] = type_match.group("type").strip().title()
            init_match = re.search(r"Init\s+([^\n;]+)", text, re.IGNORECASE)
            senses_match = re.search(
                r"Senses\s+([^;\n]+(?:; Perception [\+\d]+)?)", text, re.IGNORECASE
            )
            aura_match = re.search(r"Aura\s+([^\n]+)", text, re.IGNORECASE)
            init_val = init_match.group(1).strip() if init_match else ""
            r["Align Type Init"] = (
                f"{r['Alignment']} {r['Size']} {r['Type/(sub-type)']} {init_val}".strip()
            )
            r["Senses"] = (
                _normalize_case(senses_match.group(1)) if senses_match else ""
            )
            r["Aura"] = _normalize_aura(aura_match.group(1)) if aura_match else ""

        # --- DEFENSE ---
        defense_section = re.search(
            r"DEFENSE\n(.*?)(?:\n(?:OFFENSE|STATISTICS|SPECIAL ABILITIES|ECOLOGY)|\Z)",
            text,
            re.S | re.I,
        )
        if defense_section:
            lines = defense_section.group(1).split("\n")
            for line in lines:
                line = line.strip()
                # Split by semicolons for multiple inline fields
                parts = [p.strip() for p in line.split(";") if p.strip()]
                for part in parts:
                    # DR
                    if part.upper().startswith("DR"):
                        m = re.match(r"DR\s+(.+)", part, re.I)
                        if m:
                            r["DR"] = m.group(1).strip()
                    # SR
                    elif part.upper().startswith("SR"):
                        m = re.match(r"SR\s+(.+)", part, re.I)
                        if m:
                            r["SR"] = m.group(1).strip()
                    # Immunities
                    elif part.upper().startswith("IMMUNE"):
                        r["Immunities"] = part[len("Immune") :].strip()
                    # Resistances
                    elif part.upper().startswith("RESISTANCES"):
                        r["Resistances"] = part[len("Resistances") :].strip()
                    # Weaknesses
                    elif part.upper().startswith("WEAKNESSES"):
                        r["Weaknesses"] = part[len("Weaknesses") :].strip()
                    # Defensive Abilities
                    elif part.upper().startswith("DEFENSIVE ABILITIES"):
                        r["Defensive Abilities"] = part[
                            len("Defensive Abilities") :
                        ].strip()
                    # AC
                    elif part.upper().startswith("AC"):
                        r["AC"] = part[len("AC") :].strip()
                    # HP
                    elif part.upper().startswith("HP"):
                        r["HP"] = part[len("HP") :].strip()
                    # Fort/Ref/Will
                    else:
                        m = re.findall(r"(Fort|Ref|Will)\s*([+\-]?\d+)", part, re.I)
                        for stat, val in m:
                            r[stat.capitalize()] = val

        # --- OFFENSE ---
        offense_section = re.search(
            r"OFFENSE\n(.*?)(?:\n(?:DEFENSE|STATISTICS|SPECIAL ABILITIES|ECOLOGY)|\Z)",
            text,
            re.S | re.I,
        )
        if offense_section:
            offense_text = offense_section.group(1)
            for key in [
                "Speed",
                "Space",
                "Reach",
                "Melee",
                "Ranged",
                "Special Attacks",
            ]:
                m = re.search(rf"{key}\s+(.+)", offense_text)
                if m:
                    r[key] = m.group(1).strip()
            r["Spell-Like Abilities"] = _capture_multiline(
                offense_text, "Spell-Like Abilities"
            )
            r["Spells Known"] = _capture_multiline(offense_text, "Spells Known")
            r["Spells Prepared"] = _capture_multiline(
                offense_text, "Spells Prepared"
            )

        # --- STATISTICS ---
        stat_section = re.search(
            r"STATISTICS\n(.*?)(?:\n(?:DEFENSE|OFFENSE|SPECIAL ABILITIES|ECOLOGY)|\Z)",
            text,
            re.S | re.I,
        )
        if stat_section:
            stat_text = stat_section.group(1)
            attr_match = re.search(
                r"Str (\d+), Dex (\d+), Con (\d+), Int (\d+), Wis (\d+), Cha (\d+)",
                stat_text,
            )
            if attr_match:
                r["STR"], r["DEX"], r["CON"], r["INT"], r["WIS"], r["CHA"] = (
                    attr_match.groups()
                )
            bc_match = re.search(r"Base Atk \+(\d+); CMB \+(\d+); CMD (\d+)", stat_text)
            if bc_match:
                r["BAB"], r["CMB"], r["CMD"] = bc_match.groups()
            feats = re.search(r"Feats\s+(.+)", stat_text)
            if feats:
                r["Feats"] = feats.group(1).strip()
            skills = re.search(r"Skills\s+(.+)", stat_text)
            if skills:
                r["Skills"] = skills.group(1).strip()
            lang = re.search(r"Languages\s+(.+)", stat_text)
            if lang:
                r["Languages"] = lang.group(1).strip()

        # --- ECOLOGY / SPECIAL ABILITIES ---
        ecology_section = re.search(r"ECOLOGY\n(.*)", text, re.S | re.I)
        if ecology_section:
            eco_text = ecology_section.group(1)
            env = re.search(r"Environment\s+(.+)", eco_text)
            org = re.search(r"Organization\s+(.+)", eco_text)
            treasure = re.search(r"Treasure\s+(.+)", eco_text)
            if env:
                r["Environment"] = env.group(1).strip()
            if org:
                r["Organization"] = org.group(1).strip()
            if treasure:
                r["Treasure"] = treasure.group(1).strip()
            special_lines = []
            for line in eco_text.split("\n"):
                if not any(
                    line.startswith(f)
                    for f in ["Environment", "Organization", "Treasure"]
                ):
                    special_lines.append(line.strip())
            r["Special Abilities and Content"] = "\n".join(special_lines).strip()

        return r


if __name__ == "__main__":
    rootWidget = tk.Tk()
    app = CreatureBarn(rootWidget)
    rootWidget.mainloop()
