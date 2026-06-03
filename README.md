# Análise Detalhada do Arquivo `chaves/models.py`

Este documento fornece uma explicação linha por linha do modelo `Chave` e suas validações do projeto ChaveMaster.

## 1. Importações

```python
from django.core.exceptions import ValidationError
from django.db import models
```

- **`from django.core.exceptions import ValidationError`**  
  Importa a exceção `ValidationError` do Django, usada para sinalizar erros de validação de modelo (por exemplo em `clean()`).

- **`from django.db import models`**  
  Importa o módulo `models` do Django que contém as classes base para definir modelos (ex.: `Model`, `CharField`, `ForeignKey`).

## 2. Classe `Chave` (Modelo Principal)

```python
class Chave(models.Model):
```

Declara a classe de modelo `Chave` que herda de `models.Model`. Cada instância representa uma linha na tabela de chaves no banco de dados.

### 2.1. Enumeração de Tipos de Chave

```python
class TipoChave(models.TextChoices):
    SALA = 'sala', 'Chave de sala'
    PREDIO = 'predio', 'Chave de predio'
```

- **`class TipoChave(models.TextChoices):`**  
  Define uma enumeração de escolhas (herda de `TextChoices`) usada para o campo `tipo`. Facilita manter valores fixos com rótulos legíveis.

- **`SALA = 'sala', 'Chave de sala'`**  
  Valor da enumeração: o valor armazenado no banco é `'sala'` e o rótulo humano é `'Chave de sala'`.

- **`PREDIO = 'predio', 'Chave de predio'`**  
  Outro valor da enumeração: valor `'predio'`, rótulo `'Chave de predio'`.

### 2.2. Campo `tipo`

```python
tipo = models.CharField(
    'Tipo',
    max_length=10,
    choices=TipoChave.choices,
    default=TipoChave.SALA,
    help_text='Define se a chave pertence a sala ou ao predio',
)
```

- **`tipo = models.CharField(`**  
  Início da definição do campo `tipo` — um `CharField` que guarda qual tipo de chave é (sala ou prédio).

- **`'Tipo',`**  
  Primeiro argumento posicional do `CharField`: o `verbose_name` mostrado nas interfaces administrativas (rótulo humano).

- **`max_length=10,`**  
  Limita o tamanho máximo da string a 10 caracteres no banco de dados.

- **`choices=TipoChave.choices,`**  
  Define as escolhas válidas para o campo usando a enumeração `TipoChave`. No formulário será um select com essas opções.

- **`default=TipoChave.SALA,`**  
  Valor padrão para `tipo` quando nada for informado — aqui padrão é `SALA`.

- **`help_text='Define se a chave pertence a sala ou ao predio',`**  
  Texto de ajuda exibido em formulários/admin explicando o propósito do campo.

### 2.3. Campo `sala` (Foreign Key)

```python
sala = models.ForeignKey(
    'salas.Sala',
    verbose_name='Sala',
    on_delete=models.CASCADE,
    related_name='chaves',
    null=True,
    blank=True,
    help_text='Sala da chave',
)
```

- **`sala = models.ForeignKey(`**  
  Define o campo `sala` como `ForeignKey` referenciando o modelo de `Sala`. Armazena qual sala essa chave pertence (quando aplicável).

- **`'salas.Sala',`**  
  Referência ao modelo alvo usando string `app_label.ModelName` para evitar dependências diretas ou problemas de importação circular.

- **`verbose_name='Sala',`**  
  Rótulo humano do campo.

- **`on_delete=models.CASCADE,`**  
  Comportamento quando a `Sala` referenciada for deletada: `CASCADE` faz com que a chave também seja deletada.

- **`related_name='chaves',`**  
  O nome da relação reversa: a partir de uma `Sala` pode-se acessar `.chaves` para obter as chaves relacionadas.

- **`null=True,`**  
  Permite que o valor no banco seja NULL (sem referência).

- **`blank=True,`**  
  Permite que o campo fique em branco em formulários (não obrigatório).

- **`help_text='Sala da chave',`**  
  Texto de ajuda explicando o campo.

### 2.4. Campo `predio` (Foreign Key)

