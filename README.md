# Agente de Integração Fiscal – Documentação Técnica Completa

## 1. Visão Geral

O **Agente de Integração Fiscal** é um aplicativo desktop desenvolvido em Python que monitora automaticamente uma pasta de arquivos XML e envia novos documentos para uma API remota.

O agente foi projetado para funcionar como um **software de integração contínua**, semelhante a agentes de sincronização como Dropbox ou OneDrive.

### Principais funcionalidades

* Configuração inicial guiada
* Monitoramento automático de arquivos XML
* Envio automático para API
* Execução em segundo plano
* Ícone na bandeja do Windows
* Logs em tempo real
* Reconfiguração a qualquer momento
* Detecção instantânea de novos arquivos
* Preparado para geração de executável (.exe)

---

# 2. Arquitetura do Projeto

A aplicação foi organizada em uma arquitetura modular para facilitar manutenção e evolução.

```
Agente_SaaS/

main.py

config/
    config_manager.py

core/
    monitor_xml.py
    enviar_xml.py

ui/
    interface.py

tray/
    tray_icon.py

config.json
```

## Descrição dos módulos

### main.py

Ponto de entrada da aplicação.

Responsável apenas por iniciar a interface gráfica.

### config/

Gerenciamento da configuração da aplicação.

Arquivo principal:

* `config_manager.py`

Funções:

* salvar configuração
* carregar configuração
* verificar se configuração já existe

### core/

Camada de lógica do sistema.

Contém:

#### monitor_xml.py

Responsável por:

* monitorar pasta de XML
* detectar novos arquivos
* disparar envio para API

#### enviar_xml.py

Responsável por:

* enviar arquivo XML para a API
* tratar erros de envio
* registrar logs

### ui/

Interface gráfica do agente.

Arquivo principal:

```
interface.py
```

Responsável por:

* telas de configuração
* tela principal
* exibição de logs
* iniciar e parar agente
* abrir configurações

### tray/

Gerenciamento do ícone na bandeja do Windows.

Arquivo:

```
tray_icon.py
```

Funções:

* criar ícone do sistema
* permitir abrir painel
* manter agente rodando em background

---

# 3. Fluxo de Funcionamento

## Primeira execução

1. Usuário abre o programa
2. Sistema detecta que não existe `config.json`
3. Interface abre tela de configuração
4. Usuário informa:

* CNPJ
* Token da API
* URL da API
* Pasta onde os XML serão monitorados

5. Configuração é salva

```
config.json
```

6. Interface principal é aberta
7. Agente inicia automaticamente

---

## Execuções seguintes

Quando o sistema inicia novamente:

1. Detecta `config.json`
2. Carrega configurações automaticamente
3. Abre interface principal
4. Inicia monitoramento automaticamente

---

# 4. Monitoramento de XML

O monitoramento é feito utilizando a biblioteca:

```
watchdog
```

Essa biblioteca usa eventos do sistema operacional para detectar novos arquivos.

### Vantagens

* detecção instantânea
* não precisa loop
* não precisa sleep
* baixo consumo de CPU

### Fluxo

```
novo XML aparece
↓
watchdog detecta evento
↓
arquivo enviado para API
↓
log registrado
```

---

# 5. Envio de XML para API

O envio é feito via HTTP utilizando a biblioteca `requests`.

Formato da requisição:

```
POST /api

Headers:
Authorization: Bearer TOKEN

FormData:
arquivo = XML
cnpj = CNPJ
```

### Exemplo

```
requests.post(
    api_url,
    files={"arquivo": xml},
    data={"cnpj": cnpj},
    headers={"Authorization": "Bearer TOKEN"}
)
```

---

# 6. Sistema de Logs

Todos os eventos são exibidos na interface.

Exemplos:

```
Configuração salva
Monitorando pasta: C:/xml
XML detectado: nota123.xml
nota123.xml enviado -> OK
Erro envio: timeout
```

Logs ajudam a diagnosticar:

* erro de API
* erro de rede
* pasta inexistente
* XML inválido

---

# 7. Execução em Segundo Plano

Quando o usuário fecha a janela:

```
janela não é encerrada
↓
janela é ocultada
↓
agente continua rodando
```

Isso permite que o sistema continue funcionando.

O agente pode ser reaberto pelo **ícone na bandeja do Windows**.

---

# 8. Ícone na Bandeja do Windows

A aplicação utiliza a biblioteca:

```
pystray
```

Funcionalidades:

* manter agente ativo
* permitir abrir painel
* permitir sair do sistema

Menu do ícone:

```
Abrir Painel
Sair
```

---

# 9. Arquivo de Configuração

Arquivo:

```
config.json
```

Exemplo:

```
{
    "cnpj": "12345678000199",
    "token": "TOKEN_API",
    "api_url": "http://localhost:8000/upload",
    "pasta_xml": "C:/xml"
}
```

Campos:

| Campo     | Descrição             |
| --------- | --------------------- |
| cnpj      | CNPJ da empresa       |
| token     | Token de autenticação |
| api_url   | URL da API            |
| pasta_xml | Pasta monitorada      |

---

# 10. Instalação do Ambiente

Instalar Python 3.10 ou superior.

Instalar dependências:

```
pip install requests watchdog pystray pillow
```

---

# 11. Executando o Sistema

Rodar a aplicação:

```
python main.py
```

---

# 12. Gerar Executável (.exe)

Instalar PyInstaller:

```
pip install pyinstaller
```

Gerar executável:

```
pyinstaller --noconsole --onefile main.py
```

O executável será criado em:

```
dist/main.exe
```

---

# 13. Iniciar com Windows

Para iniciar automaticamente com Windows:

1. Pressionar:

```
Win + R
```

2. Digitar:

```
shell:startup
```

3. Copiar o executável para essa pasta.

Agora o agente iniciará automaticamente.

---

# 14. Reconfiguração do Sistema

O usuário pode alterar configurações a qualquer momento.

Basta clicar:

```
⚙ Configurações
```

Na interface.

---

# 15. Possíveis Problemas

## XML não está sendo enviado

Verificar:

* pasta correta
* API funcionando
* token válido

---

## API retorna erro

Verificar:

* endpoint correto
* autenticação

---

## XML não é detectado

Verificar:

* extensão `.xml`
* permissão da pasta

---

# 16. Melhorias Futuras

Possíveis evoluções do sistema:

* atualização automática do agente
* criptografia do token
* fila de processamento
* painel web de monitoramento
* logs em arquivo
* instalador profissional
* execução como serviço do Windows

---

# 17. Licença

Uso interno ou comercial conforme necessidade do projeto.

---

# 18. Autor

Sistema desenvolvido como agente de integração fiscal automatizado em Python.
