# Guardian - GitHub Auto-Deploy Guide

## Setup Rápido (2 minutos)

Se você quer automatizar o deploy do Guardian no GitHub, aqui estão duas formas de fazer.

---

## Pré-requisitos

Você precisa ter:
- ✅ GitHub CLI (`gh`) instalado
- ✅ Autenticado no GitHub (`gh auth login`)
- ✅ Python 3.10+ instalado

### Instalar GitHub CLI

**Windows (PowerShell):**
```powershell
choco install gh
# ou
winget install GitHub.cli
```

**macOS:**
```bash
brew install gh
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install gh

# Fedora/RHEL
sudo dnf install gh

# Arch
pacman -S github-cli
```

### Autenticar no GitHub

```bash
gh auth login
# Siga as instruções (selecione HTTPS)
```

---

## Método 1: Python (Recomendado)

Mais robusto, melhor tratamento de erros.

### Executar

```bash
cd /home/vincius.souza/Guardian
python3 github_deploy.py
```

### Opções

```bash
# Repository name customizado
python3 github_deploy.py --repo MyGuardian

# Com descrição customizada
python3 github_deploy.py --repo MyTool --description "My custom description"
```

---

## Método 2: Bash (Simples)

Para quem prefere shell script.

### Executar

```bash
cd /home/vincius.souza/Guardian
bash github_deploy.sh
```

### Opções

```bash
# Repository name customizado
bash github_deploy.sh MyGuardian
```

---

## O Que Cada Script Faz

Ambos os scripts fazem isto **automaticamente**:

1. ✅ Valida instalação do GitHub CLI
2. ✅ Valida autenticação no GitHub
3. ✅ Obtém seu username do GitHub
4. ✅ Inicializa repositório git local
5. ✅ Cria repositório no GitHub
6. ✅ Faz commit de todos os arquivos
7. ✅ Faz push para GitHub
8. ✅ Gera os one-liners prontos para usar

**Resultado**: URL pronta para compartilhar via IEX

---

## Passo-a-Passo Manual (Se preferir)

Se não quiser usar os scripts, pode fazer manualmente:

### 1. Inicializar repositório local

```bash
cd /home/vincius.souza/Guardian
git init
git config user.name "your-username"
git config user.email "your-email@github.com"
git add .
git commit -m "Initial Guardian deployment"
```

### 2. Criar repositório no GitHub

```bash
# Usar GitHub CLI para criar
gh repo create Guardian --public --push --source=. --remote=origin

# Ou criar manualmente no GitHub web:
# https://github.com/new
```

### 3. Fazer push

```bash
git remote add origin https://github.com/your-username/Guardian.git
git branch -M main
git push -u origin main
```

---

## Após o Deploy - Próximas Etapas

Uma vez deployado, você terá:

### URL Raw (para IEX)
```
https://raw.githubusercontent.com/YOUR-USERNAME/Guardian/main/guardian_standalone.py
```

### One-Liners para Compartilhar

**Windows:**
```powershell
iex(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/YOUR-USERNAME/Guardian/main/guardian_standalone.py')
```

**Linux/macOS:**
```bash
curl https://raw.githubusercontent.com/YOUR-USERNAME/Guardian/main/guardian_standalone.py | python3
```

### Documentação no Repositório

- `README.md` - Documentação principal
- `DEPLOY.md` - Quick start
- `REMOTE_EXECUTION.md` - Detalhes técnicos
- `guardian_standalone.py` - A ferramenta
- `server.py` - Servidor HTTP (opcional)

---

## Troubleshooting

### Erro: "GitHub CLI not found"

```bash
# Instale GitHub CLI
# Windows
winget install GitHub.cli

# macOS
brew install gh

# Linux
sudo apt install gh  # ou seu gerenciador de pacotes
```

### Erro: "Not authenticated"

```bash
# Faça login
gh auth login
```

### Erro: "Repository already exists"

O script vai perguntar se quer sobrescrever. Responda `y` ou `n`.

### Erro: Git não funcionando

```bash
# Certifique-se que git está instalado
git --version

# Se não estiver, instale:
# Windows: https://git-scm.com
# macOS: brew install git
# Linux: sudo apt install git
```

---

## Verificar se deu certo

Após executar o script, seu repositório deve estar em:

```
https://github.com/YOUR-USERNAME/Guardian
```

E você deve ver os arquivos:
- guardian_standalone.py ✅
- README.md ✅
- DEPLOY.md ✅
- etc.

---

## Customizações (Avançado)

### Mudar para repositório privado

Se quiser privado, edite o script:

**Em `github_deploy.py`, linha ~76:**
```python
'--public',  # Mude para '--private'
```

**Em `github_deploy.sh`, linha ~130:**
```bash
--public \  # Mude para --private
```

### Mudar branch padrão

Se quiser usar `develop` ao invés de `main`:

```bash
git branch -M develop
git push -u origin develop --force
```

---

## Quick Reference

```bash
# Python (recomendado)
python3 github_deploy.py

# Bash
bash github_deploy.sh MyRepoName

# Manual
cd Guardian
git init
git add .
git commit -m "Initial"
gh repo create Guardian --public --push --source=. --remote=origin
```

---

## Proximas Etapas

Depois que o repositório estiver pronto:

1. **Compartilhe o one-liner** com sua equipe
2. **Teste em outra máquina** para validar
3. **Documente** como usar no seu contexto
4. **Implemente** em seus workflows

---

## Support

Se tiver dúvidas:

1. Verifique se tem `gh` CLI instalado: `gh --version`
2. Verifique autenticação: `gh auth status`
3. Rode um dos scripts
4. Procure os erros específicos acima

---

**Pronto para fazer deploy?** Escolha um método:

```bash
# Python (com mais informações)
python3 github_deploy.py

# Bash (mais rápido)
bash github_deploy.sh
```

Tudo será criado automaticamente! 🚀
