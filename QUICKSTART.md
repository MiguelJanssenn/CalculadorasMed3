# Guia Rápido - Calculadoras Médicas

## 🚀 Início Rápido

### Opção 1: Usar Online (Recomendado)
1. Acesse o link da aplicação no Streamlit Cloud (após deploy)
2. Selecione a calculadora PREVENT
3. Preencha os dados do paciente
4. Clique em "Calcular Risco Cardiovascular"
5. Visualize os resultados e recomendações

### Opção 2: Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/MiguelJanssenn/CalculadorasMed3.git
cd CalculadorasMed3

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador em `http://localhost:8501`

## 📊 Calculadora PREVENT

### O que é?
A calculadora PREVENT estima o risco de eventos cardiovasculares em 10 e 30 anos, baseada nas equações da American Heart Association.

### Quando usar?
- Prevenção primária de doenças cardiovasculares
- Avaliação de risco em pacientes sem história de DCV
- Decisão sobre início de terapia com estatinas
- Definição de metas terapêuticas

### Parâmetros Necessários

**Demográficos:**
- Idade (40-79 anos)
- Sexo
- Raça/Etnia

**Clínicos:**
- Pressão arterial sistólica
- Uso de anti-hipertensivos
- Diabetes (sim/não)
- Tabagismo atual (sim/não)

**Laboratoriais:**
- Colesterol total (mg/dL)
- HDL colesterol (mg/dL)
- eGFR (opcional)

### Interpretação dos Resultados

#### Categorias de Risco:

1. **Baixo (<5%)**
   - Estilo de vida saudável
   - Monitoramento periódico

2. **Limítrofe (5-7.5%)**
   - Modificação intensiva do estilo de vida
   - Considerar estatina se outros fatores presentes

3. **Intermediário (7.5-20%)**
   - Estatina de intensidade moderada a alta
   - Controle rigoroso de PA
   - Considerar escore de cálcio coronário

4. **Alto (>20%)**
   - Estatina de alta intensidade
   - Controle agressivo de PA (<130/80)
   - Aspirina em prevenção primária
   - Considerar terapias adicionais

## 💡 Dicas de Uso

### Preparação
- Tenha os dados laboratoriais recentes do paciente
- Verifique a pressão arterial atual
- Confirme história de diabetes e tabagismo

### Durante o Atendimento
1. Abra a calculadora
2. Preencha os campos enquanto conversa com o paciente
3. Revise os dados antes de calcular
4. Discuta os resultados com o paciente

### Após o Cálculo
- Use as recomendações como guia
- Considere fatores individuais do paciente
- Documente no prontuário
- Planeje seguimento

## ⚠️ Limitações

- Válido apenas para idades entre 40-79 anos
- Prevenção primária (sem DCV prévia)
- Não substitui julgamento clínico
- Considere fatores não incluídos:
  - História familiar
  - Condições inflamatórias
  - Biomarcadores específicos

## 🔍 Validação dos Dados

Antes de calcular, verifique:
- ✅ Idade dentro da faixa (40-79)
- ✅ Dados laboratoriais recentes (<3 meses)
- ✅ PA medida adequadamente
- ✅ História clínica completa

## 📞 Suporte

Para problemas técnicos ou sugestões:
- Abra uma issue no GitHub
- Entre em contato com o desenvolvedor

## 🔄 Atualizações Futuras

Planejadas:
- CHA₂DS₂-VASc Score
- HAS-BLED Score
- GRACE Score
- Wells Score (TVP/TEP)
- Calculadora de Clearance
- E mais...

## 📚 Referências

1. Khan SS, et al. Novel Prediction Equations for Absolute Risk Assessment of Total Cardiovascular Disease Incorporating Cardiovascular-Kidney-Metabolic Health. Circulation. 2023.

2. American Heart Association. PREVENT Equations. https://github.com/AHA-DS-Analytics/PREVENT

3. ACC/AHA Guidelines on the Treatment of Blood Cholesterol.

---

**Última atualização:** Novembro 2024
