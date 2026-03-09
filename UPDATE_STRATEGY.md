# 📦 Guardian - Update & Versioning Strategy

**Pergunta**: "Agora que Guardian pode ser executado de qualquer máquina via IEX, como faremos as atualizações dele?"

**Resposta**: Sistema de atualização automático com múltiplas estratégias de versionamento.

---

## 🎯 Estratégia de Atualização

### 1. **Três Branches para Diferentes Necessidades**

```
┌─────────────────────────────────────────────────────────┐
│                    VERSIONING STRATEGY                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  📌 MAIN (STABLE)         🚀 DEVELOP (LATEST)  🔧 DEV    │
│  ├─ v0.2.0 (Current)     ├─ v0.3.0-dev        ├─ Alpha  │
│  ├─ Production-ready     ├─ New features      ├─ Exp.   │
│  ├─ Tested thoroughly    ├─ May have bugs     ├─ Caution│
│  └─ Recommended          └─ For testing       └─ Testing│
│                                                           │
└─────────────────────────────────────────────────────────┘
```

#### **MAIN (Stable)**
- ✅ Versão atual: **0.2.0**
- ✅ Production-ready
- ✅ Thoroughly tested
- ✅ **RECOMENDADO** para todos
- 📥 Command: `curl ... | python3` (default)

#### **DEVELOP (Latest)**
- 🚀 Versão: **0.3.0-dev**
- 🚀 Novas features
- ⚠️ Pode ter bugs
- ⚠️ Para early adopters
- 🔗 URL: `...raw.../develop/...`

#### **DEV (Alpha)**
- 🔧 Experimental
- 🔧 Features em desenvolvimento
- ❌ NÃO para produção
- 🔗 URL: `...raw.../dev/...`

---

## 🔄 Como as Atualizações Funcionam

### Sistema 1: **Auto-Update (Em Desenvolvimento)**

```python
# Guardian baixará nova versão automaticamente se disponível
Guardian> update
Checking for updates...
✨ Update available: 0.2.0 → 0.3.0
Branch: latest (experimental)
Install? (y/n): y
📥 Downloading...
✅ Updated successfully
```

### Sistema 2: **Manual Update (Disponível Agora)**

```bash
# Verificar atualizações
python3 update_manager.py check

# Atualizar interativamente
python3 update_manager.py update

# Atualizar de branch específico
python3 update_manager.py update stable    # Recomendado
python3 update_manager.py update latest    # Com testes
python3 update_manager.py update dev       # Experimental
```

### Sistema 3: **Fresh Download (Sempre Funciona)**

```bash
# Baixa versão mais nova do GitHub automaticamente
curl https://raw.githubusercontent.com/0gl1tch/Guardian/main/guardian_standalone.py | python3
```

---

## 📋 Versionamento Semântico

Guardian usa **Semantic Versioning**: `MAJOR.MINOR.PATCH`

```
0.2.0
│ │ │
│ │ └─ PATCH: Bug fixes (0.2.1, 0.2.2...)
│ └─── MINOR: New features (0.3.0, 0.4.0...)
└───── MAJOR: Breaking changes (1.0.0, 2.0.0...)
```

### Roadmap Atual

```
v0.2.0 ✅ (Current)
├─ DFIR forensics
├─ Zero dependencies
├─ IEX delivery
└─ Production-ready

v0.3.0 🚀 (Planned)
├─ Auto-update system
├─ Version checking
├─ Rollback capability
└─ Multi-branch support

v0.4.0 🔭 (Future)
├─ Database integration
├─ Web dashboard
├─ Team collaboration
└─ Advanced analytics

v1.0.0 🎯 (Milestone)
└─ Full enterprise features
```

---

## 🛠️ Update Manager - Uso Completo

### Instalação

```bash
# O update_manager.py já está incluído
# Nenhuma instalação necessária!
```

### Comandos

```bash
# 1. Verificar atualizações
python3 update_manager.py check
# Output: ✨ Update available! 0.2.0 → 0.3.0

# 2. Atualizar (interativo)
python3 update_manager.py update
# Pergunta qual branch deseja

# 3. Atualizar direto (branch específico)
python3 update_manager.py update stable
python3 update_manager.py update latest
python3 update_manager.py update dev

# 4. Fazer rollback (voltar versão anterior)
python3 update_manager.py rollback

# 5. Ver backups disponíveis
python3 update_manager.py list-backups
# Output:
#   1. guardian_backup_0.2.0.py (20.5KB)
#   2. guardian_backup_0.1.9.py (19.8KB)
```

---

## 🔐 Garantias de Segurança

### ✅ Backup Automático
```
Antes de qualquer update:
│
├─ guardian_backup_0.2.0.py (salvo em ~/.guardian/)
├─ Validação de sintaxe
└─ Rollback automático se falhar
```

### ✅ Validação
```
Cada update:
✓ Download completo
✓ Sintaxe Python validada
✓ Backup do anterior
✓ Rollback automático em caso de erro
```

### ✅ Sem Senha
```
Não precisa de sudo:
- Tudo no ~/.guardian/ (seu home)
- Sem acesso privileges necessário
- Seguro para ambientes restritos
```

---

## 📊 Versioning Flow

