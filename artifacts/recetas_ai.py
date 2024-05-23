import ollama
import telebot
import os
from datetime import datetime

if __name__ == '__main__':
    # Token del Chat Bot
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    
    # telebot controla la gestión de mensajes, comandos y eventos dentro del Chatbot.
    # TeleBot es la clase que permite interactuar con la API de Telegram, como enviar mensajes, responder a eventos y procesar comandos.
    # El token se utiliza para autenticar y autorizar las solicitudes del bot a la API de Telegram
    bot = telebot.TeleBot(BOT_TOKEN) 
    
    print("Running Ollama with Recetas_SD Bot de Pruebas y modelo LLM Alex...")
   
    # Ejemplo de inicialización de Usuarios Permitidos
    # usuarios_permitidos = os.environ.get("USUARIOS_PERMITIDOS")
        
    # Verificar si los usuarios permitidos no es None antes de usar el split()
    # Al menos necesitamos 2 usuarios para que no falle el split 
    # usuarios_permitidos = usuarios_permitidos.split(",")
   
    # Por defecto que use éste modelo (es una referencia al modelo LLAMA3) que fué el que descarqué en el Servidor
    # Comando utilizado: ollama create alex_experto -f ./Modelfile
    #
    model = "alex_experto" # El  modelo por defecto 
    
    recetas = ["Receta de arroz con leche", "Receta de pollo al curry", "Receta albondigas con carne", "Receta de ensalada de frutas", 
               "Receta de pizza con queso", "Receta de banana split", "Receta típica de la abuela", "Receta para hoy", "Receta especial muy nutritiva", "Receta de platanos con fresas espectacular",
               "Receta de gazpacho madrileño", "Receta de gazpacho andaluz", "Receta de típica paella valenciana", "Receta de cocido madrileño",
               "Receta de comida vegana", "Receta de comida con alto valor calórico", "Receta con muchas proteínas", "Receta para un desayuno energético"]
    
    # Control ¿Quien soy? - Introducción al Chatbot de Recetas
    @bot.message_handler(commands=['quien_soy']) # Cuando se recibe éste comando se ejecuta la siguiente función gestionar_quien_soy(mensaje)
    def gestionar_listado_recetas(mensaje): # Para gestionar cuando se recibe el comando /listado_recetas
        print("Entrando en la función para gestión del comando /quien_soy")
        
        # Verificar si el username está vacío o no está definido
        if mensaje.chat.username is None or mensaje.chat.username == "":    
            nombre_usuario = "Anónimo, veo que NO tienes un nombre de usuario (username) aún."
        else:
            nombre_usuario = mensaje.chat.username
        
        print("Visualizar Usuario:[" + nombre_usuario + "] Comando: /quien_soy");
        
        #if mensaje.chat.username in usuarios_permitidos:
        mensaje_bienvenida = (
                f"Hola <b>" + nombre_usuario +"!</b>\n\n"
                "¡Bienvenido a mi Chatbot de Recetas y Nutrición Saludable!\n\n"
                "Soy un Sistema de Inteligencia Artificial y puedo ayudarte con diversas tareas.\n\n"
                "Tengo 2 tipos de Cocineros que pueden ayudarte, y por defecto respondo como Alex:\n\n"
                "<b>Alex</b>: experto cocinero que tarda más en responder pero es más preciso en sus respuestas.\n\n"
                "<b>Juan</b>: aprendiz que tarda menos en responder pero es más impreciso en sus respuestas.\n\n"
                "Mira lo que puedo hacer por tí en el 'Menu' de comandos. Icono abajo a la Izquierda.\n"
                "<b>/listado_recetas</b>: recetas de ejemplo\n"
                "<b>/preguntar</b>: por una receta o lo que quieras\n"
                "<b>/cocineros_disponibles</b>: Listado de Cocineros de IA disponibles.\n"
                "<b>/selecionar_cocinero</b>: Seleccionar un Cocinero de IA disponible.\n"
        )
        bot.send_message(mensaje.chat.id, text=mensaje_bienvenida, parse_mode="html")
        #else:
        #    bot.send_message(mensaje.chat.id, "No tienes permiso para utilizar éste Chat Bot", parse_mode="html")

    # Control listado_recetas
    @bot.message_handler(commands=['listado_recetas']) # Cuando se recibe éste comando se ejecuta la siguiente función gestionar_listado_recetas(mensaje)
    def gestionar_listado_recetas(mensaje): # Para gestionar cuando se recibe el comando /listado_recetas
        print("Entrando en la función para gestión del comando /listado_recetas")
         # Verificar si el username está vacío o no está definido
        if mensaje.chat.username is None or mensaje.chat.username == "":    
            nombre_usuario = "Anónimo, veo que NO tienes un nombre de usuario aún."
        else:
            nombre_usuario = mensaje.chat.username

        print("Visualizar Usuario:[" + nombre_usuario + "] Comando: /listado_recetas");

        # if mensaje.chat.username in usuarios_permitidos:
        bot.send_message(mensaje.chat.id, "<b>Recetas de ejemplo:</b> \n" + '\n'.join(recetas), parse_mode="html")
        # else:
        #    bot.send_message(mensaje.chat.id, "No tienes permiso para utilizar éste Chat Bot", parse_mode="html")
    
    cocineros = ["alex_experto", "juan_aprendiz"]

    @bot.message_handler(commands=['cocineros_disponibles'])
    def chat_handler(message):
        print("Entrando en la función para gestión del comando /cocineros_disponibles")    
        # if message.chat.username in usuarios_permitidos:
        bot.send_message(message.chat.id,
                         "Cocineros de Inteligencia Artificial disponibles: \n<b>" + '\n'.join(cocineros) + '</b>',
                         parse_mode="html")
        #else:
            # bot.send_message(message.chat.id, "You are not allowed to use this bot", parse_mode="Markdown")

    @bot.message_handler(commands=['seleccionar_cocinero'])
    def chat_handler(message):
        print("Entrando en la función para gestión del comando /seleccionar_cocinero")    
        # if message.chat.username in usuarios_permitidos:
        sent_msg = bot.send_message(message.chat.id, 
                                    "¿Qué Cocinero de IA quieres usar?, escribe alguno de los dispobibles.", 
                                    parse_mode="html")
        sent_msg
        bot.register_next_step_handler(sent_msg, gestionar_cambio_cocinero)
        # else:
            # bot.send_message(message.chat.id, "You are not allowed to use this bot", parse_mode="Markdown")

    # Control preguntar
    @bot.message_handler(commands=['preguntar']) # Cuando se recibe éste comando se ejecuta la siguiente función gestionar_preguntar(mensaje)
    def gestionar_preguntar(mensaje): # Para gestionar cuando se recibe el comando /preguntar
            print("Entrando en la función para gestión del comando /preguntar")
            if mensaje.chat.username is None or mensaje.chat.username == "":    
                nombre_usuario = "Anónimo, veo que NO tienes un nombre de usuario aún."
            else:
                nombre_usuario = mensaje.chat.username
            
            print("Visualizar Usuario:[" + nombre_usuario + "] Comando: /preguntar");

            emoji_saboreando_comida = "\U0001F60B" # Emoji saboreando comida
            #if mensaje.chat.username in usuarios_permitidos:
            sent_msg = bot.send_message(mensaje.chat.id,"Dime, qué <b>Receta</b> te apetece " + emoji_saboreando_comida +"?.\nTambién me puedes preguntar por cualquier otra cosa.", parse_mode="html")
            bot.register_next_step_handler(sent_msg, gestionar_preguntar) # función de pasos siguientes (next step handler) que será llamada automáticamente después de que se haya completado una acción o paso anterior en la conversación.
            #else:
            #    bot.send_message(mensaje.chat.id, "No tienes permiso para utilizar éste Chat Bot", parse_mode="html")
    
    # Control siguiente mensaje después del comando /preguntar
    def gestionar_preguntar(mensaje): # Permite gestionar el siguiente mensaje que viene del Chat de Telegram (ejemplo al preguntar)
            msg = mensaje.text # Extrae el mensaje que viene del Chat y guardalo en la variable 'msg'
            
            emoji_cocinando = "\U0001F373" # Emoji Cocinando
            emoji_esperando = "\U000023F3" # Emoji Reloj Esperando
            
            # Formatear la respuesta con Markdown

            # Envía estos 2 mensajes
            timestamp_str = datetime.now()
            formatted_start_datetime = timestamp_str.strftime('%d/%m/%Y %H:%M:%S')
            bot.send_message(mensaje.chat.id, "Fecha y hora de la petición: <b>" + formatted_start_datetime + "</b>\n\nUtilizando el Cocinero de Inteligencia Artificial en Recetas:\n[<b>" + model + "</b>]\n\n" + "Estoy buscando la mejor respuesta lo antes posible. Me has pedido:\n[<b>" + msg + "</b>]\n", parse_mode="html")
            bot.send_message(mensaje.chat.id, "Dame unos segunditos y enseguida te respondo. Vamos a cocinar tu petición " + emoji_cocinando + " " + emoji_esperando, parse_mode="html")
            response = ollama.chat(model=model, messages=[ # Obtén la respuesta de Ollama usando el modelo Alex y pásale como contenido el mensaje extraído del chat
                {
                    'role': 'user',
                    'content': msg,
                    'options': {
                        'priority': 'high',  # Prioridad Alta
                        'language': 'es',    # Español
                    },
                }
            ])
            answer = response['message']['content'] # Extrae la respuesta generada por Ollama
            # html_content = markdown2.markdown(answer)
            answer = answer.replace('**', '')  # Eliminar '**' del texto
            # answer = answer.replace('&quot;', '') 
            # print(answer)
            # answer = html.escape(answer)  # Escapar caracteres especiales
            # respuesta_formateada = f"{answer}\n"
            
            # Timestamp para la fecha y hora de respuesta
            timestamp_str = datetime.now()
            formatted_end_datetime = timestamp_str.strftime('%d/%m/%Y %H:%M:%S')
            bot.send_message(mensaje.chat.id, "Fecha y hora de la respuesta: <b>" + formatted_end_datetime + "</b>\n\n" + answer, parse_mode="html") # Envia la respuesta generada al Chat formateada

            # bot.send_message(mensaje.chat.id, "Fecha y hora de la petición: <b>" + formatted_end_datetime + "</b>\n\n" + answer, parse_mode="html") # Envia la respuesta generada al Chat

    # Seleccionado el cocinero quiero que cambie al modelo correspondiente
    def gestionar_cambio_cocinero(message):
        new_model = message.text
        if message.text in cocineros:
            data = ollama.list()

            # Comprobar si coincide el nombre del modelo (posibles son alex_experto y juan_aprendiz)
            matched = False
            for mod in data['models']:
                if new_model in mod['name']:
                    matched = True

            if not matched: # si no coincide 
                bot.send_message(message.chat.id, "No he encontrado al Cocinero de Inteligencia Artificial...", parse_mode="html")
                # ollama.pull(new_model)
                # bot.send_message(message.chat.id, "Model aplicado con éxito!!!", parse_mode="html")
            
            # Si existe entonces cambiar el modelo
            global model
            model = new_model
            bot.send_message(message.chat.id, "El Cocinero de Inteligencia Artificial seleccionado es <b>[" + new_model + "]</b>", parse_mode="html")
        else:
            bot.send_message(message.chat.id, "El Cocinero de Inteligencia Artificial " + new_model + " no exite o no está soportado!", parse_mode="html")

    # Bucle de escucha continuo para recibir y procesar mensajes de Telegram de manera persistente. No se utiliza Webhook.
    # El bot comunica en éste caso utilizando el mecanismo de polling (getUpdates), es decir le pregunta constantemente a Telegram si hay nuevos mensajes
    bot.infinity_polling() 
