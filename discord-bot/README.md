## CAP6640 Project

### Discord Bot

This is the bot source integrated with the classifier.

- Install the Virtual Env and all the required libs:
```shell script
./setup.sh
```

- Provide a file with the tokens `token.txt` and the file with the trained model file `hate_speech_model.h5`
```shell script
echo 'your_discord_app_token' > token.txt
cp where_the_model_is/hate_speech_model.h5 .
```

- Activate the virtual env and run the code :
```shell script
source bin/activate
python3 src/main.py
```
