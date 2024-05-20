import os
import openai
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from openai.types import Completion

openai.api_key = os.getenv('OPENAI_API_KEY')

st.set_page_config(page_title='Creacion de REAs')

tab1, tab2 = st.tabs(["Creacion de REAs", "Correcion de REAs"])

with tab1:

    st.header('Creacion de Resultados de Aprendizaje asistidos por IA')
    st.markdown('''Crea tus REA ayudado por la Inteligencia Artificial. 
                Necesitarás ingresar una información base y te ayudaremos con ideas que 
                más tarde podrás refinar y modificar según tus necesidades y conocimiento.''')

    st.markdown('Vamos a determinar el **nombre del programa** para el que se crea el REA')

    st.markdown('### Paso 1: Nombre del programa')

    nombre_programa = st.text_input('Ingrese el nombre del programa')
        
    st.markdown('### Paso 2: Verbo a usar.')

    verbo = st.text_input('Ingrese el verbo a usar')

    st.markdown('### Paso 3: Cuál es el objeto')

    objeto = st.text_area('Ingrese el objeto a usar')

    st.markdown('### Paso 4: Ingrese el contexto.')

    contexto = st.text_area('Ingrese el contexto')

    st.markdown('### Paso 5: Ingrese la estrategia a usar.')

    estrategia = st.text_area('Ingrese la estrategia')

    #st.markdown('### Paso 6: Ingrese la justificacion del programa.')

    #justificacion = st.text_area('Ingrese la justificacion')

    if st.button('Construir REA'):

        with st.spinner('Creando el REA...'):

            preprompt = '''
                Eres un asistente universitario que ayuda a los docentes a crear los REA (Resultados de Aprendizaje Esperados) durante el proceso de la creación de los Campos de Aprendizaje Curricular,
                recibes indicaciones base de parte de un profesor y debes tener en cuenta los siguientes parámetros:


                El Resultado de Aprendizaje Esperado (REA) debe comenzar con un único verbo en infinitivo.
                El verbo usado debe demostrar acción.
                Se deben evitar términos como: "saber", "comprender", "aprender", "estar familiarizado con", "estar expuesto a" y "estar consciente de"
                El verbo utilizado se debe enmarcar en alguna de las dos categorías propuestas según el MEDIT de la Universidad de Cundinamarca: aplicar o crear
                El REA debe estar conformado por cuatro elementos esenciales: verbo + objeto + nivel + contexto
                Los REA han de centrarse en resultados y no en procesos. Es decir, se deben centrar en lo que el participante es capaz de demostrar.
                El REA debe ser observable y medible.
                Utiliza un lenguaje claro pero formal, propio de un docente. 

                A continuación tienes ejemplos de unos REAs y su composición según los cuatro elementos clave:

                Aplicar (verbo) los principios de finanzas internacionales (objeto) en una empresa real del sector (contexto) utilizando los 5 elementos diferenciales (Estrategia).

                Diseñar (verbo) un ambiente de aprendizaje (objeto), a partir del modelo ADDIE (Estrategia), para el desarrollo de un curso en línea (contexto).

                Crear (verbo) un plan de marketing digital (objeto) con alto grado de usabilidad (Estrategia) en la administración pública (contexto).

                Emplear (verbo) conceptos, normas e instrumentos de planeación participativa (objeto) en una propuesta de gestión comunitaria (contexto) en el marco del Sistema Municipal de Planeación y Presupuestos Participativos (Estrategia).

                Elaborar (verbo) los estados financieros (objeto) de una entidad ubicada en su localidad (contexto), según las NIFF para PYMES (Estrategia).

                Proponer (verbo) una solución informática (objeto) para el área de sistemas de una organización (contexto) teniendo en cuenta la matriz DOFA aplicada a ésta (Estrategia).
                '''

            REA_prompt = f'''
            Indicaciones del docente:
            Debes crear un REA para el CADI llamado {nombre_programa},  debe contener el verbo {verbo}, el objeto estar relacionado con 
            {objeto} teniendo en cuenta el contexto de {contexto} y la estrategia {estrategia}''' #teniendo en cuenta la justificacion del programa {justificacion}
            

    

            prompts = [REA_prompt]

            messages = [{'role' : 'system', 
                        'content' : preprompt}]


            for instrucciones in prompts:
                messages.append({'role' : 'user', 'content' : instrucciones})

                response = openai.chat.completions.create(
                    model = 'gpt-3.5-turbo',
                    messages = messages,
                    temperature = 0.8
                )

                respuesta = response.choices[0].message.content

                messages.append({'role' : 'system', 'content' : respuesta})

            resp_REA = messages[2]['content']

            st.markdown('## REA creado')
            st.write(resp_REA)
        
        st.success('Listo!')


