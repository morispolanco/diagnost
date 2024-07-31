import streamlit as st
import requests
import json

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

    respuesta = requests.post(url, headers=headers, json=payload)
    if respuesta.status_code == 200:
        return respuesta.json()['choices'][0]['message']['content']
    else:
        return f"Error: {respuesta.status_code} - {respuesta.text}"

def main():
    st.title("Aplicación de Evaluación de Texto")

    api_key = st.text_input("Ingrese su clave de API:", type="password")
    texto_a_evaluar = st.text_area("Ingrese el texto a evaluar:", height=200)

    if st.button("Evaluar Texto"):
        if api_key and texto_a_evaluar:
            with st.spinner("Evaluando texto..."):
                resultado_evaluacion = evaluar_texto(api_key, texto_a_evaluar)
                st.subheader("Resultado de la Evaluación:")
                st.write(resultado_evaluacion)
        else:
            st.error("Por favor, proporcione tanto la clave de API como el texto a evaluar.")

if __name__ == "__main__":
    main()