```python
predio = models.ForeignKey(
    'predios.Predio',
    verbose_name='Predio',
    on_delete=models.CASCADE,
    related_name='chaves_predio',
    null=True,
    blank=True,
    help_text='Predio da chave quando for chave geral',
)
```

- **`predio = models.ForeignKey(`**  
  Define o campo `predio` como `ForeignKey` para o modelo `Predio`. Usado quando a chave é geral do prédio.

- **`'predios.Predio',`**  
  Referência ao modelo `Predio` no app `predios`.

- **`verbose_name='Predio',`**  
  Rótulo humano.

- **`on_delete=models.CASCADE,`**  
  Deleta a `Chave` se o `Predio` referenciado for deletado.

- **`related_name='chaves_predio',`**  
  Nome da relação reversa: `Predio.chaves_predio` retorna as chaves de prédio.

- **`null=True,`**  
  Permite NULL no banco.

- **`blank=True,`**  
  Campo opcional em formulários.

- **`help_text='Predio da chave quando for chave geral',`**  
  Ajuda explicando quando usar `predio`.

## 3. Classe Meta (Configurações do Modelo)

```python
class Meta:
    verbose_name = 'Chave'
    verbose_name_plural = 'Chaves'
    db_table = 'chaves_chave'
    ordering = ['id']
```

- **`class Meta:`**  
  Meta-informações do modelo (configurações adicionais).

- **`verbose_name = 'Chave'`**  
  Nome singular usado em áreas administrativas e relatórios.

- **`verbose_name_plural = 'Chaves'`**  
  Nome plural usado em listas e títulos.

- **`db_table = 'chaves_chave'`**  
  Nome explícito da tabela no banco de dados (substitui o nome gerado automaticamente).

- **`ordering = ['id']`**  
  Ordenação padrão dos objetos para evitar warnings de paginação inconsistente em ListView.

## 4. Método `clean()` (Validações de Negócio)

```python
def clean(self):
    super().clean()
```

- **`def clean(self):`**  
  Método de validação de modelo chamado antes de salvar/form validar. Deve lançar `ValidationError` para sinalizar entradas inválidas.

- **`super().clean()`**  
  Chama a implementação base para manter qualquer validação herdada.

### 4.1. Validação para Chaves de Sala

```python
    if self.tipo == self.TipoChave.SALA:
        if not self.sala_id:
            raise ValidationError({'sala': 'Informe a sala para chave do tipo sala.'})
        if self.predio_id:
            raise ValidationError({'predio': 'Nao informe predio para chave do tipo sala.'})
```

- **`if self.tipo == self.TipoChave.SALA:`**  
  Inicia validações específicas quando o `tipo` é `SALA`.

- **`if not self.sala_id:`**  
  Verifica se o campo `sala` foi fornecido; se não houver `id`, considera inválido. Usa `self.sala_id` (seguro) ao invés de `self.sala.id`.

- **`raise ValidationError({'sala': 'Informe a sala para chave do tipo sala.'})`**  
  Lança `ValidationError` mapeado ao campo `sala` com a mensagem solicitando a sala. O dicionário garante que o erro apareça no campo correto no formulário.

- **`if self.predio_id:`**  
  Verifica se `predio` foi informado quando não deveria ser (para chave de sala). Se `predio_id` existir, isso é inválido.

- **`raise ValidationError({'predio': 'Nao informe predio para chave do tipo sala.'})`**  
  Lança erro apontando `predio` quando informado indevidamente.

### 4.2. Validação para Chaves de Prédio

```python
    if self.tipo == self.TipoChave.PREDIO:
        if not self.predio_id:
            raise ValidationError({'predio': 'Informe o predio para chave do tipo predio.'})
        if self.sala_id:
            raise ValidationError({'sala': 'Nao informe sala para chave do tipo predio.'})
```

- **`if self.tipo == self.TipoChave.PREDIO:`**  
  Validações quando o `tipo` é `PREDIO` (chave do prédio).

- **`if not self.predio_id:`**  
  Garante que `predio` esteja informado; se ausente, lança erro.