```
┌──────────────────────────────────────────────────┐
│            Local Execution (IEX)                 │
│  $ curl .../main/guardian_standalone.py | py3   │
└──────────────────────┬───────────────────────────┘
                       │
                ┌──────▼────────┐
                │ Guardian v0.2 │
                └──────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    ✅ Stable    🚀 Latest      🔧 Dev
    (main)     (develop)      (dev)
    v0.2.0     v0.3.0-dev     v0.4.0-alpha
    
    Update? (If available)
        │
        ├─ Manual: python3 update_manager.py update
        ├─ Auto:   Guardian > update
        └─ Fresh:  curl ... | py3 (sempre latest)
```

---

## 🎯 Cenários de Uso

### Cenário 1: Equipe Conservadora (Sem Risco)
```bash
# Use STABLE (main)
curl .../main/guardian_standalone.py | python3

# Nunca atualiza automaticamente
# Atualizações manuais apenas de MAIN
python3 update_manager.py update stable
```

### Cenário 2: Early Adopters (Com Testes)
```bash
# Use LATEST (develop)
curl .../develop/guardian_standalone.py | python3

# Sempre nova versão com mais features
# Teste antes de produção
python3 update_manager.py update latest
```

### Cenário 3: Developers (Cutting Edge)
```bash
# Use DEV branch
curl .../dev/guardian_standalone.py | python3

# Quer contribuir ao desenvolvimento
# Reportar bugs em GitHub Issues
python3 update_manager.py update dev
```

---

## 📈 Fluxo de Atualização do Desenvolvedor

```
1. Desenvolvimento Local
   ├─ Fazer changes em seu Guardian
   └─ Testar localmente

2. Git Push (seu repo/branch)
   ├─ git commit -m "New feature"
   └─ git push origin develop

3. Test in DEVELOP branch
   ├─ Equipe testa em campo
   └─ Report issues

4. Merge para MAIN (quando estável)
   ├─ git pull request
   ├─ Code review
   └─ Merge to main

5. Tag Release
   ├─ git tag v0.3.0
   └─ Atualiza VERSIONS.json

6. Teams auto-update
   ├─ python3 update_manager.py check
   ├─ Vê nova versão 0.3.0
   └─ python3 update_manager.py update stable
```

---

## 🔗 Links de Atualização

### Para Diferentes Branches

```
STABLE (Recomendado):
  curl https://raw.githubusercontent.com/0gl1tch/Guardian/main/guardian_standalone.py | python3

LATEST (Com testes):
  curl https://raw.githubusercontent.com/0gl1tch/Guardian/develop/guardian_standalone.py | python3

DEV (Experimental):
  curl https://raw.githubusercontent.com/0gl1tch/Guardian/dev/guardian_standalone.py | python3
```

---

## ✨ O Que Você Precisa Fazer Agora

### 1. **Criar Branches no GitHub** (1 minuto)
```bash
cd /home/vincius.souza/Guardian

# Criar branch develop
git checkout -b develop
git push -u origin develop

# Criar branch dev
git checkout -b dev
git push -u origin dev

# Voltar para main
git checkout main
```

### 2. **Fazer Push dos Arquivos de Update** (30 segundos)
```bash
# Adicionar update_manager.py
git add update_manager.py VERSIONS.json
git commit -m "Add update system"
git push origin main
```

### 3. **Configurar VERSIONS.json no Repo** (Já pronto)

VERSIONS.json já está criado com:
- Versão atual: 0.2.0
- Branches info
- Changelog
- Release notes

---

## 🎬 Próximos Passos

### Curto Prazo (Agora)
```
✅ Update manager criado
✅ VERSIONS.json configurado
□ Branches (develop, dev) criados
□ Documentação commitada
```

### Médio Prazo (Próximas semanas)
```
□ Testes de auto-update
□ Integração com GitHub Actions (CI/CD)
□ Notificações de atualização
□ Suporte para changelogs automáticos
```

### Longo Prazo (Futuro)
```
□ Checksum verification (SHA256)
□ GPG signing de releases
□ Canary deployments
□ Gradual rollout
□ Feature flags
□ A/B testing
```

---

## 📞 Resumo

**Pergunta Original**: "Como faremos as atualizações dele?"

**Resposta Completa**:

1. ✅ **Três branches** para diferentes níveis de estabilidade
2. ✅ **Update manager** para controle local de versões
3. ✅ **Auto-backup** antes de cada atualização
4. ✅ **Rollback** se algo der errado
5. ✅ **Sempre funciona via IEX** (usa versão do GitHub sempre)
6. ✅ **Sem complicações** de instalação ou dependencies

**Fluxo Simples**:
```
Equipe executa: curl .../main/guardian_standalone.py | python3
↓
Guardian inicia (sempre última versão de main)
↓
Você precisa atualizar? Mude a branch no GitHub!
↓
Próxima execução das pessoas pega versão nova automaticamente
```

---

## 🚀 Próxima Ação

Quer que eu:

1. **Crie os branches no GitHub?** (develop e dev)
2. **Configure CI/CD com GitHub Actions?** (auto-test/auto-release)
3. **Crie um webhook para auto-notify?** (notifica quando há atualizações)
4. **Implemente auto-update dentro do Guardian?** (Guardian > update)

Qual primeiro?
