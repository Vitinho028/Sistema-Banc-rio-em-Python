# 🏦 Sistema Bancário em Python

Sistema bancário de linha de comando desenvolvido em Python com persistência de dados via SQLite. Permite criar contas, realizar operações financeiras e consultar histórico de transações.

---

## 📋 Funcionalidades

- **Cadastro de conta** — cria uma nova conta com nome e CPF
- **Login por CPF** — acesso autenticado com validação de 11 dígitos
- **Depósito** — adiciona saldo à conta e registra a transação
- **Saque** — retira saldo com verificação de limite disponível
- **Extrato** — exibe histórico completo de transações
- **Empréstimo** — solicita crédito que é creditado ao saldo
- **Pagamento de empréstimo** — quita parcial ou totalmente o empréstimo
- **Exclusão de conta** — remove permanentemente os dados da conta

---

## 🗂️ Estrutura do Banco de Dados

O sistema utiliza SQLite e cria automaticamente o arquivo `banco.db` com 4 tabelas:

| Tabela              | Descrição                                      |
|---------------------|------------------------------------------------|
| `contas_bancarias`  | Dados do titular, CPF e saldo                  |
| `transacoes`        | Histórico de depósitos e saques                |
| `emprestimos`       | Registro de empréstimos concedidos             |
| `pagamentos`        | Registro de pagamentos de empréstimos          |

---

## 🚀 Como executar

### Pré-requisitos

- Python 3.7 ou superior
- Nenhuma biblioteca externa necessária (usa apenas módulos da biblioteca padrão)

### Executando o sistema

```bash
python banco.py
```

O arquivo `banco.db` será criado automaticamente na mesma pasta.

---

## 🖥️ Como usar

Ao iniciar, o sistema pede o CPF:

```
Bem-vindo ao sistema bancário!
Digite seu CPF (apenas números): 12345678901
```

- Se o CPF **já existir**, o acesso é concedido diretamente.
- Se o CPF **não existir**, o sistema oferece criar uma nova conta.

Após o login, o menu principal é exibido:

```
========== MENU ==========
  [1] Ver dados da conta
  [2] Depositar
  [3] Sacar
  [4] Extrato
  [5] Solicitar empréstimo
  [6] Pagar empréstimo
  [7] Excluir conta
  [0] Sair
===========================
```

---

## 📁 Estrutura dos arquivos

```
.
├── banco.py       # Código principal do sistema
├── banco.db       # Banco de dados SQLite (gerado automaticamente)
└── README.md      # Este arquivo
```

---

## ⚠️ Observações

- O CPF deve conter exatamente **11 dígitos numéricos** (sem pontos ou traços).
- Cada CPF é único no sistema — não é possível cadastrar dois titulares com o mesmo CPF.
- Valores de depósito, saque, empréstimo e pagamento devem ser **maiores que zero**.
- O saldo não pode ficar negativo — saques e pagamentos são bloqueados se o saldo for insuficiente.
- A exclusão de conta é **irreversível**.

---

## 🛠️ Tecnologias utilizadas

- **Python 3** — linguagem principal
- **SQLite3** — banco de dados embutido (módulo nativo do Python)
- **datetime** — registro de data e hora das operações
