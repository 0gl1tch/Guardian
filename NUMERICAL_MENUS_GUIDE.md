# 🎯 Guardian - Numerical Menu System Guide

**Versão**: 0.2.0  
**Data**: 9 de Março de 2024  
**Objetivo**: Simplificar o acesso a todas as funções do Guardian através de menus numéricos

---

## 📋 Três Menus Numéricos Disponíveis

Guardian agora possui **3 sistemas de menu numérico** para facilitar o acesso a todas funções:

### 1️⃣ **Guardian Tools** (Python)
```bash
python3 guardian_tools.py
```

**Funções** (0-9):
- 1️⃣ Check for Updates
- 2️⃣ Update Guardian (Stable)
- 3️⃣ Update Guardian (Latest)
- 4️⃣ Update Guardian (Dev)
- 5️⃣ Rollback to Previous Version
- 6️⃣ List Available Backups
- 7️⃣ Run Guardian
- 8️⃣ View Update Strategy
- 9️⃣ View Version Info
- 0️⃣ Exit

---

### 2️⃣ **Deploy Menu** (Bash)
```bash
bash deploy_menu.sh
```

**Funções** (0-9):
- 1️⃣ Quick Deploy (Fastest - 30 sec)
- 2️⃣ Full Deploy with Details (Python)
- 3️⃣ Bash-only Deploy
- 4️⃣ Setup Update Branches
- 5️⃣ Check GitHub Authentication
- 6️⃣ Install GitHub CLI
- 7️⃣ Get Repository Info
- 8️⃣ Test IEX Commands
- 9️⃣ View Deployment Documentation
- 0️⃣ Exit

---

### 3️⃣ **Update Menu** (Bash)
```bash
bash update_menu.sh
```

**Funções** (0-12):

#### Update Manager (1-6):
- 1️⃣ Check for Updates
- 2️⃣ Update Guardian (Interactive)
- 3️⃣ Update from Stable Branch
- 4️⃣ Update from Latest Branch
- 5️⃣ Update from Dev Branch
- 6️⃣ Rollback to Previous Version

#### Setup & Configuration (7-9):
- 7️⃣ Setup Update Branches
- 8️⃣ Install Update Manager Dependencies
- 9️⃣ Verify Update System

#### Information (10-12):
- 🔟 View Version Information
- 1️⃣1️⃣ View Update Strategy
- 1️⃣2️⃣ List All Backups

---

## 🚀 Quick Start (Choose Your Path)

### Path 1: Deploy Guardian (First Time)
```bash
# Option A: Fastest deployment
bash deploy_menu.sh
# Then select: 1

# Option B: Full control
bash deploy_menu.sh
# Then select: 2 (Python) or 3 (Bash)
```

### Path 2: Manage Updates (After Deployment)
```bash
bash update_menu.sh
# Select desired update option (1-6)
```

### Path 3: Local Management (Your Machine)
```bash
python3 guardian_tools.py
# Select desired option (0-9)
```

---

## 📊 Menu Hierarchy

```
Guardian Menus
│
├─ guardian_tools.py       [Local Management]
│  ├─ 1. Check Updates
│  ├─ 2-4. Update (different branches)
│  ├─ 5. Rollback
│  ├─ 6. List Backups
│  ├─ 7. Run Guardian
│  ├─ 8-9. Info/Docs
│  └─ 0. Exit
│
├─ deploy_menu.sh          [Deployment]
│  ├─ 1-3. Deploy (different methods)
│  ├─ 4. Setup Branches
│  ├─ 5-6. GitHub Tools
│  ├─ 7. Repo Info
│  ├─ 8-9. Testing/Docs
│  └─ 0. Exit
│
└─ update_menu.sh          [Updates & Setup]
   ├─ 1-6. Update Management
   ├─ 7-9. Setup & Install
   ├─ 10-12. Information
   └─ 0. Exit
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Você quer atualizar Guardian
```bash
$ bash update_menu.sh
Select option: 3
# Updates to stable branch automatically ✅
```

### Exemplo 2: Você quer testar a branch latest
```bash
$ bash update_menu.sh
Select option: 4
# Updates to latest with new features ✅
```

### Exemplo 3: Você quer fazer rollback
```bash
$ bash update_menu.sh
Select option: 6
# Rolls back to previous version ✅
```

### Exemplo 4: Deploy pela primeira vez
```bash
$ bash deploy_menu.sh
Select option: 1
# Quick deployment to GitHub in 30 seconds ✅
```

### Exemplo 5: Você quer gerenciar localmente
```bash
$ python3 guardian_tools.py
Select option: 1
# Check for updates ✅
Select option: 7
# Run Guardian ✅
```

---

## 🎯 Use Cases por Menu

| Necessidade | Menu | Opção |
|-----------|------|-------|
| Deploy Guardian no GitHub | deploy_menu.sh | 1 ou 2 |
| Atualizar para stable | update_menu.sh | 3 |
| Atualizar para latest | update_menu.sh | 4 |
| Testar dev branch | update_menu.sh | 5 |
| Fazer rollback | update_menu.sh | 6 |
| Setup branches develop/dev | update_menu.sh | 7 |
| Verificar sistema | update_menu.sh | 9 |
| Rodar Guardian | guardian_tools.py | 7 |
| Verificar atualizações | guardian_tools.py ou update_menu.sh | 1 |
| Ver documentação | deploy_menu.sh | 9 |

---

## 🔄 Fluxo Recomendado

### Primeira Vez (Setup Completo)
```bash
1. bash deploy_menu.sh
2. Selecione: 1 (Quick Deploy)
3. Aguarde ~30 segundos
4. Seu Guardian está no GitHub! 🎉
```

### Depois (Manutenção Regular)
```bash
1. bash update_menu.sh
2. Selecione: 1 (Check for Updates)
3. Se houver atualizações:
   - Selecione: 3 (Update Stable)
