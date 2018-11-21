# Descrição
Esta é uma aplicação de um Web Service de sistema de gerenciamento de uma biblioteca, onde é possível cadastrar usuários e livros, além de realizar o gerenciamento de empréstimo de livros para usuários cadastrados.

A aplicação utiliza o SOAP 1.1 como protocolo de entrada e saída para troca de mensagens entre o cliente o servidor. O framework Django é utilizado como servidor web e também para a comunicação e troca de dados com o banco de dados.

# Interface
Os métodos do web service estão disponíveis no arquivo `library/views.py`. Deve-se estar familiarizado com a biblioteca Spyne para tender quais são os métodos, bem como os seus parâmetros de entrada e saída.

### Exemplos

O método `user_listing` não recebe nenhum parâmetro de entrada,
```
    @rpc(_returns=Iterable(User))
    def user_listing(ctx):
        try:
            return UserModel.objects.all()
        except UserModel.DoesNotExist:
            raise ResourceNotFoundError('User')
```
e retorna uma lista de usuários.

O método `get_user` recebe uma parâmetro de entrada chamado `email`,
```
    @rpc(Unicode, _returns=User)
    def get_user(ctx, email):
        try:
            return UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise ResourceNotFoundError('User')
```
e retorna um objetivo do tipo usuário, contendo os dados do usuário.

# Exemplos

A requisição deverá ser feita para o endpoint `http://localhost:8000/library/?wsdl`. Deve possuir um header `Content-Type` com valor `text/xml`.

## Cadastro de Usuários

#### Entrada
Exemplo de Envelope de requisição:
```
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="library.views">
	<soapenv:Body>
		<tns:create_user>
			<tns:user>
				<tns:name>Fulano de Tal</tns:name>
				<tns:email>fulano@example.com</tns:email>
				<tns:phone>1234567890</tns:phone>
			</tns:user>
		</tns:create_user>
	</soapenv:Body>
</soapenv:Envelope>
```

#### Saída
O web service deve retornar uma resposta do tipo:
```
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="library.views">
    <soap11env:Body>
        <tns:create_userResponse>
            <tns:create_userResult>
                <tns:id>1</tns:id>
                <tns:name>Fulano de Tal</tns:name>
                <tns:email>fulano@example.com</tns:email>
                <tns:phone>1234567890</tns:phone>
            </tns:create_userResult>
        </tns:create_userResponse>
    </soap11env:Body>
</soap11env:Envelope>
```

## Listagem de livros
#### Entrada
````
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="library.views">
	<soapenv:Body>
		<tns:book_listing />
	</soapenv:Body>
</soapenv:Envelope>
````

#### Saída
Se há algum livro cadastrado, provavelmente o web service retornará uma resposta do tipo:
````
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="library.views">
    <soap11env:Body>
        <tns:book_listingResponse>
            <tns:book_listingResult>
                <tns:Book>
                    <tns:id>1</tns:id>
                    <tns:title>Nome do Livro</tns:title>
                    <tns:isbn>1</tns:isbn>
                    <tns:description>Descrição</tns:description>
                    <tns:release_year>2018</tns:release_year>
                    <tns:publisher>Editora</tns:publisher>
                </tns:Book>
                <tns:Book>
                    <tns:id>2</tns:id>
                    <tns:title>Nome do Livro</tns:title>
                    <tns:isbn>1</tns:isbn>
                    <tns:description>Descrição</tns:description>
                    <tns:release_year>2018</tns:release_year>
                    <tns:publisher>Editora</tns:publisher>
                </tns:Book>
            </tns:book_listingResult>
        </tns:book_listingResponse>
    </soap11env:Body>
</soap11env:Envelope>
````

## Links Relevantes
A biblioteca Spyne foi utilizada para implementar o web service em conjunto com o framework Django: [http://spyne.io/](http://spyne.io/)
