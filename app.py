import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai.types import Completion
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

class ParametrosREA(BaseModel):
    nombre_programa: str
    verbo: str
    objeto: str
    contexto: str
    estrategia: str

@app.post("/CrearREA")
def creacion_rea(parametros_rea: ParametrosREA):

    try: 
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

        nombre_programa = parametros_rea.nombre_programa
        verbo = parametros_rea.verbo
        objeto = parametros_rea.objeto
        contexto = parametros_rea.contexto
        estrategia = parametros_rea.estrategia

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
                temperature = 1
            )

            respuesta = response.choices[0].message.content

            messages.append({'role' : 'system', 'content' : respuesta})

        resp_REA = messages[2]['content']
        
        return resp_REA
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Se ha presentado la excepción: {e}")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="crear_rea", port= 8000)