4. Pronto! ✅
```

### Quando Algo Quebrar
```bash
1. bash update_menu.sh
2. Selecione: 6 (Rollback)
3. Guardian volta à versão anterior ✅
```

---

## 🛡️ Segurança dos Menus

Todos os menus:
- ✅ Pedem confirmação antes de ações destrutivas
- ✅ Validam dependências antes de executar
- ✅ Mostram warnings para operações de risco
- ✅ Não precisam de sudo
- ✅ Têm rollback automático

---

## 🆘 Troubleshooting

### "Command not found: guardian_tools.py"
```bash
# Certifique-se que está no diretório Guardian
cd /home/vincius.souza/Guardian

# Ou use o caminho completo
python3 /home/vincius.souza/Guardian/guardian_tools.py
```

### "Permission denied"
```bash
# Os scripts devem ser executáveis
chmod +x guardian_tools.py deploy_menu.sh update_menu.sh
```

### "Python not found"
```bash
# Instale Python 3.10+
sudo apt install python3

# Ou use outro gerenciador de pacotes
```

### "GitHub CLI not found"
```bash
# Use o deploy_menu.sh para instalar
bash deploy_menu.sh
# Selecione: 6
```

---

## 📚 Combinando com Documentação

Cada menu tem links para documentação:

```
Deploy Menu
  └─ Opção 9: View Documentation
     ├─ START_HERE.md
     ├─ GITHUB_DEPLOY.md
     ├─ DEPLOYMENT_CHECKLIST.md
     ├─ READY_TO_DEPLOY.md
     └─ IEX_READY.md

Guardian Tools
  └─ Opção 8: View Update Strategy
     └─ UPDATE_STRATEGY.md

Update Menu
  └─ Opção 11: View Update Strategy
     └─ UPDATE_STRATEGY.md
```

---

## ✨ Benefícios do Sistema Numérico

✅ **Rápido** - Não precisa lembrar comandos longos  
✅ **Intuitivo** - Menu visual com números  
✅ **Seguro** - Confirmações antes de ações  
✅ **Completo** - Todas funções em um lugar  
✅ **Documentado** - Cada opção tem ajuda integrada  
✅ **Cross-platform** - Funciona em Windows/Mac/Linux  

---

## 🎬 Próximas Vezes

Depois que estiver familiarizado com os menus numéricos, você pode:

1. Usar scripts diretamente (sem menu):
   ```bash
   python3 update_manager.py check
   python3 update_manager.py update stable
   ```

2. Integrar com cron/scheduler:
   ```bash
   # Verificar atualizações diariamente
   0 9 * * * /home/user/Guardian/update_menu.sh << echo 1
   ```

3. Usar em scripts de automação:
   ```bash
   # Deploy automático
   bash deploy_menu.sh << echo 1
   ```

---

## 📞 Resumo Rápido

| Tarefa | Comando |
|--------|---------|
| Deploy rápido | `bash deploy_menu.sh` → 1 |
| Atualizar | `bash update_menu.sh` → 3 |
| Fazer rollback | `bash update_menu.sh` → 6 |
| Rodar Guardian | `python3 guardian_tools.py` → 7 |
| Verificar system | `bash update_menu.sh` → 9 |
| Ver docs | `bash deploy_menu.sh` → 9 |

---

## 🚀 Conclusão

Os **3 menus numéricos** deixam Guardian ainda mais fácil de usar:

- **guardian_tools.py** - Para gerenciamento local
- **deploy_menu.sh** - Para deployment
- **update_menu.sh** - Para atualizações e setup

Escolha seu menu, selecione um número, e pronto! ✅

---

**Dúvidas?** Consulte:
- [IEX_READY.md](IEX_READY.md) - Como executar via IEX
- [UPDATE_STRATEGY.md](UPDATE_STRATEGY.md) - Estratégia de atualizações
- [START_HERE.md](START_HERE.md) - Guia rápido

🛡️ **Guardian - Simples, Poderoso, Confiável**
