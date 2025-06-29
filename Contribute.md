# Guia de Contribuição

Obrigado por considerar contribuir para o projeto Chat! Estamos muito felizes em tê-lo(a) aqui. Este guia irá ajudá-lo(a) a começar a contribuir.

## 📋 Tabela de Conteúdo

- [Código de Conduta](#-código-de-conduta)
- [Como Posso Ajudar?](#-como-posso-ajudar)
- [Encontrando Issues para Trabalhar](#-encontrando-issues-para-trabalhar)
- [Configurando o Ambiente de Desenvolvimento](#-configurando-o-ambiente-de-desenvolvimento)
- [Processo de Pull Request](#-processo-de-pull-request)
- [Padrões de Código](#-padrões-de-código)
- [Testes](#-testes)
- [Reportando Bugs](#-reportando-bugs)
- [Solicitando Recursos](#-solicitando-recursos)
- [Perguntas Frequentes](#-perguntas-frequentes)

## 🤝 Código de Conduta

Este projeto e todos os participantes estão sujeitos ao nosso [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, esperamos que você mantenha este código. Por favor, relate comportamentos inaceitáveis para [seu-email@exemplo.com](mailto:seu-email@exemplo.com).

## 💡 Como Posso Ajudar?

Existem várias maneiras de contribuir para o projeto:

- **Relatar bugs** - Use a [página de issues](https://github.com/Henriquehnnm/Chat/issues) para relatar bugs
- **Discutir o código** - Participe das discussões sobre recursos, design, etc.
- **Enviar correções** - Corrija erros de digitação, adicione documentação ou resolva bugs
- **Solicitar recursos** - Sugira novos recursos ou melhorias
- **Traduzir** - Ajude a traduzir o aplicativo para outros idiomas
- **Escrever tutoriais** - Crie tutoriais ou exemplos de como usar o aplicativo
- **Compartilhe** - Conte aos outros sobre o projeto

## 🔍 Encontrando Issues para Trabalhar

Problemas marcados com as seguintes tags são ótimos para começar:

- `good first issue` - Ótimo para iniciantes
- `help wanted` - Precisa de ajuda
- `bug` - Relatos de bugs que precisam ser corrigidos

## 🛠 Configurando o Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.8+
- Git
- pip (gerenciador de pacotes do Python)

### Passos para Configuração

1. **Faça um Fork do repositório**
   ```bash
   # Navegue até a pasta onde deseja clonar o repositório
   git clone https://github.com/seu-usuario/Chat.git
   cd Chat
   ```

2. **Configure o repositório remoto**
   ```bash
   git remote add upstream https://github.com/Henriquehnnm/Chat.git
   ```

3. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Se houver dependências de desenvolvimento
   ```

5. **Execute os testes**
   ```bash
   pytest
   ```

## 🔄 Processo de Pull Request

1. **Atualize sua branch principal**
   ```bash
   git checkout main
   git pull upstream main
   ```

2. **Crie uma branch para sua feature/correção**
   ```bash
   git checkout -b feature/nome-da-feature
   # ou
   git checkout -b bugfix/descricao-do-bug
   ```

3. **Faça commit das suas alterações**
   ```bash
   git add .
   git commit -m "Descrição clara e concisa das alterações"
   ```

4. **Envie para o seu fork**
   ```bash
   git push origin nome-da-sua-branch
   ```

5. **Crie um Pull Request**
   - Vá até a página do seu fork no GitHub
   - Clique em "Compare & pull request"
   - Preencha o template do PR com as informações solicitadas
   - Adicione screenshots ou gifs se aplicável
   - Clique em "Create pull request"

## 📝 Padrões de Código

- Siga o [PEP 8](https://www.python.org/dev/peps/pep-0008/) para código Python
- Use docstrings seguindo o padrão Google
- Escreva mensagens de commit claras e descritivas
- Mantenha as linhas com no máximo 88 caracteres (configuração do Black)

## 🧪 Testes

Certifique-se de que todos os testes passem antes de enviar um PR:

```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=src tests/
```

## 🐛 Reportando Bugs

Use o [issue tracker](https://github.com/Henriquehnnm/Chat/issues) para relatar bugs. Inclua:

1. Um resumo claro e descritivo do problema
2. Passos para reproduzir o problema
3. Comportamento esperado vs. comportamento atual
4. Capturas de tela ou gifs, se aplicável
5. Sua configuração (SO, versão do Python, etc.)

## ✨ Solicitando Recursos

Adoraríamos ouvir suas sugestões de novos recursos! Por favor:

1. Verifique se o recurso já não foi solicitado
2. Explique por que este recurso seria útil
3. Inclua exemplos de como o recurso funcionaria

## ❓ Perguntas Frequentes

### Como faço para começar a contribuir?

Comece olhando as issues com a tag `good first issue`. São problemas mais simples, ótimos para quem está começando.

### Como faço para propor uma mudança grande?

Para mudanças significativas, abra primeiro uma issue para discutir a proposta antes de começar a trabalhar nela.

### Como posso entrar em contato com os mantenedores?

Você pode abrir uma issue ou nos contatar por email em [seu-email@exemplo.com](mailto:seu-email@exemplo.com).

---

Obrigado por ajudar a tornar este projeto melhor! Sua contribuição é muito valiosa para nós. 💜
