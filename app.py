# rodar local:  streamlit run app.py
import pandas as pd
import scipy.stats
import streamlit as st
import time

# estas são variáveis persistentes preservadas à medida que o Streamlin executa novamente esse script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('Jogando uma moeda')

def toss_coin(n):
    # Cria um container vazio que vai guardar o gráfico
    chart_placeholder = st.empty()
    
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    
    mean = None
    outcome_no = 0
    outcome_1_count = 0
    means_list = []  # guarda os valores para redesenhar o gráfico
    
    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        means_list.append(mean)
        
        # Limpa o container e redesenha o gráfico com todos os dados acumulados
        with chart_placeholder.container():
            st.line_chart(means_list)
        
        time.sleep(0.02)  # sleep menor para não travar
    
    return mean

number_of_trials = st.slider('Número de tentativas?', 1, 1000, 10)
start_button = st.button('Executar')

if start_button:
    st.write(f'Executando o experimento de {number_of_trials} tentativas.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iterations', 'mean'])
        ],
        axis=0)
    st.session_state['df_experiment_results'] = \
        st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])