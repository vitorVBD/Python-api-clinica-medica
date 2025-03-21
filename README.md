<p align="center"> <img src="./assets/python-logo.png" alt="API Clínica Médica" width="150" /> <br /> <b>API Clínica Médica</b> <br /> <sub><sup><b>(Python-api-clinica-medica)</b></sup></sub> <br /> </p> <p align="center"> Este projeto é uma API robusta, segura e eficiente para gerenciar dados de médicos, secretários, pacientes e laudos. A API também é capaz de gerar laudos em PDF automaticamente, unindo informações do médico responsável e os dados clínicos do paciente atendido. <br /> </p>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI Badge"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL Badge"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-FF6F61?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy Badge"/>
  <img src="https://img.shields.io/badge/Bcrypt-0A0A0A?style=for-the-badge&logo=security&logoColor=white" alt="Bcrypt Badge"/>
  <img src="https://img.shields.io/badge/Dotenv-4B8BBE?style=for-the-badge&logo=python&logoColor=white" alt="Dotenv Badge"/>
</p>

## Estrutura do Projeto

### Funcionalidades
- **Gerenciamento de Médicos**: Cadastro, atualização, listagem e remoção de médicos.
- **Gerenciamento de Secretários**: Cadastro, atualização, listagem e remoção de secretários.
- **Gerenciamento de Pacientes**: Cadastro, atualização, listagem e remoção de pacientes.
- **Geração de Laudos em PDF**: Geração automática de laudos em PDF com informações do médico e dados clínicos do paciente. (Em Construção)

### Estrutura de Pastas

```
├── .env
├── README.md
├── src
│ ├── main.py
│ ├── pycache
│ │ └── main.cpython-312.pyc
│ ├── auth
│ │ └── security.py
│ ├── database
│ │ ├── database.py
│ │ └── pycache
│ ├── models
│ │ ├── Doctor.py
│ │ ├── Patient.py
│ │ └── Secretary.py
│ ├── repositories
│ │ ├── Doctor_Repository.py
│ │ ├── Patient_Repository.py
│ │ └── Secretary_Respository.py
│ ├── routes
│ │ ├── Doctor_Controller.py
│ │ ├── Patient_Controller.py
│ │ ├── Secretary_Controller.py
│ │ └── router.py
│ ├── schemas
│ └── services
│ ├── Doctor_Service.py
│ ├── Patient_Service.py
│ └── Secretary_Service.py
└── venv
```

### Tecnologias e Ferramentas Utilizadas
- **FastAPI**: Framework para construção da API.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **PostgreSQL**: Banco de dados utilizado.
- **bcrypt**: Biblioteca para hashing de senhas.
- **dotenv**: Biblioteca para carregar variáveis de ambiente.
- **Python**: Linguagem de programação utilizada.

### Licença
Este software é licenciado sob os termos da MIT License.

---

<div align="center">

⌨️ Desenvolvido por [Vitor Bittencourt](https://github.com/vitorVBD) ☕

</div>