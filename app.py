import streamlit as st
import requests
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler

# Configuración de la página
st.set_page_config(page_title="Diagnóstico de español", page_icon="🇪🇸")

# Título de la aplicación
st.title("Diagnóstico ")

# Obtener la API key de los secrets de Streamlit
api_key = st.secrets["api_key"]

def keep_alive():
    # Código para mantener la app activa
    print("App still alive!")

# Usar BackgroundScheduler en lugar de BlockingScheduler
sched = BackgroundScheduler()
sched.add_job(keep_alive, 'interval', minutes=30)
sched.start()

def evaluar_texto(api_key, texto):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": f"sk-tune-{api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta/llama-3.1-405b-instruct",
        "messages": [
            {"role": "system", "content": "Eres un asistente útil que evalúa textos en busca de errores gramaticales y mejoras de estilo."},
            {"role": "user", "content": f"Por favor, evalúa el siguiente texto, identificando errores gramaticales, sugiriendo mejoras de estilo y proporcionando una puntuación del 1 al 10:\n\n{texto}"}
        ],
        "stream": False,
        "frequency_penalty": 0.3,
        "max_tokens": 9000
    }

    try:
        respuesta = requests.post(url, headers=headers, json=payload)
        respuesta.raise_for_status()
        return respuesta.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Error en la solicitud: {str(e)}"

def main():
    texto_a_evaluar = st.text_area("Ingrese el texto a evaluar:", height=200)

    if st.button("Evaluar Texto"):
        if texto_a_evaluar:
            with st.spinner("Evaluando texto..."):
                resultado_evaluacion = evaluar_texto(api_key, texto_a_evaluar)
                st.subheader("Resultado de la Evaluación:")
                st.write(resultado_evaluacion)
        else:
            st.error("Por favor, ingrese el texto a evaluar.")

if __name__ == "__main__":
    main()
