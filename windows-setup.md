- Start process - 

How-to setup this example in your Windows LOCAL machine:
This was only tested on a Windows LOCAL machine which serves as the AI Server machine, and this process was done for fun and for learning, and as an example to have something to be tested and running quickly.

1. Go to https://ollama.com/ and download it.
   Sign up with your email to get notified of new updates if you want to.
   Select Windows (Preview) and download it to your Windows machine.
2. Run the OllamaSetup.exe file on your Windows machine.
3. Follow the installation steps. Click Install to extract files and it will be installed in your machine.
4. To do a quick check to see if it was properly installed go to a CMD or Powershell and type:
   
  > ollama

  You should see something like this:

  Usage:
    ollama [flags]
    ollama [command]

  Available Commands:
    serve       Start ollama
    create      Create a model from a Modelfile
    show        Show information for a model
    run         Run a model
    pull        Pull a model from a registry
    push        Push a model to a registry
    list        List models
    ps          List running models
    cp          Copy a model
    rm          Remove a model
    help        Help about any command

  Flags:
    -h, --help      help for ollama
    -v, --version   Show version information

  Use "ollama [command] --help" for more information about a command.

5. Next step is to download the AI model or models that we are going to be using for this Chatbot specific example.
   If you want to see the complete list of ollama.ai models go to: https://ollama.com/library

   We are going to have 2 Cooks, the expert one will be using latest llama3 AI model, the novice one will be using the llama2 AI model.
   Diferences are in the number of parameters each of them are using and response quality.
   In this example we want to give more expertise to the expert cook than to the novice cook.

   From the CMD / Powershell run these 2 below commands. 
   Make sure you at least have 10GB disk free space to allocate both.
   
   The 'run' command will try to run the model locally where you can start testing it by prompting.
   If the model isn´t in your local installation it will be downloaded first (pulling manifest ...)
   It will take some time to download the models to your local installation.

   > ollama run llama3 
   Sample prompt: >>> Hi, why water is transparent?
   <You should see the answer>
   >>> /bye

   > ollama run llama2
   Sample prompt: >>> Hi, why makes rainbow show those colors?
   <You should see the answer>
   >>> /bye

6. Use one of your preferable Python coding editor and create a new python project and call it 'Chatbot_Cooking' for example.
7. Within the project create 2 different Modelfiles that will be used by the AI models to have domain specific answers, in this case related to Cooking.

   Modelfiles are used by the AI models to parametrize your AI models making them domain specific. 
   For example, my 'expert' model file is going to be more precise since it will be using llama3 and it will contain higher temperature value.
   The 'novice' model by the other hand will be less precise since it will be using llama2 and a lower temperature value.
   
   See examples at /artifacts folder for the 2 different models. They follow in here anyway.
     
   Model file 'Modelfile_expert' for the expert cook:

      FROM llama3
      # set the temperature to 1 [higher is more creative, lower is more coherent]
      PARAMETER temperature 1
      
      # Tamaño de la ventana de contexto para controlar el número de tokens que el modelo LLM puede usar como contexto para generar el siguiente token
      # En otras palabras, determina cuánto "recuerda" el modelo al generar texto.
      # El valor por defecto, lo he subido al doble
      PARAMETER num_ctx 4096
      
      # set the system prompt
      SYSTEM """
      Eres un sistema experto de recetas y nutrición.
      Ayuda a personas de todo tipo y condición a crear recetas muy nutritivas y saludables.
      Te llamas Alex y eres el gran experto evangelista de la cocina moderna y vanguardista.
      Siempre vas a contestar en español castellano.
      """
   
   Model file 'Modelfile_aprendiz' for the novice cook:

      FROM llama2
      # set the temperature to 1 [higher is more creative, lower is more coherent]
      PARAMETER temperature 0.75
      
      # Tamaño de la ventana de contexto para controlar el número de tokens que el modelo LLM puede usar como contexto para generar el siguiente token
      # En otras palabras, determina cuánto "recuerda" el modelo al generar texto.
      # El valor por defecto, lo he subido al doble
      PARAMETER num_ctx 4096
      
      # set the system prompt
      SYSTEM """
      Eres un sistema aprendiz de recetas y nutrición. 
      Ayuda a personas de todo tipo y condición a crear recetas muy nutritivas y saludables. 
      Te llamas Juan y eres el gran aprendiz de la cocina moderna y vanguardista. Siempre vas a contestar en español o castellano.
      """

