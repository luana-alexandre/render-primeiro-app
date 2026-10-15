import pandas as pd
import scipy.stats
import streamlit as st
import time

# Preserva as variáveis entre as interações da sessão
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iterations', 'mean']
    )

st.header('Jogando uma moeda')

chart = st.empty()
chart.line_chart([0.5])


def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    means = [0.5]
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1

        if r == 1:
            outcome_1_count += 1

        mean = outcome_1_count / outcome_no
        means.append(mean)

        chart.line_chart(means)
        time.sleep(0.05)

    return mean


number_of_trials = st.slider('Número de tentativas?', 1, 1000, 10)
start_button = st.button('Executar')

if start_button:
    st.write(f'Executando o experimento de {number_of_trials} tentativas.')

    mean = toss_coin(number_of_trials)
    st.session_state['experiment_no'] += 1

    new_result = pd.DataFrame(
        data=[[
            st.session_state['experiment_no'],
            number_of_trials,
            mean
        ]],
        columns=['no', 'iterations', 'mean']
    )

    st.session_state['df_experiment_results'] = pd.concat(
        [
            st.session_state['df_experiment_results'],
            new_result
        ],
        ignore_index=True
    )

st.write(st.session_state['df_experiment_results'])