- **`raise ValidationError({'predio': 'Informe o predio para chave do tipo predio.'})`**  
  Mensagem de erro para `predio` faltante.

- **`if self.sala_id:`**  
  Verifica se `sala` foi preenchida indevidamente para uma chave de prédio.

- **`raise ValidationError({'sala': 'Nao informe sala para chave do tipo predio.'})`**  
  Mensagem de erro para `sala` quando não deve ser informada.

## 5. Propriedade `pode_emprestar`

```python
@property
def pode_emprestar(self):
    return self.tipo == self.TipoChave.SALA
```

- **`@property`**  
  Decorador que transforma o método seguinte em atributo somente-leitura do objeto (acessível como `instancia.pode_emprestar`).

- **`def pode_emprestar(self):`**  
  Define a propriedade `pode_emprestar` que indica se a chave pode ser emprestada.

- **`return self.tipo == self.TipoChave.SALA`**  
  Retorna `True` quando a chave é do tipo `SALA`, `False` caso contrário. Isso garante que apenas chaves de sala possam ser emprestadas.

## 6. Método `__str__()` (Representação em String)

```python
def __str__(self):
    if self.tipo == self.TipoChave.PREDIO and self.predio_id:
        return f"Chave Predio {self.predio.endereco}"
    if self.sala_id:
        return f"Chave Sala {self.sala.id}"
    return f"Chave {self.id}"
```

- **`def __str__(self):`**  
  Método que define a representação em string da instância (usada no admin, em listas e ao imprimir o objeto).

- **`if self.tipo == self.TipoChave.PREDIO and self.predio_id:`**  
  Se for chave de prédio e houver `predio_id` presente, formata a string usando o endereço do prédio.
  
  ✅ **Bom:** Usa `self.predio_id` (atributo FK seguro) ao invés de `self.predio.id`.

- **`return f"Chave Predio {self.predio.endereco}"`**  
  Retorna string legível com o endereço do prédio (acessa `predio.endereco`). Este acesso a `self.predio.endereco` é seguro aqui porque foi verificado que `predio_id` existe.

- **`if self.sala_id:`**  
  Se existe `sala_id`, retorna uma string indicando a sala (para chaves de sala).
  
  ✅ **Bom:** Usa `self.sala_id` (seguro) ao invés de `self.sala.id`.

- **`return f"Chave Sala {self.sala.id}"`**  
  Retorna string com id da sala.

- **`return f"Chave {self.id}"`**  
  Caso não haja `predio` nem `sala` definidos, retorna identificação genérica com o `id` da chave.

## 7. Observações e Recomendações

### 7.1. Segurança em Validações

No método `clean()`, é **mais seguro** usar os atributos `_id` (`self.sala_id`, `self.predio_id`) em vez de acessar `self.sala.id` / `self.predio.id`:

- `self.sala_id` acessa apenas a chave estrangeira no banco, sem carregar o objeto relacionado.
- `self.sala.id` tenta carregar o objeto inteiro; se `self.sala` for `None`, levanta `AttributeError`.

**Exemplo melhorado:**
```python
def clean(self):
    super().clean()
    if self.tipo == self.TipoChave.SALA:
        if not self.sala_id:  # Mais seguro
            raise ValidationError({'sala': 'Informe a sala para chave do tipo sala.'})
        if self.predio_id:  # Mais seguro
            raise ValidationError({'predio': 'Nao informe predio para chave do tipo sala.'})
    # ... resto do código
```

### 7.2. Mapeamento de Erros em Formulários

As validações usam dicionários em `ValidationError`:
```python
raise ValidationError({'campo': 'mensagem'})
```

Isso permite que formulários Django mostrem o erro **exatamente no campo correto**, melhorando a experiência do usuário.

### 7.3. Relacionamentos Reversos

Os nomes `related_name` bem definidos facilitam consultas reversas:

- `sala.chaves.all()`: obtém todas as chaves associadas a uma sala.
- `predio.chaves_predio.all()`: obtém todas as chaves de prédio.

Isso é útil em templates, views e queries otimizadas.

### 7.4. Propriedades vs Métodos

A propriedade `pode_emprestar` encapsula a lógica de negócio:

```python
# Em uma view ou template:
if chave.pode_emprestar:
    # lógica de empréstimo
```

Isso mantém a lógica concentrada no modelo e facilita manutenção futura.

## 8. Superusuário e Django Admin

Para acessar a área administrativa do projeto, é necessário criar um superusuário com o comando:

```bash
python manage.py createsuperuser
```

Durante a criação, o Django solicita:

- nome de usuário
- e-mail
- senha

Depois disso, o acesso é feito pela rota `/admin`, usando as credenciais criadas.

### 8.1. Para que serve

O superusuário permite entrar no Django Admin e gerenciar os modelos registrados no painel administrativo.

### 8.2. Observação importante

Se o projeto não tiver um superusuário criado, a tela `/admin` continuará existindo, mas não será possível autenticar.

## 9. Template de Login

O arquivo `login.html` é o template usado para montar a tela de autenticação do sistema.

Ele geralmente:

- estende o layout principal com `extends 'principal.html'`
- recebe um objeto `form` vindo da view
- exibe os campos de usuário e senha
- usa um botão de confirmação para enviar o login

### 9.1. Função no sistema

Esse template é o ponto de entrada para o usuário acessar a aplicação. Ele não cria autenticação sozinho; apenas renderiza a interface que envia os dados para a view de login do Django.

## 10. Template Base `principal.html`

O arquivo `principal.html` funciona como o layout base do sistema.

Ele centraliza elementos que se repetem em várias páginas, como:

- o cabeçalho do site
- a barra de navegação
- a exibição de mensagens do Django
- o rodapé
- o bloco `content`, onde cada página insere seu conteúdo específico

### 10.1. Função no sistema

Esse template evita repetição de código e garante que todas as páginas sigam o mesmo padrão visual.

## 11. Template `registros.html`

O arquivo `registros.html` mostra um resumo rápido dos principais dados do sistema.

Ele exibe cartões com contagens de:

- prédios
- salas
- chaves
- cópias
- reservas

### 11.1. Função no sistema

Esse template atua como um painel inicial de acompanhamento, ajudando o usuário a visualizar rapidamente a quantidade de registros cadastrados.

## 12. Configuração de Login em `settings.py`

No arquivo `settings.py`, estas configurações controlam o comportamento de entrada e saída do sistema:

```python
LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
```

### 12.1. O que cada uma faz

- `LOGIN_REDIRECT_URL = 'index'`: após o login, o usuário é enviado para a página inicial.
- `LOGIN_URL = 'login'`: quando uma página protegida é acessada sem autenticação, o Django manda para a tela de login.
- `LOGOUT_REDIRECT_URL = 'login'`: ao sair do sistema, o usuário volta para a tela de login.

### 12.2. Função no sistema

Essas linhas organizam o fluxo de autenticação do projeto, definindo para onde o usuário vai ao entrar, ao tentar acessar algo protegido e ao fazer logout.

## 13. Notificações por e-mail para empréstimos

O projeto também pode usar e-mail para avisar quando um empréstimo de chave estiver perto de vencer.

### 13.1. Como isso entra no contexto do sistema

- o empréstimo é salvo em `emprestimos.models.Emprestimo`
- a regra de aviso consulta os empréstimos com `status = aberto`
- quando a data prevista está dentro da janela configurada, o sistema cria uma notificação em `notificacoes.models.Notificacao`
- se o usuário tiver e-mail cadastrado, o aviso também pode ser enviado por SMTP usando o Gmail configurado em `settings.py`

### 13.2. Como o envio funciona

O envio pode ser executado por um comando de gerenciamento, por exemplo:

```bash
python manage.py enviar_alertas_emprestimos --dias 3
```

Esse comando procura os empréstimos que vencem em até 3 dias, registra a notificação e envia o e-mail para o usuário responsável.

### 13.3. Função no projeto

Esse fluxo atende ao requisito de lembrar o usuário antes do prazo de devolução da chave, evitando atraso e melhorando o controle do empréstimo.

---

**Autor:** Análise detalhada do modelo `Chave` do projeto ChaveMaster  
**Data:** Maio de 2026