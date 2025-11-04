# CalculadorasMed3 ⚕️

Plataforma Integrada de Calculadoras e Scores Médicos desenvolvida com Streamlit.

## 📋 Descrição

Esta plataforma foi desenvolvida para auxiliar profissionais de saúde na prática clínica diária, oferecendo acesso rápido e fácil a calculadoras e scores médicos importantes. Com uma interface moderna e intuitiva, permite o cálculo instantâneo durante atendimentos médicos.

A plataforma utiliza um sistema centralizado de dados do paciente, onde as informações são inseridas uma única vez e automaticamente utilizadas por todas as calculadoras disponíveis.

## 🎯 Calculadoras Disponíveis

### 🫀 Cardiologia

#### PREVENT - Risco Cardiovascular (AHA)
Calculadora da American Heart Association para estimativa de risco cardiovascular em 10 e 30 anos. Baseada nas equações PREVENT (Predicting Risk of cardiovascular disease EVENTs), esta ferramenta auxilia nas decisões sobre prevenção primária de doenças cardiovasculares.

**Parâmetros avaliados:**
- Idade (40-79 anos)
- Sexo
- Raça/Etnia
- Colesterol Total e HDL
- Pressão Arterial Sistólica
- Uso de anti-hipertensivos
- Presença de diabetes
- Tabagismo
- **eTFG (obrigatório)** - Taxa de Filtração Glomerular estimada
- **RACu (opcional)** - Relação Albumina/Creatinina Urinária
- **HbA1c (opcional)** - Hemoglobina Glicada

### 🍽️ Gastroenterologia

#### FIB-4 - Fibrose Hepática
Avaliação não invasiva de fibrose hepática usando idade, AST, ALT e contagem de plaquetas.

#### MELD - Model for End-Stage Liver Disease
Score utilizado para priorização de transplante hepático e avaliação de gravidade da doença hepática.

#### Child-Pugh - Classificação de Cirrose
Classificação da gravidade da cirrose hepática baseada em parâmetros clínicos e laboratoriais.

### 💧 Nefrologia

#### eTFG - Taxa de Filtração Glomerular Estimada
Cálculo usando equação CKD-EPI 2021 (sem ajuste racial) para estimativa da função renal.

#### Kt/V - Adequação da Diálise
Avaliação da adequação da hemodiálise usando fórmula de Daugirdas II.

### 🩺 Endocrinologia

#### IMC - Índice de Massa Corporal
Classificação do peso corporal segundo critérios da OMS.

#### HOMA-IR - Resistência Insulínica
Modelo homeostático para avaliação de resistência à insulina.

#### HOMA-Beta - Função das Células Beta
Modelo homeostático para avaliação da função pancreática (células beta).

## 🚀 Como Usar

### Localmente

1. Clone o repositório:
```bash
git clone https://github.com/MiguelJanssenn/CalculadorasMed3.git
cd CalculadorasMed3
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
streamlit run app.py
```

4. Acesse no navegador: `http://localhost:8501`

### Fluxo de Trabalho

1. **Preencha os Dados do Paciente**: Na aba "Dados do Paciente", insira todas as informações disponíveis do paciente
2. **Salve os Dados**: Clique em "Salvar Dados do Paciente"
3. **Selecione uma Calculadora**: Navegue pelas abas de especialidade ou use a aba "Todas as Calculadoras"
4. **Obtenha Resultados**: Clique no botão de cálculo para obter resultados instantâneos

## 📦 Dependências

- streamlit >= 1.28.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- plotly >= 5.17.0

## 🔧 Estrutura do Projeto

```
CalculadorasMed3/
├── app.py                    # Aplicação principal Streamlit
├── prevent_calculator.py     # Implementação da calculadora PREVENT
├── calculators/              # Módulo de calculadoras
│   ├── __init__.py
│   ├── gastro.py            # Calculadoras de Gastroenterologia
│   ├── nephro.py            # Calculadoras de Nefrologia
│   └── endocrino.py         # Calculadoras de Endocrinologia
├── test_prevent.py          # Testes da calculadora PREVENT
├── test_calculators.py      # Testes das outras calculadoras
├── examples.py              # Exemplos de uso
├── requirements.txt         # Dependências Python
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Documentação
```

## 🎨 Características

- **Interface Moderna**: Design limpo e profissional usando Streamlit
- **Sistema Centralizado**: Dados do paciente inseridos uma vez, usados por todas as calculadoras
- **Organização por Especialidade**: Abas dedicadas para cada especialidade médica
- **Cálculos Instantâneos**: Resultados em tempo real
- **Categorização de Risco**: Classificação clara do nível de risco
- **Recomendações Clínicas**: Orientações baseadas nos resultados
- **Responsivo**: Funciona em diferentes tamanhos de tela

## 📚 Referências

- American Heart Association - PREVENT Equations
- [AHA PREVENT Repository](https://github.com/AHA-DS-Analytics/PREVENT.git)
- CKD-EPI 2021 Equation
- KDOQI Guidelines
- WHO BMI Classification

## 🧪 Testes

Execute os testes com:

```bash
# Testar calculadora PREVENT
python test_prevent.py

# Testar outras calculadoras
python test_calculators.py

# Executar exemplos
python examples.py
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Adicionar novas calculadoras
- Melhorar a interface
- Corrigir bugs
- Melhorar a documentação

## ⚠️ Aviso Importante

Esta ferramenta é destinada ao auxílio na decisão clínica e **não substitui o julgamento médico**. Os resultados devem sempre ser interpretados no contexto clínico completo do paciente.

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional e clínico.

## ✨ Versão 2.0 - Novidades

- ✅ Sistema centralizado de dados do paciente
- ✅ Interface com abas por especialidade
- ✅ 9 calculadoras implementadas (Cardiologia, Gastroenterologia, Nefrologia, Endocrinologia)
- ✅ eTFG obrigatória no PREVENT
- ✅ Parâmetros opcionais (RACu e HbA1c) no PREVENT
- ✅ Testes automatizados para todas as calculadoras

---

Desenvolvido com ❤️ para a comunidade médica