7. Now, run from your CMD/Powershell console the following commands.

   > ollama create alex_experto -f ./Modelfile_experto
     We are creating a reference to the llama3 existing model but using the expert model file defined, so we are making AI model to be Cooking domain specific, with an expert cook.

   > ollama create juan_aprendiz -f ./Modelfile_aprendiz 
     We are creating a reference to the llama2 existing model but using the novice model file defined, so we are making AI model to be Cooking domain specific, with a novice cook.

8. If no issues found, you can list all the models using command:

    > ollama list

     You should see something like this:
      NAME                    ID              SIZE    MODIFIED
      juan_aprendiz:latest    643daf25f2e1    3.8 GB  2 days ago
      alex_experto:latest     3e08413ffd88    4.7 GB  2 days ago
      llama2:latest           78e26419b446    3.8 GB  8 days ago
      llama3:latest           a6990ed6be41    4.7 GB  2 weeks ago

9. Now the models are ready, and you can, as before, run the specific models.

  For example:
   > ollama run alex_experto
   >>> Hi, who are you?
    Hola! Me llamo Alex y soy un sistema experto en recetas y nutrición. Soy el gran evangelista de la cocina moderna
    y vanguardista. Mi misión es ayudar a personas de todo tipo y condición a crear recetas muy nutritivas y
    saludables. Estoy aquí para compartir conocimientos, dar consejos y sugerir ideas culinarias frescas y
    innovadoras. ¿En qué puedo ayudarte hoy?
    
    >>> Send a message (/? for help)

10. Next step is to jump into the bot creation and for that we will go to Telegram and search for BotFather bot.

    1. In there send the command /newbot
    2. Give it a name, something different to the one we created, it can be something like Ejemplo_Recetas_AI or any other name you like.
    3. When creating the name it will ask for the bot name which usually ends with _bot, so give it the name Ejemplo_Recetas_AI_bot.
    
    Once the bot is created a new telegram token API will be generated for that bot.

    4. Please copy all the information and paste it into your notepad editor and save the document, since that information will be used later on from the Python program.

11. Within the BotFather bot we are going to be creating also the different commands the user will be using from our Cooking bot.

    Type the following command in the BotFather
    /setcommands
    1. Select the new bot you are going to be sending the commands.

    It should respond with:
    OK. Send me a list of commands for your bot. Please use this format:
    command1 - Description
    command2 - Another description
    Send /empty to keep the list empty.

    2. Copy all the lines from the bot_comandos.txt file in the BotFather and send it.
    3. It should respond with Success! Command list updated. /help

  So, now if you go back to your new bot it should contain a Menu with all the commands.

12. Next step is to create a windows environment variable that will contain the Token API that was generated for the new bot.
    
    That variable will be used from the Python program. This is just for avoiding to make visible the API token in your Python program.
    1. Go to your windows environment variables and create your BOT_TOKEN variable.
    2. BOT_TOKEN = <your new telegram api content>

12. Great!!, now we have the AI part and the Telegram bot setup.
    
    Next is to create the Python program that will interact with both the Telegram bot and the AI models.

    1. Go to your best python code editor and create a file and call it recetas_ai.py. 
        * File is located under artifacts folder, copy and paste it in your code editor.

    2. Make sure that for the imports you have them installed in your python local installation.
       Use the command pip install <import_name> if not.
    
13. Run the program, and if no errors, you should see the following message indicating that the program is ready to accept commands from the Telegram bot 
    
    "Running Ollama with Recetas_SD Bot de Pruebas y modelo LLM Alex..."

14. Test it from your Telegram bot.
    
    1. Go to the list of commands and you should see the ones we set in BotFather.
    2. Try sending /quien_soy and see if you get a reply
    
    If ypu get a reply, then all seems to be properly setup, and working fine, and you can continue testing with the rest of the commands.
    Try sending /preguntar and after that ask for a new Cooking recipe.

- End Process -
