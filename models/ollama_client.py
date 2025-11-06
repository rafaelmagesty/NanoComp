import ollama
from models.base_client import BaseClient


class OllamaClient(BaseClient):
    """Cliente para uso com modelos Ollama locais."""

    def __init__(self, model_version: str = "llama3", templates_dir=None):
        super().__init__(templates_dir=templates_dir)
        self.model_version = model_version
        self.client = ollama

    def generate_prompt(self, template: str, **kwargs):
        """Formata o template e extrai seções para mensagens do chat."""
        formatted = super().generate_prompt(template, **kwargs)
        
        # Extrai blocos
        system = self.find_pattern(formatted, "SYSTEM_CONFIG")[0]
        user1 = self.find_pattern(formatted, "USER_CONFIG")[0]
        
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user1},
        ]
        
        # Para templates com exemplo (one-shot ou few-shot)
        assistant_matches = self.find_pattern(formatted, "ASSISTANT_CONFIG")
        user_matches = self.find_pattern(formatted, "USER_CONFIG")
        
        if assistant_matches:
            messages.append({"role": "assistant", "content": assistant_matches[0]})
            if len(user_matches) > 1:
                messages.append({"role": "user", "content": user_matches[1]})
        
        return messages

    def process(self, args=None, **overrides):
        """Processa um prompt usando o modelo Ollama."""
        # Combina args com overrides
        if args is None:
            args = {}
        if hasattr(args, '__dict__'):
            payload = vars(args).copy()
        elif isinstance(args, dict):
            payload = args.copy()
        else:
            payload = {}
        
        payload.update(overrides)
        
        # Extrai parâmetros
        prompt_name = payload.get("PROMPT")
        if not prompt_name:
            raise ValueError("É necessário informar 'PROMPT' no args ou overrides")
        
        model_version = payload.get("VERSION") or payload.get("MODEL_VERSION") or self.model_version
        input_path = payload.get("INPUT_PATH")
        
        # Carrega template e prepara mensagens
        template = self.load_template(prompt_name)
        
        # Se houver INPUT_PATH, carrega o conteúdo
        if input_path:
            payload.setdefault("INPUT_SEQUENCE", self.get_input_code(input_path))
        
        # Remove PROMPT do payload pois já foi usado para carregar o template
        # e não é necessário para substituição de placeholders
        payload_for_prompt = {k: v for k, v in payload.items() if k != "PROMPT"}
        
        messages = self.generate_prompt(
            template=template,
            **payload_for_prompt
        )
        
        # Chama o Ollama
        resp = self.client.chat(model=model_version, messages=messages)
        return resp["message"]["content"]

