# CalculadorasMed3 ⚕️

Plataforma de Calculadoras e Scores Médicos desenvolvida com Streamlit.

## 📋 Descrição

Esta plataforma foi desenvolvida para auxiliar profissionais de saúde na prática clínica diária, oferecendo acesso rápido e fácil a calculadoras e scores médicos importantes. Com uma interface moderna e intuitiva, permite o cálculo instantâneo durante atendimentos médicos.

## 🎯 Calculadoras Disponíveis

### PREVENT - Risco Cardiovascular (AHA)
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
- eGFR (opcional)

**Resultados fornecidos:**
- Risco cardiovascular em 10 anos
- Risco cardiovascular em 30 anos
- Categoria de risco (Baixo, Limítrofe, Intermediário, Alto)
- Recomendações clínicas específicas

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

### No Streamlit Cloud

A aplicação está disponível online em: [Link será adicionado após deploy]

## 📦 Dependências

- streamlit
- pandas
- numpy
- plotly

## 🔧 Estrutura do Projeto

```
CalculadorasMed3/
├── app.py                    # Aplicação principal Streamlit
├── prevent_calculator.py     # Implementação da calculadora PREVENT
├── requirements.txt          # Dependências Python
├── .gitignore               # Arquivos ignorados pelo Git
└── README.md                # Documentação
```

## 🎨 Características

- **Interface Moderna**: Design limpo e profissional usando Streamlit
- **Cálculos Instantâneos**: Resultados em tempo real
- **Categorização de Risco**: Classificação clara do nível de risco
- **Recomendações Clínicas**: Orientações baseadas nos resultados
- **Responsivo**: Funciona em diferentes tamanhos de tela

## 📚 Referências

- American Heart Association - PREVENT Equations
- [AHA PREVENT Repository](https://github.com/AHA-DS-Analytics/PREVENT.git)

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

## ✨ Próximas Funcionalidades

- [ ] Score de GRACE (Síndrome Coronariana Aguda)
- [ ] Score de CHA₂DS₂-VASc (Risco de AVC em FA)
- [ ] Score de HAS-BLED (Risco de sangramento)
- [ ] Calculadora de Clearance de Creatinina
- [ ] Score de WELLS (TVP e TEP)
- [ ] E muito mais...

---

Desenvolvido com ❤️ para a comunidade médica