# Guia de Deploy no Streamlit Cloud

## Passo a Passo para Deploy

### 1. Preparação do Repositório

O repositório já está configurado com os arquivos necessários:
- ✅ `app.py` - Aplicação principal
- ✅ `prevent_calculator.py` - Lógica da calculadora
- ✅ `requirements.txt` - Dependências
- ✅ `.streamlit/config.toml` - Configuração do Streamlit

### 2. Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io/

2. Faça login com sua conta GitHub

3. Clique em "New app"

4. Configure:
   - **Repository**: MiguelJanssenn/CalculadorasMed3
   - **Branch**: main (ou copilot/add-prevent-calculator se ainda não foi merged)
   - **Main file path**: app.py

5. Clique em "Deploy!"

6. Aguarde alguns minutos para o deploy ser concluído

### 3. Acesso à Aplicação

Após o deploy, você receberá um URL como:
```
https://[your-app-name].streamlit.app
```

### 4. Atualizações

Qualquer commit no repositório irá automaticamente atualizar a aplicação no Streamlit Cloud.

## Configurações Opcionais

### Secrets (se necessário no futuro)

Para adicionar secrets (chaves de API, etc):
1. No Streamlit Cloud, vá em App settings
2. Clique em "Secrets"
3. Adicione suas configurações no formato TOML

### Configurações Avançadas

No arquivo `.streamlit/config.toml` você pode personalizar:
- Tema de cores
- Porta do servidor
- Configurações de cache
- E muito mais

## Troubleshooting

### Erro de Dependências
- Verifique se todas as dependências estão no `requirements.txt`
- Use versões compatíveis das bibliotecas

### Erro de Memória
- O Streamlit Cloud oferece recursos limitados
- Otimize seu código para usar menos memória

### App Lento
- Use `@st.cache_data` para cachear funções pesadas
- Minimize cálculos desnecessários

## Monitoramento

- Acesse os logs em tempo real no Streamlit Cloud
- Configure notificações por email para erros
- Use analytics do Streamlit para ver uso

## Recursos Adicionais

- [Documentação Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Fórum Streamlit](https://discuss.streamlit.io/)
- [Exemplos de Apps](https://streamlit.io/gallery)
