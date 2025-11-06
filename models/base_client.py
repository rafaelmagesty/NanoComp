import os
import re
from pathlib import Path
from typing import Any, Dict, List


class BaseClient:
    """Classe base para carregar templates e processar prompts."""

    def __init__(self, templates_dir=None):
        if templates_dir is None:
            root = os.path.abspath(os.path.join(__file__, "..", ".."))
            self.templates_dir = Path(root) / "templates"
        else:
            self.templates_dir = Path(templates_dir)

    def load_template(self, file_name: str) -> str:
        """Carrega o conteúdo de um arquivo de template."""
        path = self.templates_dir / f"{file_name}.txt"
        if not path.exists():
            raise FileNotFoundError(f"Template file not found at: {path}")
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            raise IOError(f"Error loading template {file_name}: {e}")

    def get_input_code(self, file_path: str) -> str:
        """Lê o conteúdo de um arquivo de código de entrada."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return f"ERROR: File not found at '{file_path}'"
        except Exception as e:
            return f"ERROR: {e}"

    def find_pattern(self, text: str, flag: str) -> List[str]:
        """Encontra e retorna o conteúdo delimitado por {FLAG} e {FLAG_END} em um texto."""
        pattern = rf"{{{flag}}}(.*?){{{flag}_END}}"
        matches = re.findall(pattern, text, re.DOTALL)
        return [match.strip() for match in matches]

    def generate_request_dict(self, role: str, content: str) -> Dict[str, str]:
        """Gera um dicionário formatado para uma mensagem de chat."""
        return {"role": role, "content": content}

    def generate_prompt(self, template: str, **kwargs: Any) -> str:
        """Substitui placeholders dinâmicos no template, preservando marcações de seção."""
        formatted = template
        for key, val in kwargs.items():
            # Escapa chaves literais nos valores para evitar conflitos
            if isinstance(val, str):
                val = val.replace("{", "TEMP_OPEN_BRACE_").replace("}", "_TEMP_CLOSE_BRACE")
            # Substitui o placeholder no template
            formatted = formatted.replace(f"{{{key}}}", str(val))
        # Restaura as chaves literais nos valores após a substituição
        formatted = formatted.replace("TEMP_OPEN_BRACE_", "{").replace("_TEMP_CLOSE_BRACE", "}")
        return formatted