with tab2:

    st.markdown('''Corrige tus REA ayudado por la Inteligencia Artificial. 
                Necesitarás ingresar una información base y te ayudaremos con ideas que 
                más tarde podrás refinar y modificar según tus necesidades y conocimiento.''')

    st.markdown('Vamos a determinar el **nombre del programa** para el que se crea el REA')

    st.markdown('### Paso 1: Nombre del programa')

    nombre_programa = st.text_input('Ingrese el nombre del programa.')
        
    st.markdown('### Paso 2: Ingresa tu idea preliminar del REA.')

    REA_usuario = st.text_area('Ingrese el REA')


    if st.button('Corregir REA'):

        with st.spinner('Revisando tu REA...'):

            preprompt = '''
                Eres un asistente universitario que ayuda a los docentes a corregir los REA (Resultados de Aprendizaje Esperados) durante el proceso de la creación de los Campos de Aprendizaje Curricular,
                recibes un REA base de parte de un profesor y debes tener en cuenta los siguientes parámetros para realizar las correcciones:


                El Resultado de Aprendizaje Esperado (REA) debe comenzar con un único verbo en infinitivo.
                El verbo usado debe demostrar acción.
                Se deben evitar términos como: "saber", "comprender", "aprender", "estar familiarizado con", "estar expuesto a" y "estar consciente de"
                El verbo utilizado se debe enmarcar en alguna de las dos categorías propuestas según el MEDIT de la Universidad de Cundinamarca: aplicar o crear
                El REA debe estar conformado por cuatro elementos esenciales: verbo + objeto + estrategia + contexto
                Los REA han de centrarse en resultados y no en procesos. Es decir, se deben centrar en lo que el participante es capaz de demostrar.
                El REA debe ser observable y medible.
                Se debe utilizar un lenguaje claro pero formal, propio de un docente. 

                A continuación tienes ejemplos de unos REAs y su composición según los cuatro elementos clave:

                Aplicar (verbo) los principios de finanzas internacionales (objeto) en una empresa real del sector (contexto) utilizando los 5 elementos diferenciales (Estrategia).

                Diseñar (verbo) un ambiente de aprendizaje (objeto), a partir del modelo ADDIE (Estrategia), para el desarrollo de un curso en línea (contexto).

                Crear (verbo) un plan de marketing digital (objeto) con alto grado de usabilidad (Estrategia) en la administración pública (contexto).

                Emplear (verbo) conceptos, normas e instrumentos de planeación participativa (objeto) en una propuesta de gestión comunitaria (contexto) en el marco del Sistema Municipal de Planeación y Presupuestos Participativos (Estrategia).

                Elaborar (verbo) los estados financieros (objeto) de una entidad ubicada en su localidad (contexto), según las NIFF para PYMES (Estrategia).

                Proponer (verbo) una solución informática (objeto) para el área de sistemas de una organización (contexto) teniendo en cuenta la matriz DOFA aplicada a ésta (Estrategia).
                '''

            REA_prompt_correccion = f'''
            REA base: {REA_usuario}, debes devolver unicamente el REA corregido, sin incluir aclaraciones de las correcciones realizadas.
            ''' 
            
            prompts = [REA_prompt_correccion]

            messages = [{'role' : 'system', 
                        'content' : preprompt}]


            for instrucciones in prompts:
                messages.append({'role' : 'user', 'content' : instrucciones})

                response = openai.ChatCompletion.create(
                    model = 'gpt-3.5-turbo',
                    messages = messages,
                    temperature = 0.8
                )

                respuesta = response.choices[0].message.content

                messages.append({'role' : 'system', 'content' : respuesta})

            resp_REA = messages[2]['content']

            st.markdown('## REA corregido')
            st.write(resp_REA)
        
        st.success('Listo!')